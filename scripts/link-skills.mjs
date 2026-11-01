#!/usr/bin/env node
// Publish this repo's two skill folders into ~/.agents with one symlink each:
//   ~/.agents/skills        -> skills/         Pi's user skill directory, loaded in every session
//   ~/.agents/scoped-skills -> scoped-skills/  a store, not a skill location, so Pi never reads it
// A single symlink per folder means a git pull keeps everything current, and it replaces the
// older layout of one symlink per skill. Refuses to discard anything that does not point back
// into this repo.
// Usage: node scripts/link-skills.mjs [--check]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const repo = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const agentsDir = path.join(process.env.HOME, ".agents");
const checkOnly = process.argv.includes("--check");

const LINKS = [
  { name: "skills", src: path.join(repo, "skills") },
  { name: "scoped-skills", src: path.join(repo, "scoped-skills") },
];

/** Every entry in a legacy per-skill directory, reporting the ones this repo does not own. */
function legacyContents(dir) {
  const owned = [];
  const foreign = [];
  for (const entry of fs.readdirSync(dir)) {
    const link = path.join(dir, entry);
    let target = null;
    try {
      target = fs.readlinkSync(link);
    } catch {
      /* a real directory or file */
    }
    if (target !== null && path.resolve(dir, target).startsWith(repo + path.sep)) owned.push(entry);
    else foreign.push(entry);
  }
  return { owned, foreign };
}

/** Publish one link, replacing only what this repo owns. Returns false on a problem. */
function publish({ name, src }) {
  const dest = path.join(agentsDir, name);

  if (!fs.existsSync(src)) {
    console.log(`problem: ${src} does not exist, so ${dest} cannot be published`);
    return false;
  }

  let state;
  try {
    state = fs.lstatSync(dest);
  } catch {
    state = null;
  }

  if (state === null) {
    if (checkOnly) {
      console.log(`problem: ${dest} does not exist; run scripts/link-skills.mjs`);
      return false;
    }
    fs.mkdirSync(agentsDir, { recursive: true });
    fs.symlinkSync(src, dest);
    console.log(`linked ${dest} -> ${src}`);
    return true;
  }

  if (state.isSymbolicLink()) {
    const target = fs.readlinkSync(dest);
    if (path.resolve(agentsDir, target) === src) {
      console.log(`${dest} -> ${src}`);
      return true;
    }
    if (checkOnly) {
      console.log(`problem: ${dest} links to ${target}, expected ${src}`);
      return false;
    }
    fs.rmSync(dest, { force: true });
    fs.symlinkSync(src, dest);
    console.log(`relinked ${dest} -> ${src} (was ${target})`);
    return true;
  }

  if (state.isDirectory()) {
    // The old layout: one symlink per skill, all pointing into this repo.
    const { owned, foreign } = legacyContents(dest);
    if (foreign.length > 0) {
      console.log(`problem: ${dest} holds entries that do not point into this repo, left alone: ${foreign.join(", ")}`);
      console.log("Move or remove them yourself, then re-run this script.");
      return false;
    }
    if (checkOnly) {
      console.log(`problem: ${dest} is still the per-skill directory (${owned.length} links); run scripts/link-skills.mjs`);
      return false;
    }
    fs.rmSync(dest, { recursive: true, force: true });
    fs.symlinkSync(src, dest);
    console.log(`replaced the per-skill directory (${owned.length} links) with ${dest} -> ${src}`);
    return true;
  }

  console.log(`problem: ${dest} exists and is neither a symlink nor a directory, left alone`);
  return false;
}

let ok = true;
for (const link of LINKS) ok = publish(link) && ok;
if (!ok) process.exitCode = 1;
