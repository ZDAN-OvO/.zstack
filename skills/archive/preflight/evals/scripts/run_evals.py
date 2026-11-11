#!/usr/bin/env python3
"""Run each preflight case with/without the skill in a temporary fixture copy.

Usage: run_evals.py <iteration-dir> [--model M] [--jobs J] [--only id,id]
Successful runs resume only when their inputs match. Failed/legacy runs retry.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

HERE = Path(__file__).resolve().parent.parent
SKILL = HERE.parent
FIX = HERE / "eval-fixtures"
GENERATED_DIRS = {"node_modules", ".git", ".venv", "__pycache__"}


def is_generated(path):
    return bool(GENERATED_DIRS.intersection(Path(path).parts))


def write_json(path, value):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(path)


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def snapshot(root):
    result = {}
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = [name for name in subdirs if name not in GENERATED_DIRS]
        for name in files:
            path = Path(directory) / name
            if path.is_file():
                result[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def text(value):
    return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")


def parse_events(raw):
    """Use completed assistant messages, never partial text deltas."""
    final, tokens, tools, transcript, last = "", 0, {}, [], None
    for line in raw.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "message_end":
            continue
        message = event["message"]
        if message.get("role") == "assistant":
            last = message
            tokens += (message.get("usage") or {}).get("totalTokens", 0)
            blocks = []
            for content in message.get("content", []):
                if content.get("type") == "text":
                    blocks.append(content["text"])
                    transcript.append("ASSISTANT: " + content["text"])
                elif content.get("type") == "toolCall":
                    tools[content["name"]] = tools.get(content["name"], 0) + 1
                    transcript.append(f"TOOL {content['name']}: " + json.dumps(content.get("arguments"), ensure_ascii=False))
            final = "\n\n".join(blocks)
        elif message.get("role") == "toolResult":
            result = "".join(c.get("text", "") for c in message.get("content", []) if c.get("type") == "text")
            transcript.append("RESULT: " + result)
    if not last or last.get("stopReason") != "stop" or not final.strip():
        reason = (last or {}).get("errorMessage") or (last or {}).get("stopReason", "no completed assistant message")
        raise ValueError(f"incomplete model response: {reason}")
    return final, tokens, tools, "\n\n".join(transcript)


def run_one(case, config, it_dir, model, timeout=900):
    name = f"eval-{case['id']}-{case['name']}"
    run_dir = Path(it_dir).resolve() / name / config / "run-1"
    run_dir.mkdir(parents=True, exist_ok=True)
    signature = fingerprint({"case": case, "config": config, "model": model,
                             "fixture": snapshot(FIX / case["fixture"]),
                             "skill": {str(p.relative_to(SKILL)): hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in [SKILL / "SKILL.md", *sorted((SKILL / "references").rglob("*"))]
                                       if p.is_file()} if config == "with_skill" else None})
    status_file = run_dir / "status.json"
    if status_file.exists():
        status = json.loads(status_file.read_text())
        if status.get("status") == "success":
            if status.get("input_hash") != signature:
                return name, config, "FAILED inputs changed; use a new iteration directory"
            required = ["outputs/response.md", "changes.json", "transcript.md", "timing.json", "metrics.json"]
            if all((run_dir / p).exists() for p in required) and (run_dir / "workspace-after").is_dir():
                return name, config, "skip"
    # Remove old attempt artifacts so a failed retry cannot expose stale outputs/grades.
    for directory in ("outputs", "workspace-after"):
        shutil.rmtree(run_dir / directory, ignore_errors=True)
    for filename in ("grading.json", "grading-status.json"):
        (run_dir / filename).unlink(missing_ok=True)
    (run_dir / "outputs").mkdir()
    meta = {"eval_id": case["id"], "eval_name": case["name"], "prompt": case["prompt"],
            "assertions": case["expectations"]}
    # The two configurations share metadata; write once in main before starting workers.
    meta_path = run_dir.parents[1] / "eval_metadata.json"
    if not meta_path.exists():
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    prompt = case["prompt"]
    args = ["pi", "-p", "--mode", "json", "--no-session", "-ns", "-ne", "-nc", "--no-mcp",
            "--no-prompt-templates", "--tools", "read,bash,edit,write,grep,find,ls", "--model", model]
    if config == "with_skill":
        args += ["--skill", str(SKILL)]
        if case["explicit"]:
            prompt = "/skill:preflight " + prompt
    else:
        prompt = re.sub(r"/skill:preflight\b[ \t]*", "", prompt)
    write_json(run_dir / "input.json", {"case": case, "config": config, "model": model,
                                        "effective_prompt": prompt, "input_hash": signature})
    write_json(status_file, {"status": "running", "input_hash": signature})
    started = time.monotonic()
    raw, stderr, returncode, error = "", "", None, None
    with tempfile.TemporaryDirectory(prefix=f"pf-{case['id']}-{config}-") as temp:
        ws = Path(temp)
        try:
            shutil.copytree(FIX / case["fixture"], ws, dirs_exist_ok=True)
            before = snapshot(ws)
            try:
                process = subprocess.run(args + ["--", prompt], cwd=ws, stdin=subprocess.DEVNULL,
                                         capture_output=True, text=True, timeout=timeout)
                raw, stderr, returncode = process.stdout, process.stderr, process.returncode
            except subprocess.TimeoutExpired as exc:
                raw, stderr = text(exc.stdout), text(exc.stderr)
                raise ValueError(f"execution timed out after {timeout}s") from exc
            if returncode != 0:
                raise ValueError(f"pi exited with code {returncode}; see stderr.log")
            final, tokens, tools, transcript = parse_events(raw)
            after = snapshot(ws)
            changed = sorted(k for k in after if before.get(k) != after[k])
            deleted = sorted(k for k in before if k not in after)
            out = run_dir / "outputs"
            (out / "response.md").write_text(final, encoding="utf-8")
            for key in changed:
                target = out / "files" / key
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ws / key, target)
            write_json(run_dir / "changes.json", {"changed": changed, "deleted": deleted,
                       "excluded_directory_names": sorted(GENERATED_DIRS)})
            (run_dir / "transcript.md").write_text(transcript, encoding="utf-8")
            write_json(run_dir / "metrics.json", {"tool_calls": tools, "total_tool_calls": sum(tools.values()),
                                                  "output_chars": len(final)})
            shutil.copytree(ws, run_dir / "workspace-after", ignore=shutil.ignore_patterns(*GENERATED_DIRS))
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            (run_dir / "outputs/response.md").unlink(missing_ok=True)
        finally:
            (run_dir / "events.jsonl").write_text(raw, encoding="utf-8")
            (run_dir / "stderr.log").write_text(stderr, encoding="utf-8")
            duration = time.monotonic() - started
            write_json(run_dir / "timing.json", {"duration_ms": int(duration * 1000),
                       "total_tokens": locals().get("tokens", 0), "total_duration_seconds": round(duration, 1)})
            write_json(status_file, {"status": "failed" if error else "success", "error": error,
                                    "returncode": returncode, "input_hash": signature})
    return name, config, f"FAILED {error}" if error else f"{duration:.0f}s changed={len(changed)}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iteration_dir")
    parser.add_argument("--model", default="auto/deepseek-v4.1-flash")
    parser.add_argument("--jobs", type=positive_int, default=8)
    parser.add_argument("--timeout", type=positive_int, default=900)
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    cases = json.loads((HERE / "evals.json").read_text())["evals"]
    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        unknown = wanted - {str(c["id"]) for c in cases}
        if unknown:
            parser.error(f"unknown eval IDs: {', '.join(sorted(unknown))}")
        cases = [c for c in cases if str(c["id"]) in wanted]
    for case in cases:
        if not (FIX / case["fixture"]).is_dir():
            parser.error(f"fixture missing: {case['fixture']}")
    iteration = Path(args.iteration_dir).resolve()
    iteration.mkdir(parents=True, exist_ok=True)
    for case in cases:
        directory = iteration / f"eval-{case['id']}-{case['name']}"
        directory.mkdir(exist_ok=True)
        meta = {"eval_id": case["id"], "eval_name": case["name"], "prompt": case["prompt"], "assertions": case["expectations"]}
        path = directory / "eval_metadata.json"
        if path.exists() and json.loads(path.read_text()) != meta:
            parser.error(f"case changed: {path}; use a new iteration directory")
        write_json(path, meta)
    failures = 0
    with ThreadPoolExecutor(args.jobs) as pool:
        tasks = [pool.submit(run_one, case, config, iteration, args.model, args.timeout)
                 for case in cases for config in ("with_skill", "without_skill")]
        for task in as_completed(tasks):
            name, config, message = task.result()
            failures += message.startswith("FAILED")
            print(f"RUN {name} {config} {message}", flush=True)
    print(f"RUNS: {len(tasks)} total, {failures} failed", flush=True)
    return int(failures > 0)


if __name__ == "__main__":
    raise SystemExit(main())
