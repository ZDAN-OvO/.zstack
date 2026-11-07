import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { OPTIONAL, SLOTS, STAGES, checkBrief } from "./check-brief.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const CLI = path.join(here, "check-brief.mjs");

// 一份合法 brief：中文内容 + 英文标题，含可选栏与 bullet 内的代码块
const VALID = `# Brief: 下季产品方向的竞品分析

- Stage: execute
- Source: "帮我做一份竞品分析"，补充了决策目标和客群

## Goal
- 支撑下季产品方向决策：USP 往更好用走还是更便宜走，给明确建议和理由。

## Context
- 年营收约 200 万美元的营销自动化 SaaS，客户为 50 人以下公司。
- 客户常嫌复杂、嫌贵；去年调价反响不好。

## Materials
- 三家竞品官网与产品文档。
- 不用二手评论文章；查不到就留白并标注 not found。

## Boundaries
- 不编造 ARR、用户数、增长率。
- 不动付费等级架构，定价定位可以讨论。

## Done
- 先交 Markdown outline：
  \`\`\`text
  关键差异 / 建议 USP / 判断逻辑
  \`\`\`
- 审过后再写完整报告。

## Assumptions
- 竞品名单由 agent 按客群重叠度选出，用户可否决。
`;

const rules = (text, file) => checkBrief(text, file).problems.map((p) => p.rule);

test("accepts the documented template filled in", () => {
  assert.deepEqual(checkBrief(VALID, "docs/briefs/competitor-usp-direction.md").problems, []);
});

test("accepts a brief without optional sections", () => {
  assert.deepEqual(rules(VALID.replace(/\n## Assumptions[\s\S]*$/, "\n")), []);
});

test("rejects a missing title", () => {
  assert.ok(rules(VALID.replace("# Brief: ", "# ")).includes("title"));
});

test("rejects an unknown stage", () => {
  assert.ok(rules(VALID.replace("Stage: execute", "Stage: build")).includes("stage"));
});

test("rejects missing Source metadata", () => {
  assert.ok(rules(VALID.replace(/- Source: .*\n/, "")).includes("meta"));
});

test("rejects a missing slot", () => {
  const text = VALID.replace(/## Materials\n[\s\S]*?(?=## Boundaries)/, "");
  assert.ok(rules(text).includes("missing"));
});

test("rejects slots out of order", () => {
  const goal = VALID.match(/## Goal\n[\s\S]*?(?=## Context)/)[0];
  const text = VALID.replace(goal, "").replace("## Done", `${goal}## Done`);
  assert.ok(rules(text).includes("order"));
});

test("rejects unknown and duplicate sections", () => {
  assert.ok(rules(VALID.replace("## Assumptions", "## Notes")).includes("section"));
  assert.ok(rules(`${VALID}\n## Goal\n- again\n`).includes("section"));
});

test("rejects prose instead of bullets", () => {
  assert.ok(rules(VALID.replace("- 支撑下季", "支撑下季")).includes("prose"));
});

test("rejects an empty optional section", () => {
  assert.ok(rules(VALID.replace(/- 竞品名单.*\n/, "")).includes("empty"));
});

test("rejects more than five bullets in a slot", () => {
  const extra = "- 补充\n".repeat(5);
  assert.ok(rules(VALID.replace("## Context\n", `## Context\n${extra}`)).includes("length"));
});

test("rejects template placeholders left behind", () => {
  assert.ok(rules(VALID.replace("- 竞品名单", "<!-- Defaulted slots -->\n- 竞品名单")).includes("placeholder"));
  assert.ok(rules(VALID.replace("Stage: execute", "Stage: <think | explore | decide | execute>")).includes("placeholder"));
});

test("rejects headings below H2", () => {
  assert.ok(rules(VALID.replace("## Context\n", "## Context\n### Sub\n")).includes("heading"));
});

test("checks file name and location", () => {
  assert.ok(rules(VALID, "docs/briefs/Competitor USP.md").includes("slug"));
  assert.ok(rules(VALID, "notes/competitor-usp.md").includes("location"));
});

test("CLI exits 0 on a valid brief, 1 on problems, 2 with nothing to check", (t) => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "check-brief-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const run = (args) => spawnSync(process.execPath, [CLI, ...args], { cwd: root, encoding: "utf8" });

  assert.equal(run([]).status, 2);
  fs.mkdirSync(path.join(root, "docs", "briefs"), { recursive: true });
  fs.writeFileSync(path.join(root, "docs", "briefs", "good-brief.md"), VALID);
  assert.equal(run([]).status, 0);
  fs.writeFileSync(path.join(root, "docs", "briefs", "bad-brief.md"), VALID.replace("Stage: execute", "Stage: x"));
  const bad = run([]);
  assert.equal(bad.status, 1);
  assert.match(bad.stdout, /bad-brief\.md:3: .*\[stage\]/);
});

test("SKILL.md template headings match the checker's slots", () => {
  // 防止 SKILL.md 模板和脚本常量各改各的
  const skill = fs.readFileSync(path.join(here, "../SKILL.md"), "utf8");
  const template = skill.match(/```markdown\n(# Brief:[\s\S]*?)\n```/)[1];
  const headings = [...template.matchAll(/^## (.+)$/gm)].map((m) => m[1]);
  assert.deepEqual(headings, [...SLOTS, ...OPTIONAL]);
  assert.match(template, new RegExp(`Stage: <${STAGES.join(" \\| ")}>`));
});
