#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REQUIRED = ['Why', 'What changed', 'Scope', 'Blast Radius', 'Verification'];
const ALL = ['Why', 'What changed', 'Scope', 'Tradeoffs', 'Blast Radius', 'Verification'];

// Deliberately checks the published default format, not the truth of a PR's claims.
export function checkPr(text) {
  const problems = [];
  const fail = (line, message) => problems.push({ line, message });
  const sections = [];
  const lines = [];
  let fence = null;
  const raw = text.split(/\r?\n/);
  for (let i = 0; i < raw.length; i++) {
    const line = raw[i];
    if (fence) {
      const m = line.match(/^ {0,3}(`+|~+)[ \t]*$/);
      if (m && m[1][0] === fence.char && m[1].length >= fence.length) fence = null;
      continue;
    }
    const opening = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
    if (opening && !(opening[1][0] === '`' && opening[2].includes('`'))) {
      fence = { char: opening[1][0], length: opening[1].length, line: i + 1 };
      continue;
    }
    const l = { text: line, n: i + 1 };
    lines.push(l);
    const h = /^## (.+)$/.exec(line);
    if (h) sections.push({ name: h[1].trim(), n: i + 1, body: [] });
    else if (sections.length) sections.at(-1).body.push(l);
    else if (line.trim()) fail(i + 1, 'start with ## Why; move preambles into the briefing');
    if (/\{\{[^}]*\}\}|\b(?:TODO|TBD|FIXME)\b|<(?:evidence|path|summary|outcome|link)(?:\s[^>]*)?>/i.test(line)) fail(i + 1, 'unfilled placeholder');
    if (/^# |^### /.test(line)) fail(i + 1, 'use only the fixed H2 sections in the briefing');
  }
  if (fence) fail(fence.line, 'unclosed code fence');
  const names = sections.map(s => s.name);
  const expected = ALL.filter(name => REQUIRED.includes(name) || names.includes(name));
  if (names.join('|') !== expected.join('|')) fail(1, 'expected Why, What changed, Scope, optional Tradeoffs, Blast Radius, Verification in order');
  const nonblank = raw.filter(l => l.trim()).length;
  if (nonblank > 40) fail(1, `briefing is ${nonblank} nonblank lines; link details and keep at most 40`);
  for (const s of sections) {
    const prose = s.body.filter(l => l.text.trim());
    if (!prose.length) fail(s.n, `${s.name} needs reviewer-facing prose`);
    if (['What changed', 'Scope', 'Verification'].includes(s.name)) {
      const bullets = prose.filter(l => /^- \S/.test(l.text));
      if (bullets.length < 1 || bullets.length > 3) fail(s.n, `${s.name} needs 1–3 top-level bullets`);
      if (s.name === 'Verification') {
        for (let i = 0; i < bullets.length; i++) {
          const at = s.body.indexOf(bullets[i]);
          const end = i + 1 < bullets.length ? s.body.indexOf(bullets[i + 1]) : s.body.length;
          const item = s.body.slice(at, end).map(l => l.text).join('\n');
          if (!/\[[^\]\n]+\]\((?:https?:\/\/[^\s)]+|[^\s)]+)\)/.test(item)) fail(bullets[i].n, 'each Verification bullet needs a Markdown evidence link');
        }
      }
    }
  }
  return { problems };
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === '--help') {
    console.log('Usage: node check-pr.mjs <body.md>\nChecks default briefing structure, not evidence truth. Exit 0 valid, 1 invalid, 2 usage/read error.');
    return;
  }
  if (args.length !== 1 || args[0].startsWith('-')) {
    console.error('Usage: node check-pr.mjs <body.md>');
    process.exitCode = 2;
    return;
  }
  try {
    const { problems } = checkPr(fs.readFileSync(args[0], 'utf8'));
    for (const p of problems) console.error(`${args[0]}:${p.line}: ${p.message}`);
    console.log(`${problems.length} problems`);
    process.exitCode = problems.length ? 1 : 0;
  } catch (error) {
    console.error(`${args[0]}: ${error.message}`);
    process.exitCode = 2;
  }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
