#!/usr/bin/env node
// Publish this repo's skills into both harnesses, with the skill files existing once.
//
//   skills-pi/<skill>      -> ../skills/<scene>/<skill>     built from targets.json
//   skills-claude/<skill>  -> ../skills/<scene>/<skill>     built from targets.json
//   ~/.pi/agent/skills     -> skills-pi/                    Pi's user skill directory
//   ~/.claude/skills       -> skills-claude/                Claude Code's user skill directory
//
// One directory symlink per harness is all a harness needs, and one symlink per skill in each
// farm keeps both current after a git pull, so a skill file exists once. Nothing outside those
// two links is touched: a target directory holding anything that does not point back into this
// repo is reported, not deleted.
// Usage: node scripts/link-skills.mjs [--check]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const home = process.env.HOME;
const checkOnly = process.argv.includes("--check");
const skillsDir = path.join(repo, "skills");

const LINKS = [
  { base: path.join(home, ".pi", "agent"), name: "skills", src: path.join(repo, "skills-pi") },
  { base: path.join(home, ".claude"), name: "skills", src: path.join(repo, "skills-claude") },
];
function problem(message) {
  console.log(`problem: ${message}`);
  return false;
}

function targets() {
  const file = path.join(repo, "targets.json");
  if (!fs.existsSync(file)) {
    console.log("problem: targets.json is missing, so there is nothing to publish");
    return null;
  }
  try {
    const parsed = JSON.parse(fs.readFileSync(file, "utf8"));
    if (!parsed || typeof parsed !== "object" || !Object.values(parsed).every(Array.isArray)) {
      console.log("problem: targets.json is not an object mapping a pool to an array of skill names");
      return null;
    }
    return parsed;
  } catch (error) {
    console.log(`problem: targets.json is not valid JSON: ${error.message}`);
    return null;
  }
}

/** name -> scene, from the skills/ tree. */
function sceneOf() {
  const scenes = new Map();
  for (const scene of fs.readdirSync(skillsDir, { withFileTypes: true })) {
    if (!scene.isDirectory()) continue;
    for (const entry of fs.readdirSync(path.join(skillsDir, scene.name), { withFileTypes: true })) {
      if (entry.isDirectory()) scenes.set(entry.name, scene.name);
    }
  }
  return scenes;
}

/** Make `farm` hold exactly one link per wanted name, pointing at that skill's directory. */
function syncFarm(farm, names, scenes) {
  const dir = path.join(repo, farm);
  let ok = true;
  if (!fs.existsSync(dir)) {
    if (checkOnly) return problem(`${farm}/ does not exist; run scripts/link-skills.mjs`);
    fs.mkdirSync(dir);
  }

  const wanted = new Set(names);
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const link = path.join(dir, entry.name);
    const current = entry.isSymbolicLink() ? fs.readlinkSync(link) : null;
    const owned = current !== null && path.resolve(dir, current).startsWith(repo + path.sep);
    if (wanted.has(entry.name) && current !== null) {
      const scene = scenes.get(entry.name);
      if (path.resolve(dir, current) === path.join(skillsDir, scene ?? "", entry.name)) continue;
    }
    if (current === null) {
      ok = problem(`${farm}/${entry.name} is a real file or directory; ${farm}/ holds only links into skills/`) && ok;
      continue;
    }
    if (!owned) {
      ok = problem(`${farm}/${entry.name} links outside this repo (${current}), left alone`) && ok;
      continue;
    }
    if (wanted.has(entry.name)) {
      if (checkOnly) ok = problem(`${farm}/${entry.name} points at ${current}, expected skills/${scenes.get(entry.name) ?? "?"}/${entry.name}`) && ok;
      else {
        fs.rmSync(link, { force: true });
        fs.symlinkSync(path.join("..", "skills", scenes.get(entry.name) ?? "", entry.name), link);
        console.log(`relinked ${farm}/${entry.name}`);
      }
    } else if (checkOnly) {
      ok = problem(`${farm}/${entry.name} is not in targets.json; run scripts/link-skills.mjs`) && ok;
    } else {
      fs.rmSync(link, { force: true });
      console.log(`removed ${farm}/${entry.name} (not in targets.json)`);
    }
  }

  for (const name of [...wanted].sort()) {
    const link = path.join(dir, name);
    if (fs.existsSync(link) || fs.lstatSync(link, { throwIfNoEntry: false })) continue;
    const scene = scenes.get(name);
    if (!scene) {
      ok = problem(`"${name}" is in targets.json but has no skills/<scene>/${name}/ directory`) && ok;
      continue;
    }
    if (checkOnly) ok = problem(`${farm}/${name} is missing; run scripts/link-skills.mjs`) && ok;
    else {
      fs.symlinkSync(path.join("..", "skills", scene, name), link);
      console.log(`linked ${farm}/${name} -> skills/${scene}/${name}`);
    }
  }
  return ok;
}

/** Point one harness directory at this repo's farm, replacing only what this repo owns. */
function publish({ base, name, src }) {
  const dest = path.join(base, name);
  if (!fs.existsSync(src)) return problem(`${src} does not exist, so ${dest} cannot be published`);

  const state = fs.lstatSync(dest, { throwIfNoEntry: false });
  if (!state) {
    if (checkOnly) return problem(`${dest} does not exist; run scripts/link-skills.mjs`);
    fs.mkdirSync(base, { recursive: true });
    fs.symlinkSync(src, dest);
    console.log(`linked ${dest} -> ${src}`);
    return true;
  }

  if (state.isSymbolicLink()) {
    const target = fs.readlinkSync(dest);
    if (path.resolve(base, target) === src) {
      console.log(`${dest} -> ${src}`);
      return true;
    }
    if (checkOnly) return problem(`${dest} links to ${target}, expected ${src}`);
    fs.rmSync(dest, { force: true });
    fs.symlinkSync(src, dest);
    console.log(`relinked ${dest} -> ${src} (was ${target})`);
    return true;
  }

  if (state.isDirectory()) {
    // The older layout: one symlink per skill, all pointing into this repo.
    const entries = fs.readdirSync(dest);
    const foreign = entries.filter((entry) => {
      const link = path.join(dest, entry);
      const target = fs.lstatSync(link).isSymbolicLink() ? fs.readlinkSync(link) : null;
      return target === null || !path.resolve(dest, target).startsWith(repo + path.sep);
    });
    if (foreign.length > 0) {
      return problem(
        `${dest} holds entries that do not point into this repo, left alone: ${foreign.join(", ")}\n` +
          "Move or remove them yourself, then re-run this script.",
      );
    }
    if (checkOnly) return problem(`${dest} is still the per-skill directory (${entries.length} links); run scripts/link-skills.mjs`);
    fs.rmSync(dest, { recursive: true, force: true });
    fs.symlinkSync(src, dest);
    console.log(`replaced the per-skill directory (${entries.length} links) with ${dest} -> ${src}`);
    return true;
  }

  return problem(`${dest} exists and is neither a symlink nor a directory, left alone`);
}

const wanted = targets();
let ok = wanted !== null;
if (ok) {
  const scenes = sceneOf();
  ok = syncFarm("skills-pi", wanted.pi ?? [], scenes) && ok;
  ok = syncFarm("skills-claude", wanted.claude ?? [], scenes) && ok;
  for (const link of LINKS) ok = publish(link) && ok;
}
if (!ok) process.exitCode = 1;
