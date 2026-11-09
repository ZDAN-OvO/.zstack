#!/usr/bin/env python3
"""收集 /tmp 下的 eval 运行结果到 evals/iteration-N，并生成 grading.json / timing.json。

用法：python3 evals/grade.py <run-root> <iteration-dir> [<结果目录名>=<工作区子目录名> ...]
      默认 with_skill=with_skill without_skill=without_skill；改进已有技能时用 new_skill=with_skill
      python3 evals/grade.py --fix-benchmark <iteration-dir> <model>   # aggregate_benchmark 之后运行
  run-root:      /tmp/to-brief-eval（每个 eval 一个 <id>-<name>/<config>/ws 工作区）
  iteration-dir: evals/iteration-1（需预先放好 judgments.json 人工评分）
[auto] 断言由本脚本判定；其余断言读取 judgments.json。
"""
import glob, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
CHECKER = SKILL / "scripts" / "check-brief.mjs"
SESSIONS = Path.home() / ".pi/agent/sessions/subagent"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def session_for(ws):
    """按 session 头里的 cwd 找到子代理会话文件。"""
    hits = []
    for f in SESSIONS.glob("*/*.jsonl"):
        with open(f) as fh:
            head = json.loads(fh.readline())
        if head.get("cwd") == str(ws):
            hits.append(f)
    return max(hits, key=lambda f: f.stat().st_mtime) if hits else None


def read_session(f):
    final, tokens, start, end, tools = "", 0, None, None, {}
    for line in open(f):
        d = json.loads(line)
        m = d.get("message") or {}
        if m.get("role") == "assistant":
            tokens += (m.get("usage") or {}).get("totalTokens", 0)
            ts = m.get("timestamp")
            start = start or ts
            end = ts
            texts = [c["text"] for c in m.get("content", []) if c.get("type") == "text"]
            for c in m.get("content", []):
                if c.get("type") == "toolCall":
                    tools[c.get("name", "?")] = tools.get(c.get("name", "?"), 0) + 1
            if texts and m.get("stopReason") != "toolUse":
                final = "\n".join(texts)
    secs = round((end - start) / 1000, 1) if start and end else None
    return final, tokens, secs, tools


def changed_files(fixture, ws):
    out = []
    for p in Path(ws).rglob("*"):
        if p.is_file():
            rel = p.relative_to(ws)
            src = fixture / rel
            if not src.exists() or sha(src) != sha(p):
                out.append(rel)
    return out


def check(path):
    r = subprocess.run(["node", str(CHECKER), str(path)], capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()


def auto(text, fixture, ws, new_briefs, final):
    """返回 (passed, evidence)。"""
    t = text.lower()
    briefs = [ws / b for b in new_briefs]
    if "no brief file is written" in t:
        return (not briefs, f"new briefs: {[str(b) for b in new_briefs] or 'none'}")
    if "exactly one new brief" in t:
        return (len(briefs) == 1, f"new briefs: {[str(b) for b in new_briefs] or 'none'}")
    if "passes check-brief" in t:
        if not briefs:
            return ("any newly" in t, "no new brief")
        res = [check(b) for b in briefs]
        return (all(ok for ok, _ in res), "; ".join(f"{b.name}: {msg}" for b, (ok, msg) in zip(briefs, res)))
    m = re.search(r"stage is (\w+)", t)
    if m:
        if len(briefs) != 1:
            return (False, "no single brief to read")
        stage = re.search(r"^- Stage: (\S+)", briefs[0].read_text(), re.M)
        got = stage.group(1) if stage else None
        return (got == m.group(1), f"Stage: {got}")
    if "unchanged" in t:
        rel = "local/briefs/competitor-usp-direction.md"
        same = sha(fixture / rel) == sha(ws / rel)
        return (same, "sha256 identical to fixture" if same else "file was modified")
    if "in english" in t:
        if len(briefs) != 1:
            return (False, "no single brief")
        body = briefs[0].read_text()
        cjk = len(re.findall(r"[\u4e00-\u9fff]", body))
        return (cjk == 0, f"CJK characters in brief: {cjk}")
    raise ValueError(f"unknown auto assertion: {text}")


def main(run_root, iteration, configs=("with_skill=with_skill", "without_skill=without_skill")):
    run_root, iteration = Path(run_root), Path(iteration)
    evals = json.load(open(SKILL / "evals/evals.json"))["evals"]
    judgments = json.load(open(iteration / "judgments.json"))
    for e in evals:
        fixture = SKILL / e["files"][0]
        eval_dir = iteration / f"eval-{e['id']}-{e['name']}"
        eval_dir.mkdir(parents=True, exist_ok=True)
        json.dump({"eval_id": e["id"], "eval_name": e["name"], "prompt": e["prompt"],
                   "assertions": e["expectations"]}, open(eval_dir / "eval_metadata.json", "w"),
                  ensure_ascii=False, indent=2)
        for pair in configs:
            cfg, src = pair.split("=")
            ws = run_root / f"{e['id']:02d}-{e['name']}" / src / "ws"
            run = eval_dir / cfg / "run-1"
            outputs = run / "outputs"
            shutil.rmtree(outputs, ignore_errors=True)
            outputs.mkdir(parents=True)
            sess = session_for(ws)
            final, tokens, secs, tools = read_session(sess) if sess else ("", 0, None, {})
            (outputs / "response.md").write_text(final)
            changed = changed_files(fixture, ws)
            for rel in changed:
                dst = outputs / "workspace" / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ws / rel, dst)
            new_briefs = [r for r in changed if str(r).startswith("local/briefs/")]
            manual = iter(judgments[f"{e['id']}/{cfg}"])
            exps = []
            for a in e["expectations"]:
                if a.startswith("[auto]"):
                    ok, ev = auto(a, fixture, ws, new_briefs, final)
                else:
                    ok, ev = next(manual)
                exps.append({"text": a, "passed": bool(ok), "evidence": ev})
            passed = sum(x["passed"] for x in exps)
            json.dump({"expectations": exps,
                       "summary": {"passed": passed, "failed": len(exps) - passed, "total": len(exps),
                                   "pass_rate": round(passed / len(exps), 2)},
                       "execution_metrics": {"tool_calls": tools, "total_tool_calls": sum(tools.values()),
                                             "output_chars": len(final)}},
                      open(run / "grading.json", "w"), ensure_ascii=False, indent=2)
            json.dump({"total_tokens": tokens, "total_duration_seconds": secs,
                       "session": str(sess) if sess else None},
                      open(run / "timing.json", "w"), indent=2)
            print(f"eval-{e['id']:<2} {cfg:<13} {passed}/{len(exps)}  tokens={tokens} secs={secs}")


def fix_benchmark(iteration, model):
    """aggregate_benchmark 写死了模型名和 3 runs，这里按实际情况改正。"""
    iteration = Path(iteration)
    b = json.load(open(iteration / "benchmark.json"))
    b["metadata"].update(executor_model=model, analyzer_model="main session (manual judgments)",
                         runs_per_configuration=1)
    json.dump(b, open(iteration / "benchmark.json", "w"), ensure_ascii=False, indent=2)
    md = (iteration / "benchmark.md").read_text()
    md = md.replace("<model-name>", model).replace("3 runs each", "1 run each")
    (iteration / "benchmark.md").write_text(md)


if __name__ == "__main__":
    if sys.argv[1] == "--fix-benchmark":
        fix_benchmark(sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], *([sys.argv[3:]] if len(sys.argv) > 3 else []))
