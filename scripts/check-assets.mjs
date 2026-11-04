#!/usr/bin/env node
// Validate the skill library: the `skills/<scene>/<skill>/SKILL.md` layout, targets.json, the two
// per-harness link farms, the root index, and SKILL.md frontmatter.
// Zero dependencies, so CI needs no install step.
// Usage: node scripts/check-assets.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

/** Parse the top-level keys of a `---` delimited frontmatter block. */
export function parseFrontmatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") return null;
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") {
      end = i;
      break;
    }
  }
  if (end < 0) return null;

  const fields = {};
  let key = null;
  for (let i = 1; i < end; i++) {
    const line = lines[i];
    const match = /^([A-Za-z0-9_-]+):(.*)$/.exec(line);
    if (match) {
      key = match[1];
      const value = match[2].trim();
      fields[key] = /^[|>][-+]?$/.test(value) ? "" : value;
    } else if (key && fields[key] === "" && line.trim() !== "") {
      fields[key] = line.trim();
    }
  }
  return fields;
}

// `targets.json` is the one source of truth for which harness gets which skill, and the two
// farms are its only materialization: one symlink per skill, pointing into `skills/`.
const TARGETS = "targets.json";
const FARMS = { pi: "skills-pi", claude: "skills-claude" };
// A bucket, not a scene: kept in the repo, published to no harness.
const ARCHIVE = "archive";

// The root README is the only index. Every entry links `./skills/<scene>/<skill>/SKILL.md`, and
// its section decides whether the skill is user-invoked, model-invoked, or archived.
const ENTRY = /\]\(\.\/skills\/([^/)\s]+)\/([^/)\s]+)\/SKILL\.md\)/;

function declaredSection(title) {
  const text = title.trim().toLowerCase();
  if (text.includes("user-invoked")) return "user";
  if (text.includes("model-invoked")) return "model";
  if (text.startsWith("archived")) return ARCHIVE;
  return null;
}

function indexEntries(readme) {
  const entries = [];
  let declared = null;
  readme.split(/\r?\n/).forEach((line, i) => {
    const heading = /^##\s+(.*)$/.exec(line);
    if (heading) {
      declared = declaredSection(heading[1]);
      return;
    }
    const match = ENTRY.exec(line);
    if (!match) return;
    entries.push({ scene: match[1], name: match[2], declared, lineNo: i + 1 });
  });
  return entries;
}

function dirs(dir) {
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

/** Every skill on disk, read from `skills/<scene>/<name>/`: `{ name, scene, isArchive, rel }`. */
function librarySkills(skillsDir) {
  const skills = [];
  if (!fs.existsSync(skillsDir)) return skills;
  for (const scene of dirs(skillsDir)) {
    for (const name of dirs(path.join(skillsDir, scene))) {
      skills.push({ name, scene, isArchive: scene === ARCHIVE, rel: `skills/${scene}/${name}/SKILL.md` });
    }
  }
  return skills;
}

function checkFrontmatter(fail, rel, name, text) {
  const fields = parseFrontmatter(text);
  if (fields === null) {
    fail("frontmatter-invalid", rel, "no `---` delimited frontmatter block at the top of the file");
    return;
  }
  if (fields.name !== name) {
    fail("frontmatter-name-mismatch", rel, `name is "${fields.name ?? ""}", directory is "${name}"`);
  }
  if (!(fields.description ?? "").trim()) fail("frontmatter-description-missing", rel, "description is empty");
}

/** Each farm is exactly the links targets.json asks for, and nothing else. */
function checkFarms(fail, root, skillsDir, targets, onDisk) {
  // A root without farms is a fixture or a checkout that never published; only judge a farm that exists.
  if (!Object.values(FARMS).some((farm) => fs.existsSync(path.join(root, farm)))) return;

  for (const [pool, farmName] of Object.entries(FARMS)) {
    const farmDir = path.join(root, farmName);
    const wanted = new Set(targets[pool] ?? []);
    if (!fs.existsSync(farmDir)) {
      fail("target-farm-missing", farmName, `no ${farmName}/ directory; run scripts/link-skills.mjs`);
      continue;
    }
    const present = new Set();
    for (const entry of fs.readdirSync(farmDir, { withFileTypes: true })) {
      present.add(entry.name);
      const link = path.join(farmDir, entry.name);
      if (!entry.isSymbolicLink()) {
        fail("target-link-not-symlink", `${farmName}/${entry.name}`, "a farm holds only symlinks into skills/; this is a real file or directory");
        continue;
      }
      const skill = onDisk.get(entry.name);
      if (!skill) {
        fail("target-link-extra", `${farmName}/${entry.name}`, `"${entry.name}" is linked but no such skill exists`);
        continue;
      }
      const current = fs.readlinkSync(link);
      if (path.resolve(farmDir, current) !== path.join(skillsDir, skill.scene, skill.name)) {
        fail("target-link-wrong", `${farmName}/${entry.name}`, `points at ${current}, expected skills/${skill.scene}/${skill.name}`);
      }
    }
    for (const name of wanted) {
      if (!present.has(name)) fail("target-link-missing", farmName, `"${name}" is in the ${pool} pool but not linked in ${farmName}/`);
    }
    for (const name of present) {
      if (!wanted.has(name) && onDisk.has(name)) {
        fail("target-link-extra", `${farmName}/${name}`, `"${name}" is linked but is not in the ${pool} pool`);
      }
    }
  }
}

export function checkAssets(root) {
  const problems = [];
  const fail = (rule, file, message) => problems.push({ rule, file, message });

  const skillsDir = path.join(root, "skills");
  const readmeRel = "README.md";
  const readmePath = path.join(root, readmeRel);
  if (!fs.existsSync(readmePath)) {
    fail("root-readme-missing", readmeRel, "README.md is missing, so no skill is indexed");
    return problems;
  }
  const readme = fs.readFileSync(readmePath, "utf8");

  // `skills/` holds only scene directories (plus the archive bucket), and each holds only
  // skill directories.
  for (const entry of fs.readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) {
      fail("skills-stray-file", `skills/${entry.name}`, "skills/ holds only scene directories; this is a file");
    }
  }
  for (const scene of dirs(skillsDir)) {
    for (const entry of fs.readdirSync(path.join(skillsDir, scene), { withFileTypes: true })) {
      if (!entry.isDirectory()) {
        fail("scene-stray-file", `skills/${scene}/${entry.name}`, `skills/${scene}/ holds only skill directories; this is a file`);
      }
    }
  }

  const skills = librarySkills(skillsDir);
  const onDisk = new Map(skills.map((skill) => [skill.name, skill]));

  // targets.json decides what is published, and the archive is the complement.
  let targets = null;
  const targetsPath = path.join(root, TARGETS);
  if (!fs.existsSync(targetsPath)) {
    fail("targets-missing", TARGETS, "no targets.json, so no skill is published anywhere");
  } else {
    try {
      const parsed = JSON.parse(fs.readFileSync(targetsPath, "utf8"));
      const shapeOk =
        parsed &&
        typeof parsed === "object" &&
        !Array.isArray(parsed) &&
        Object.values(parsed).every(
          (names) => Array.isArray(names) && names.every((name) => typeof name === "string" && name !== ""),
        );
      if (!shapeOk) fail("targets-invalid", TARGETS, "expected an object mapping a pool name to an array of skill names");
      else targets = parsed;
    } catch (error) {
      fail("targets-invalid", TARGETS, `not valid JSON: ${error.message}`);
    }
  }

  if (targets) {
    const listed = new Set();
    for (const [pool, names] of Object.entries(targets)) {
      const seen = new Set();
      for (const name of names) {
        if (seen.has(name)) fail("targets-duplicate", TARGETS, `"${name}" is listed twice under "${pool}"`);
        seen.add(name);
        listed.add(name);
        const skill = onDisk.get(name);
        if (!skill) fail("targets-unknown-skill", TARGETS, `"${name}" is listed under "${pool}" but has no directory`);
        else if (skill.isArchive) fail("targets-archived-skill", TARGETS, `"${name}" is archived, so no harness may be told about it`);
      }
    }
    for (const skill of skills) {
      if (skill.isArchive) continue;
      if (!listed.has(skill.name)) {
        fail("targets-unlisted", TARGETS, `"${skill.name}" is in no target list and not archived, so nothing decides where it goes`);
      }
    }
    checkFarms(fail, root, skillsDir, targets, onDisk);
  }

  const entries = indexEntries(readme);
  const indexed = new Set(entries.map((entry) => entry.name));

  for (const entry of entries) {
    const where = `${readmeRel}:${entry.lineNo}`;
    const found = onDisk.get(entry.name);
    if (!found) {
      fail("index-entry-unresolved", where, `"${entry.name}" has no skills/${entry.scene}/${entry.name}/SKILL.md`);
      continue;
    }
    if (found.scene !== entry.scene) {
      fail(
        "index-scene-mismatch",
        where,
        `"${entry.name}" is at skills/${found.scene}/${entry.name}/, but the index links skills/${entry.scene}/${entry.name}/`,
      );
    }
    if (found.isArchive && entry.declared !== ARCHIVE) {
      fail("index-archived-mismatch", where, `"${entry.name}" is archived, so it belongs under "## Archived"`);
    } else if (!found.isArchive && entry.declared === ARCHIVE) {
      fail("index-archived-mismatch", where, `"${entry.name}" is published, so it does not belong under "## Archived"`);
    }
  }

  // Entries are alphabetical within a section, so a new skill has one obvious home.
  for (let i = 1; i < entries.length; i++) {
    const prev = entries[i - 1];
    const entry = entries[i];
    if (prev.declared === entry.declared && entry.name < prev.name) {
      fail("index-order", `${readmeRel}:${entry.lineNo}`, `"${entry.name}" comes after "${prev.name}"; entries are alphabetical`);
    }
  }
  if (entries.length === 0) fail("root-index-empty", readmeRel, "the index lists no skills");

  for (const skill of skills) {
    const skillPath = path.join(skillsDir, skill.scene, skill.name, "SKILL.md");
    if (!fs.existsSync(skillPath)) {
      fail("skill-no-skill-md", `skills/${skill.scene}/${skill.name}`, "directory has no SKILL.md");
      continue;
    }
    if (!indexed.has(skill.name)) fail("skill-not-indexed", readmeRel, `"${skill.name}" has no entry in the index`);

    const text = fs.readFileSync(skillPath, "utf8");
    checkFrontmatter(fail, skill.rel, skill.name, text);
    const fields = parseFrontmatter(text);
    if (fields === null || skill.isArchive) continue;

    const flagged = (fields["disable-model-invocation"] ?? "").trim().toLowerCase() === "true";
    const entry = entries.find((candidate) => candidate.name === skill.name);
    if (!entry) continue;
    if (entry.declared === null) {
      fail("invocation-undeclared", `${readmeRel}:${entry.lineNo}`, `"${skill.name}" is outside every index section`);
    } else if (entry.declared === "user" && !flagged) {
      fail(
        "invocation-mismatch",
        `${readmeRel}:${entry.lineNo}`,
        `"${skill.name}" is listed as user-invoked but its frontmatter has no disable-model-invocation: true`,
      );
    } else if (entry.declared === "model" && flagged) {
      fail(
        "invocation-mismatch",
        `${readmeRel}:${entry.lineNo}`,
        `"${skill.name}" is listed as model-invoked but its frontmatter sets disable-model-invocation: true`,
      );
    }
  }

  return problems;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(fileURLToPath(import.meta.url));
if (isMain) {
  const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
  const problems = checkAssets(root);
  if (problems.length === 0) {
    console.log("skill library is consistent");
  } else {
    for (const { rule, file, message } of problems) console.log(`${file}: ${message} [${rule}]`);
    console.log(`${problems.length} problem${problems.length === 1 ? "" : "s"} found`);
    process.exitCode = 1;
  }
}
