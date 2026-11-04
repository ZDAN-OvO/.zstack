# Agent Instructions

This repo is a skill library, not a project to build or test. Each directory under `skills/<scene>/` is one Agent Skill, copied from an upstream source and published by one symlink per skill into each harness that [`targets.json`](./targets.json) names.

## Layout

| Item | Rule |
|---|---|
| Skill | `skills/<scene>/<skill-name>/SKILL.md` |
| Scenes | Exactly seven, one level: `plan`, `build`, `verify`, `investigate`, `explain`, `documents`, `meta` |
| Archive | `skills/archive/<skill-name>/` holds skills no harness is told about. It is a bucket, not an eighth scene |
| Targets | `targets.json` lists which skills each harness gets: `pi` and `claude`. A skill in a scene must appear in at least one list; a skill in no list belongs in `archive/` |
| Farms | `skills-pi/<skill-name>` and `skills-claude/<skill-name>` are symlinks into `skills/`, built from `targets.json`. Never edited by hand; each harness only needs one symlink at the farm |
| Root index | `README.md` lists every skill: user-invoked, model-invoked, and archived. It is the only index |
| Supporting files | `references/`, `scripts/`, and assets stay beside `SKILL.md` |
| Frontmatter | `name` must equal the skill directory name |

Scenes are the one grouping axis: what you are doing when you reach for the skill, never what the skill is about. `plan` is the fuzzy request before code, `build` is settled design and implementation, `verify` is review and evidence before delivery, `investigate` is broken or unexplained code, `explain` is telling or drawing a result for a human, `documents` is a non-code deliverable, `meta` is the working setup itself. Each scene holds between 1 and 6 live skills, and every addition has one obvious home; a skill that fits two scenes goes to the earlier one in that list. Do not add a scene without deleting one, and do not nest deeper: the tree stops at `skills/<scene>/<skill>/`.

## Index

- `README.md` holds the repo description, then `## User-invoked`, `## Model-invoked`, and `## Archived`, each a flat list of `- **[name](./skills/<scene>/name/SKILL.md)**: one-line description.`
- The one-liner is our own human-facing summary of the skill, never a pasted trigger list. The skill name always links to its `SKILL.md` under `skills/<scene>/`.
- The `## Scenes` and `## Targets` tables explain the folders and the install split; the entry paths stay authoritative. Moving a skill between scenes, or in and out of the archive, means moving the directory and its index path together.
- Archive membership is not an invocation mode: an archived skill keeps its frontmatter flag, but it is listed under `## Archived` and published nowhere.
- Invocation is the axis the index sorts on. Every skill is either user-invoked (`disable-model-invocation: true`, reachable only as `/skill:<name>`, description read by a human) or model-invoked (no flag, description carries trigger phrasing). Keep whichever mode upstream chose.
- Entries are alphabetical within a section.
- Adding, renaming, or removing a skill, or flipping its invocation mode, updates `README.md` in the same change. An index that misses a skill, or routes to one that is gone, is a defect, not a chore for later.

## Skill references

A skill that points at another skill names it as `/<skill-name>`: ``run `/grilling` ``, ``see `/unslop` ``. Never as a path, not `~/.pi/agent/skills/x/SKILL.md`, not `../x/SKILL.md`, not `$SKILLS_HOME/x/SKILL.md`. Paths are only for files the skill itself owns: its own `scripts/`, `references/`, and assets.

This is a Pi porting rule rather than upstream wording. When an upstream skill links another skill by path, or names Claude Code's Skill tool, convert that reference to `/<skill-name>` and change nothing else in the sentence. Report it like any other adaptation. The root index is navigation, not a reference: it keeps linking `./skills/<scene>/name/SKILL.md`.

## Install a skill

1. Pin the upstream source to a revision (commit SHA or tag). Copy from upstream itself, never from a translation, port, or another agent's vendored copy.
2. Copy the skill directory to `skills/<scene>/<skill-name>`, byte for byte, then confirm with `diff -r` against the source. Retyping upstream prose is a defect even when it looks equivalent.
3. Compare frontmatter field by field against upstream, not only the body. Keep `disable-model-invocation: true` when upstream has it.
4. Adapt only what cannot work on Pi, with a targeted edit. That means platform paths (`.cursor/skills/` becomes `.agents/skills/`), other agents' config paths, and vendor-specific tool names. Everything else stays as upstream wrote it.
5. Re-run `diff -r` against the source and state every changed line.
6. Publish it and verify:

   ```bash
   node scripts/link-skills.mjs
   node scripts/link-skills.mjs --check
   ```

   The script reads `targets.json`, rebuilds `skills-pi/` and `skills-claude/` (one relative symlink per skill, pointing into `skills/`), then points `~/.pi/agent/skills` at the first farm and `~/.claude/skills` at the second. It prunes links that point into this repo but are no longer listed, and leaves every entry it does not own alone, so a skill that travels to both harnesses is still one directory here. It does not read frontmatter, so check the invocation flag against upstream yourself.

7. Add the entry to `README.md` under the right invocation heading and the scene folder the skill landed in, add its name to `targets.json`, and report the source and revision, plus any reference the copy left dangling (a playbook, skill, or path that does not exist here).

The user runs `/reload` in Pi after a skill or its frontmatter changes.

## Facts

- `~/.pi/agent/skills` is Pi's user skill directory and `~/.claude/skills` Claude Code's. Each is a single symlink to a farm in this repo (`skills-pi/`, `skills-claude/`), and each farm holds one symlink per published skill pointing into `skills/`. A `git pull` therefore updates both harnesses, and a skill that goes to both still lives here once. Pi discovers directories containing `SKILL.md` recursively, so the scene folder costs nothing.
- `~/.agents/` is retired: nothing is published there any more, and neither script writes it.
- Writing through either link writes into this repo's working tree. Tools that install skills by writing there modify the repo directly; treat those changes as unreviewed and verify them with `git status`.
- `scripts/link-skills.mjs` maintains both farms and both links from `targets.json`; it is the only supported way to publish skills. Idempotent, no dependencies, and it owns only links that resolve inside this repo.
- `AGENTS.global.md` is the global instructions asset. Publish it by symlink at `~/.pi/agent/AGENTS.md` for Pi's native context loader. This repo's own instructions remain in this file.

## Verify library assets

| Check | Command |
| --- | --- |
| Both farms and both harness links match `targets.json`, with no stale links into this repo | `node scripts/link-skills.mjs --check` |
| Scene layout, archive, targets, root index, frontmatter, invocation mode | `node scripts/check-assets.mjs` |
| Checker regression tests | `node --test scripts/*.test.mjs` |

`.github/workflows/validate-assets.yml` runs the last two on every push and pull request. The link check stays local, because CI has no home directory to link.

## Don't

- Do not reword, shorten, or otherwise improve copied upstream text. Report the problem instead. The one exception is a cross-skill reference: convert it to `/<skill-name>` (see above).
- Do not install with `npx skills add`: it skips the pin and the `diff -r` verification, and writes an unverified copy straight into this working tree through the symlink.
- Do not create a scene, or nest deeper than `skills/<scene>/<skill>/`. The seven scenes are fixed; a new skill joins an existing one.
- Do not leave a skill in a scene without a `targets.json` entry, and do not list an archived skill as a target. A scene skill with no target, or an archived skill with one, is a defect the checker reports.
- Do not put a file directly under `skills/`, under a scene folder, or under `archive/`. Every entry in all three is a directory, and every skill directory has a `SKILL.md`.
- Do not let `README.md` drift from `skills/`. Update it in the same change that touches the skill, including its scene path and whether it is archived.
