import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { LADDER_HEADER, OPTIONAL, REQUIRED, TRIALS, checkReq } from "./check-req.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const CLI = path.join(here, "check-req.mjs");

// 一份合法需求文档：中文内容 + 英文标题，三个下游技能都跑过，含一条试跑记录
const VALID = `# Requirement: 登录链路不再卡住或白屏

- Source: "修一下登录页偶尔白屏的 bug"
- Date: 2026-11-08

## Requirement

用户从打开 App 到登录成功，不再卡住或白屏；先定位根因，再改。

## Ladder

| Rung | Goal | AI owns | Needs | Status |
|---|---|---|---|---|
| 0 | 修一下登录页偶尔白屏的 bug | | | |
| 1 | 登录页每次都能正常打开 | 复现与定位 | 前端错误日志 | rejected |
| 2 | 用户从打开 App 到登录成功不再卡住或白屏 | 整条登录链路的稳定性 | 前端日志、/api/session 监控 | handed |

Handed over: rung 2

## Deeper

- Premise: holds
- Kept: 先区分 fetch 挂起、401 返回非 JSON、mount 前报错三种失败
- Dropped: 压测，用户说流量不大

## Wider

- Noun → verb: 登录页 → 让回访用户三秒内回到上次的位置
- Borrowed: 游戏存档：断点续玩
  进入时直接回到上次状态
- Dropped: 机场值机：用户说场景不像

## Trials

### 2026-11-08 · rung 1 · rejected
- Fell short: 只加了 loading 骨架屏，白屏的真正原因没找到。
`;

const rules = (text, file) => checkReq(text, file).problems.map((p) => p.rule);
const swap = (from, to) => {
  assert.ok(VALID.includes(from), `fixture lacks: ${from}`);
  return VALID.replace(from, to);
};

test("accepts the documented template filled in", () => {
  assert.deepEqual(checkReq(VALID, "docs/reqs/login-stability.md").problems, []);
});

test("accepts a requirement with only higher run and no trials yet", () => {
  const text = VALID.replace(/## Deeper[\s\S]*$/, "## Trials\n").replace("| rejected |", "| |");
  assert.deepEqual(checkReq(text).problems, []);
});

test("accepts an accepted handed rung", () => {
  assert.deepEqual(rules(swap("| handed |", "| accepted |")), []);
});

test("rejects a missing title", () => {
  assert.ok(rules(swap("# Requirement: ", "# ")).includes("title"));
});

test("rejects missing or malformed metadata", () => {
  assert.ok(rules(VALID.replace(/- Source: .*\n/, "")).includes("meta"));
  assert.ok(rules(swap("Date: 2026-11-08", "Date: 11/08")).includes("date"));
});

test("rejects missing, unknown, duplicate and out-of-order sections", () => {
  assert.ok(rules(VALID.replace(/## Trials[\s\S]*$/, "")).includes("missing"));
  assert.ok(rules(swap("## Wider", "## Notes")).includes("section"));
  assert.ok(rules(`${VALID}\n## Deeper\n- Premise: holds\n`).includes("section"));
  const deeper = VALID.match(/## Deeper\n[\s\S]*?(?=## Wider)/)[0];
  assert.ok(rules(VALID.replace(deeper, "").replace("## Trials", `${deeper}## Trials`)).includes("order"));
});

test("rejects an empty requirement", () => {
  assert.ok(rules(swap("用户从打开 App 到登录成功，不再卡住或白屏；先定位根因，再改。\n", "")).includes("empty"));
});

test("rejects a broken ladder table", () => {
  assert.ok(rules(swap("| Rung | Goal | AI owns | Needs | Status |", "| Rung | Goal | Status |")).includes("ladder"));
  assert.ok(rules(swap("| 2 | 用户从", "| 3 | 用户从")).includes("rung"));
  assert.ok(rules(swap("| 0 | 修一下登录页偶尔白屏的 bug | | | |", "| 0 | 修一下登录页偶尔白屏的 bug | AI | | |")).includes("ladder"));
  assert.ok(rules(swap("| handed |", "| maybe |")).includes("status"));
});

test("rejects a handed line that disagrees with the table", () => {
  assert.ok(rules(swap("Handed over: rung 2", "Handed over: rung 1")).includes("handed"));
  assert.ok(rules(swap("Handed over: rung 2", "")).includes("handed"));
  assert.ok(rules(swap("| rejected |", "| handed |")).includes("handed"));
});

test("rejects prose in the ladder", () => {
  assert.ok(rules(swap("Handed over: rung 2", "Handed over: rung 2\n先交这层。")).includes("prose"));
});

test("rejects bad Deeper and Wider fields", () => {
  assert.ok(rules(swap("- Premise: holds\n", "")).includes("field"));
  assert.ok(rules(swap("- Kept: 先区分", "- Maybe: 先区分")).includes("field"));
  assert.ok(rules(swap("- Noun → verb:", "Noun → verb:")).includes("prose"));
  assert.ok(rules(swap("- Premise: holds\n- Kept: 先区分", "- Kept: 先区分")).includes("field"));
});

test("rejects bad trial entries", () => {
  assert.ok(rules(swap("### 2026-11-08 · rung 1 · rejected", "### rung 1 rejected")).includes("trial"));
  assert.ok(rules(swap("· rung 1 · rejected", "· rung 1 · meh")).includes("trial"));
  assert.ok(rules(swap("· rung 1 · rejected", "· rung 9 · rejected")).includes("trial"));
  assert.ok(rules(VALID.replace(/- Fell short: .*\n/, "")).includes("trial"));
  assert.ok(rules(swap("### 2026-11-08 · rung 1 · rejected\n", "")).includes("prose"));
});

test("rejects template placeholders left behind", () => {
  assert.ok(rules(swap("Handed over: rung 2", "Handed over: rung <N>")).includes("placeholder"));
  assert.ok(rules(swap("- Premise: holds", "- Premise: <holds | moved, handed to /higher>")).includes("placeholder"));
  assert.ok(rules(swap("- Fell short: 只加了", "- Fell short: <what the user said fell short>")).includes("placeholder"));
  assert.ok(rules(swap("- Kept: 先区分", "<!-- note -->\n- Kept: 先区分")).includes("placeholder"));
});

test("rejects stray headings", () => {
  assert.ok(rules(swap("## Requirement\n", "## Requirement\n### Sub\n")).includes("heading"));
});

test("checks file name and location", () => {
  assert.ok(rules(VALID, "docs/reqs/Login Stability.md").includes("slug"));
  assert.ok(rules(VALID, "ladders/login-stability.md").includes("location"));
});

test("CLI exits 0 on a valid requirement, 1 on problems, 2 with nothing to check", (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "check-req-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const run = (args) => spawnSync(process.execPath, [CLI, ...args], { cwd: root, encoding: "utf8" });

  assert.equal(run([]).status, 2);
  fs.mkdirSync(path.join(root, "docs", "reqs"), { recursive: true });
  fs.writeFileSync(path.join(root, "docs", "reqs", "good-req.md"), VALID);
  assert.equal(run([]).status, 0);
  fs.writeFileSync(path.join(root, "docs", "reqs", "bad-req.md"), VALID.replace("Date: 2026-11-08", "Date: x"));
  const bad = run([]);
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /bad-req\.md:4: .*\[date\]/);
});

test("SKILL.md template matches the checker", () => {
  // 防止 SKILL.md 模板和脚本常量各改各的
  const skill = fs.readFileSync(path.join(here, "../SKILL.md"), "utf8");
  const template = skill.match(/```markdown\n(# Requirement:[\s\S]*?)\n```/)[1];
  const headings = [...template.matchAll(/^## (.+)$/gm)].map((m) => m[1]);
  assert.deepEqual(headings, [...REQUIRED, ...OPTIONAL, TRIALS]);
  assert.match(template, new RegExp(`^\\| ${LADDER_HEADER.join(" \\| ")} \\|$`, "m"));
  // 模板里每个占位都要被脚本认成占位
  const filled = checkReq(template).problems.filter((p) => p.rule === "placeholder").length;
  assert.ok(filled >= 10, `only ${filled} placeholder lines recognised`);
});
