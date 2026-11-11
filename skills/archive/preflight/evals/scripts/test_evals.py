"""Local runner/grader regressions; no model requests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import run_evals as runner
import grade_evals as grader


def events(texts, stop="stop"):
    return json.dumps({"type": "message_end", "message": {
        "role": "assistant", "stopReason": stop,
        "content": [{"type": "text", "text": t} for t in texts],
        "usage": {"totalTokens": 42}}}) + "\n"


class EvalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.case = {"id": 99, "name": "regression", "fixture": "empty",
                     "explicit": False, "prompt": "hello", "expectations": ["one", "two"]}
        self.run = self.root / "eval-99-regression" / "without_skill" / "run-1"

    def completed(self, stdout="", returncode=0, stderr=""):
        return subprocess.CompletedProcess([], returncode, stdout, stderr)

    def invoke_runner(self, result):
        with patch.object(runner.subprocess, "run", return_value=result):
            return runner.run_one(self.case, "without_skill", self.root, "test-model")

    def seed_grade(self):
        (self.run / "outputs").mkdir(parents=True)
        (self.run / "outputs/response.md").write_text("answer")
        for name, value in {"changes.json": {"changed": [], "deleted": []},
                            "timing.json": {"total_duration_seconds": 1},
                            "metrics.json": {},
                            "status.json": {"status": "success"}}.items():
            (self.run / name).write_text(json.dumps(value))

    def invoke_grade(self, result):
        with patch.object(grader.subprocess, "run", return_value=result):
            return grader.grade(self.run, self.case, "test-grader")

    def test_failed_process_is_not_a_completed_run(self):
        self.invoke_runner(self.completed(returncode=1, stderr="provider unavailable"))
        self.assertFalse((self.run / "outputs/response.md").exists())
        self.assertEqual(json.loads((self.run / "status.json").read_text())["status"], "failed")
        self.assertIn("provider unavailable", (self.run / "stderr.log").read_text())

    def test_legacy_response_does_not_block_retry(self):
        (self.run / "outputs").mkdir(parents=True)
        (self.run / "outputs/response.md").write_text("(no final text)")
        self.invoke_runner(self.completed(events(["recovered"])))
        self.assertEqual((self.run / "outputs/response.md").read_text(), "recovered")

    def test_final_response_preserves_all_text_blocks(self):
        self.invoke_runner(self.completed(events(["first", "second"])))
        self.assertEqual((self.run / "outputs/response.md").read_text(), "first\n\nsecond")

    def test_nested_artifacts_and_deleted_files_are_preserved(self):
        def modify_workspace(args, **kwargs):
            ws = Path(kwargs["cwd"])
            (ws / ".keep").unlink()
            (ws / "a").mkdir()
            (ws / "a/b.txt").write_text("nested")
            (ws / "a__b.txt").write_text("flat")
            return self.completed(events(["done"]))
        with patch.object(runner.subprocess, "run", side_effect=modify_workspace):
            runner.run_one(self.case, "without_skill", self.root, "test-model")
        changes = json.loads((self.run / "changes.json").read_text())
        self.assertEqual(changes["changed"], ["a/b.txt", "a__b.txt"])
        self.assertEqual(changes["deleted"], [".keep"])
        self.assertEqual((self.run / "outputs/files/a/b.txt").read_text(), "nested")
        self.assertEqual((self.run / "outputs/files/a__b.txt").read_text(), "flat")

    def test_executor_keeps_tool_evidence_past_800_characters(self):
        tool_result = json.dumps({"type": "message_end", "message": {"role": "toolResult", "content": [
            {"type": "text", "text": "x" * 1500 + "TAIL_EVIDENCE"}]}}) + "\n"
        self.invoke_runner(self.completed(tool_result + events(["done"])))
        self.assertIn("TAIL_EVIDENCE", (self.run / "transcript.md").read_text())

    def test_error_message_with_exit_zero_is_not_success(self):
        self.invoke_runner(self.completed(events(["partial"], stop="error")))
        self.assertFalse((self.run / "outputs/response.md").exists())

    def test_baseline_strips_bare_skill_command_in_history(self):
        self.case["prompt"] = "History:\n/skill:preflight\nLatest: hello"
        with patch.object(runner.subprocess, "run", return_value=self.completed(events(["ok"]))) as run:
            runner.run_one(self.case, "without_skill", self.root, "test-model")
        self.assertNotIn("/skill:preflight", run.call_args.args[0][-1])

    def test_successful_run_resumes_without_model_call(self):
        self.invoke_runner(self.completed(events(["done"])))
        with patch.object(runner.subprocess, "run") as call:
            _, _, message = runner.run_one(self.case, "without_skill", self.root, "test-model")
        self.assertEqual(message, "skip")
        call.assert_not_called()

    def test_changed_input_cannot_reuse_successful_run(self):
        self.invoke_runner(self.completed(events(["done"])))
        self.case["prompt"] = "different task"
        with patch.object(runner.subprocess, "run") as call:
            _, _, message = runner.run_one(self.case, "without_skill", self.root, "test-model")
        self.assertIn("FAILED", message)
        call.assert_not_called()

    def test_runner_timeout_is_failed_and_retryable(self):
        with patch.object(runner.subprocess, "run", side_effect=subprocess.TimeoutExpired("pi", 1, output=b"partial")):
            _, _, message = runner.run_one(self.case, "without_skill", self.root, "test-model")
        self.assertIn("FAILED", message)
        self.assertEqual((self.run / "events.jsonl").read_text(), "partial")
        self.invoke_runner(self.completed(events(["recovered"])))
        self.assertEqual((self.run / "outputs/response.md").read_text(), "recovered")

    def test_grader_rejects_missing_expectation(self):
        self.seed_grade()
        result = json.dumps({"expectations": [{"text": "one", "passed": True, "evidence": "answer"}]})
        self.invoke_grade(self.completed(result))
        self.assertFalse((self.run / "grading.json").exists())

    def test_grader_rejects_string_boolean(self):
        self.seed_grade()
        result = json.dumps({"expectations": [{"text": e, "passed": "false", "evidence": "answer"}
                                              for e in self.case["expectations"]]})
        self.invoke_grade(self.completed(result))
        self.assertFalse((self.run / "grading.json").exists())

    def test_grader_does_not_accept_output_from_failed_process(self):
        self.seed_grade()
        result = json.dumps({"expectations": [{"text": e, "passed": True, "evidence": "answer"}
                                              for e in self.case["expectations"]]})
        self.invoke_grade(self.completed(result, returncode=1, stderr="provider failed"))
        self.assertFalse((self.run / "grading.json").exists())

    def test_grader_timeout_does_not_crash_batch(self):
        self.seed_grade()
        with patch.object(grader.subprocess, "run", side_effect=subprocess.TimeoutExpired("pi", 1)):
            _, msg = grader.grade(self.run, self.case, "test-grader")
        self.assertIn("FAILED", msg)

    def test_grader_receives_full_file_and_transcript(self):
        self.seed_grade()
        large = "x" * 13000 + "EVIDENCE_AT_END"
        (self.run / "transcript.md").write_text(large)
        (self.run / "workspace-after").mkdir()
        (self.run / "workspace-after/plan.md").write_text(large)
        (self.run / "changes.json").write_text(json.dumps({"changed": ["plan.md"], "deleted": []}))
        valid = {"expectations": [{"text": e, "passed": True, "evidence": "EVIDENCE_AT_END"}
                                   for e in self.case["expectations"]]}
        def inspect_prompt(args, **kwargs):
            prompt = Path(args[-1][1:]).read_text()
            self.assertEqual(prompt.count("EVIDENCE_AT_END"), 2)
            return self.completed(json.dumps(valid))
        with patch.object(grader.subprocess, "run", side_effect=inspect_prompt):
            grader.grade(self.run, self.case, "test-grader")
        self.assertTrue((self.run / "grading.json").exists())

    def test_snapshot_excludes_installed_dependencies_but_keeps_lockfile(self):
        (self.root / "node_modules").mkdir()
        (self.root / "node_modules/binary.node").write_bytes(b"\xff" * 100)
        (self.root / "package-lock.json").write_text("{}")
        self.assertEqual(set(runner.snapshot(self.root)), {"package-lock.json"})

    def test_grader_excludes_dependency_contents_from_legacy_runs(self):
        self.seed_grade()
        (self.run / "changes.json").write_text(json.dumps({"changed": ["node_modules/missing.node"], "deleted": []}))
        valid = {"expectations": [{"text": e, "passed": True, "evidence": "answer"}
                                   for e in self.case["expectations"]]}
        self.invoke_grade(self.completed(json.dumps(valid)))
        evidence = json.loads((self.run / "grading-input.json").read_text())
        self.assertEqual(evidence["EXCLUDED_GENERATED_FILE_COUNT_IN_RAW_MANIFEST"], 1)
        self.assertEqual(evidence["FILE_CONTENTS"], {})
        self.assertTrue((self.run / "grading.json").exists())

    def test_grader_sends_binary_files_as_metadata_not_text(self):
        self.seed_grade()
        (self.run / "workspace-after").mkdir()
        (self.run / "workspace-after/deck.pptx").write_bytes(b"PK\x03\x04" + b"\x00\xff" * 50000)
        (self.run / "workspace-after/notes.md").write_text("plain notes")
        (self.run / "changes.json").write_text(json.dumps({"changed": ["deck.pptx", "notes.md"], "deleted": []}))
        valid = {"expectations": [{"text": e, "passed": True, "evidence": "answer"}
                                   for e in self.case["expectations"]]}
        self.invoke_grade(self.completed(json.dumps(valid)))
        files = json.loads((self.run / "grading-input.json").read_text())["FILE_CONTENTS"]
        self.assertEqual(files["notes.md"], "plain notes")
        self.assertIn("binary file", files["deck.pptx"])
        self.assertIn("100004 bytes", files["deck.pptx"])
        self.assertLess(len(files["deck.pptx"]), 300)

    def test_grader_does_not_grade_failed_execution(self):
        self.seed_grade()
        (self.run / "status.json").write_text(json.dumps({"status": "failed"}))
        with patch.object(grader.subprocess, "run") as call:
            _, message = grader.grade(self.run, self.case, "test-grader")
        self.assertIn("FAILED", message)
        call.assert_not_called()

    def test_valid_grade_counts_exact_expectations(self):
        self.seed_grade()
        result = json.dumps({"expectations": [
            {"text": "one", "passed": True, "evidence": "answer"},
            {"text": "two", "passed": False, "evidence": "not present"}]})
        self.invoke_grade(self.completed(result))
        grade = json.loads((self.run / "grading.json").read_text())
        self.assertEqual(grade["summary"], {"passed": 1, "failed": 1, "total": 2, "pass_rate": .5})


if __name__ == "__main__":
    unittest.main()
