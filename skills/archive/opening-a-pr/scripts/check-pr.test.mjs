import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { checkPr } from './check-pr.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const example = fs.readFileSync(path.join(here, '../references/example.md'), 'utf8').match(/```markdown\n([\s\S]*?)\n```/)[1];
const messages = text => checkPr(text).problems.map(p => p.message).join('\n');

test('accepts the default briefing and permits omitting a nonexistent tradeoff', () => {
  assert.deepEqual(checkPr(example).problems, []);
  assert.deepEqual(checkPr(example.replace(/## Tradeoffs[\s\S]*?(?=## Blast Radius)/, '')).problems, []);
});
test('rejects logs and path inventories submitted as the PR body', () => {
  assert.match(messages('src/server.mjs\n$ npm test\n42 tests passed\n'), /start with ## Why/);
  assert.match(messages('## Summary\n- src/server.mjs\n## Evidence\nAll green.\n'), /expected Why/);
});
test('requires scope, risk and correctly ordered briefing sections', () => {
  assert.match(messages(example.replace('## Scope', '## Files')), /expected Why/);
  assert.match(messages(example.replace('## Blast Radius', '## Risk')), /expected Why/);
  assert.match(messages(example.replace('## Why', '## What changed')), /expected Why/);
  assert.match(messages(example.replace(/(## Blast Radius\n)[\s\S]*?(?=## Verification)/, '$1\n')), /reviewer-facing prose/);
});
test('requires a per-operation evidence link, including multiline bullets', () => {
  assert.match(messages(example.replace(/\[API run and state assertions\]\([^)]+\)/, 'tests passed')), /evidence link/);
  assert.deepEqual(checkPr(example.replace('. [API run', '.\n  [API run')).problems, []);
});
test('rejects unfilled placeholders and lab-notebook-sized descriptions', () => {
  assert.match(messages(example.replace('A lost response', '{{problem}}')), /placeholder/);
  assert.match(messages(example + '\n' + Array(41).fill('raw log line').join('\n')), /at most 40/);
});
test('ignores diagram headings but rejects incomplete code fences', () => {
  assert.deepEqual(checkPr(example.replace('## Scope', '```text\n## fake\n```\n\n## Scope')).problems, []);
  assert.match(messages(example + '\n~~~\nunfinished'), /unclosed code fence/);
});
test('CLI is read-only and distinguishes invalid content from usage/read errors', t => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pr-briefing-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const file = path.join(dir, 'body with spaces.md');
  const run = args => spawnSync(process.execPath, [path.join(here, 'check-pr.mjs'), ...args], { encoding: 'utf8' });
  fs.writeFileSync(file, example);
  assert.equal(run([file]).status, 0);
  assert.equal(fs.readFileSync(file, 'utf8'), example);
  fs.writeFileSync(file, 'npm test: all green');
  assert.equal(run([file]).status, 1);
  assert.equal(run([]).status, 2);
  assert.equal(run([file + '.missing']).status, 2);
  assert.equal(run(['--help']).status, 0);
});
