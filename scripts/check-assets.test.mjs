import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { checkAssets, parseFrontmatter } from "./check-assets.mjs";

const SKILL = (name, { user = false } = {}) =>
  `---\nname: ${name}\ndescription: does one thing\n${user ? "disable-model-invocation: true\n" : ""}---\n\n# ${name}\n`;

const TARGETS = (pi = [], claude = []) => `${JSON.stringify({ pi, claude }, null, 2)}\n`;

function library(t, files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "check-assets-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  for (const [rel, content] of Object.entries(files)) {
    const target = path.join(root, rel);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, content);
  }
  return root;
}

const README =
  "## User-invoked\n\n- **[alpha](./skills/plan/alpha/SKILL.md)**: first.\n\n## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n";

test("a consistent library has no problems", (t) => {
  const root = library(t, {
    "README.md": README,
    "targets.json": TARGETS(["alpha", "beta"]),
    "skills/plan/alpha/SKILL.md": SKILL("alpha", { user: true }),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  assert.deepEqual(checkAssets(root), []);
});

test("scenes may differ per skill, and one skill may go to both harnesses", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[alpha](./skills/plan/alpha/SKILL.md)**: first.\n- **[beta](./skills/verify/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["alpha", "beta"], ["beta"]),
    "skills/plan/alpha/SKILL.md": SKILL("alpha"),
    "skills/verify/beta/SKILL.md": SKILL("beta"),
  });
  assert.deepEqual(checkAssets(root), []);
});

test("an archived skill is consistent when nothing publishes it", (t) => {
  const root = library(t, {
    "README.md":
      "## Model-invoked\n\n- **[alpha](./skills/plan/alpha/SKILL.md)**: first.\n\n## Archived\n\n- **[old](./skills/archive/old/SKILL.md)**: retired.\n",
    "targets.json": TARGETS(["alpha"]),
    "skills/plan/alpha/SKILL.md": SKILL("alpha"),
    "skills/archive/old/SKILL.md": SKILL("old"),
  });
  assert.deepEqual(checkAssets(root), []);
});

test("a missing root README is reported", (t) => {
  const root = library(t, { "skills/plan/beta/SKILL.md": SKILL("beta") });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["root-readme-missing"]);
});

test("an entry with no matching skill is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n- **[ghost](./skills/plan/ghost/SKILL.md)**: gone.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["index-entry-unresolved"]);
});

test("an entry pointing at the wrong scene is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/verify/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "index-scene-mismatch");
  assert.match(problem.message, /skills\/plan\/beta/);
});

test("a skill missing from the index is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta", "gamma"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
    "skills/plan/gamma/SKILL.md": SKILL("gamma"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["skill-not-indexed"]);
});

test("frontmatter name must equal the directory name", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("renamed"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["frontmatter-name-mismatch"]);
});

test("invocation must agree between index and frontmatter", (t) => {
  const root = library(t, {
    "README.md": "## User-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "invocation-mismatch");
  assert.match(problem.message, /user-invoked/);
});

test("an entry outside both invocation headings is reported", (t) => {
  const root = library(t, {
    "README.md": "# title\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["invocation-undeclared"]);
});

test("a directory without SKILL.md is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
    "skills/archive/half-written/notes.md": "work in progress\n",
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["skill-no-skill-md"]);
});

test("a loose file directly in skills/ is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
    "skills/README.md": "leftover bucket index\n",
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["skills-stray-file"]);
});

test("a loose file in a scene directory is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
    "skills/plan/notes.md": "scene notes\n",
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["scene-stray-file"]);
});

test("entries out of alphabetical order are reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n- **[alpha](./skills/plan/alpha/SKILL.md)**: first.\n",
    "targets.json": TARGETS(["alpha", "beta"]),
    "skills/plan/alpha/SKILL.md": SKILL("alpha"),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["index-order"]);
});

// `targets.json` decides what is published, and the archive is the complement.
const BASE_FILES = {
  "README.md": "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n",
  "skills/plan/beta/SKILL.md": SKILL("beta"),
};

test("a missing targets.json is reported", (t) => {
  const root = library(t, BASE_FILES);
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["targets-missing"]);
});

test("a scene skill in no target list is reported", (t) => {
  const root = library(t, {
    "README.md":
      "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n- **[gamma](./skills/plan/gamma/SKILL.md)**: third.\n",
    "targets.json": TARGETS(["beta"]),
    "skills/plan/beta/SKILL.md": SKILL("beta"),
    "skills/plan/gamma/SKILL.md": SKILL("gamma"),
  });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "targets-unlisted");
  assert.match(problem.message, /gamma/);
});

test("a target name with no skill is reported", (t) => {
  const root = library(t, { ...BASE_FILES, "targets.json": TARGETS(["beta", "ghost"]) });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["targets-unknown-skill"]);
});

test("publishing an archived skill is reported", (t) => {
  const root = library(t, {
    "README.md": "## Archived\n\n- **[old](./skills/archive/old/SKILL.md)**: retired.\n",
    "targets.json": TARGETS(["old"]),
    "skills/archive/old/SKILL.md": SKILL("old"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["targets-archived-skill"]);
});

test("an archived skill listed as model-invoked is reported", (t) => {
  const root = library(t, {
    "README.md": "## Model-invoked\n\n- **[old](./skills/archive/old/SKILL.md)**: retired.\n",
    "targets.json": TARGETS([]),
    "skills/archive/old/SKILL.md": SKILL("old"),
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["index-archived-mismatch"]);
});

test("a name listed for both harnesses twice is reported", (t) => {
  const root = library(t, { ...BASE_FILES, "targets.json": TARGETS(["beta"], ["beta", "beta"]) });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["targets-duplicate"]);
});

test("invalid targets JSON is reported", (t) => {
  const root = library(t, { ...BASE_FILES, "targets.json": "{ pi: [\n" });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.deepEqual(rules, ["targets-invalid"]);
});

test("frontmatter parsing reads block scalars", () => {
  const fields = parseFrontmatter("---\nname: x\ndescription: |\n  line one\n  line two\n---\n");
  assert.equal(fields.name, "x");
  assert.equal(fields.description, "line one");
});

test("frontmatter parsing rejects a missing block", () => {
  assert.equal(parseFrontmatter("# no frontmatter\n"), null);
  assert.equal(parseFrontmatter("---\nname: x\n"), null);
});

// The farms are the only materialization of targets.json, so they are checked when they exist.
function farm(t, files, links) {
  const root = library(t, files);
  for (const farmName of ["skills-pi", "skills-claude"]) fs.mkdirSync(path.join(root, farmName), { recursive: true });
  for (const [rel, target] of Object.entries(links)) fs.symlinkSync(target, path.join(root, rel));
  return root;
}

const FARM_BASE = {
  "README.md":
    "## Model-invoked\n\n- **[beta](./skills/plan/beta/SKILL.md)**: second.\n- **[other](./skills/verify/other/SKILL.md)**: third.\n",
  "targets.json": TARGETS(["beta"], ["other"]),
  "skills/plan/beta/SKILL.md": SKILL("beta"),
  "skills/verify/other/SKILL.md": SKILL("other"),
};

test("a populated pair of farms has no problems", (t) => {
  const root = farm(t, FARM_BASE, {
    "skills-pi/beta": "../skills/plan/beta",
    "skills-claude/other": "../skills/verify/other",
  });
  assert.deepEqual(checkAssets(root), []);
});

test("a skill in the pool with no link is reported", (t) => {
  const root = farm(t, FARM_BASE, { "skills-claude/other": "../skills/verify/other" });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "target-link-missing");
  assert.match(problem.message, /beta/);
});

test("a link that targets.json does not list is reported", (t) => {
  const root = farm(t, FARM_BASE, {
    "skills-pi/beta": "../skills/plan/beta",
    "skills-pi/other": "../skills/verify/other",
    "skills-claude/other": "../skills/verify/other",
  });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "target-link-extra");
  assert.match(problem.message, /other/);
});

test("a link pointing at the wrong directory is reported", (t) => {
  const root = farm(t, FARM_BASE, {
    "skills-pi/beta": "../skills/verify/other",
    "skills-claude/other": "../skills/verify/other",
  });
  const [problem] = checkAssets(root);
  assert.equal(problem.rule, "target-link-wrong");
  assert.match(problem.message, /skills\/plan\/beta/);
});

test("a real file inside a farm is reported", (t) => {
  const root = farm(t, { ...FARM_BASE, "skills-pi/notes.md": "hand edited\n" }, {
    "skills-claude/other": "../skills/verify/other",
  });
  const rules = checkAssets(root).map((problem) => problem.rule);
  assert.ok(rules.includes("target-link-not-symlink"));
});
