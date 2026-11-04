import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { checkPlan } from './check-plan.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const example = fs.readFileSync(path.join(here, '../references/examples.md'), 'utf8').match(/```markdown\n([\s\S]*?)\n```/)[1];
const messages = text => checkPlan(text).problems.map(p => p.message).join('\n');
const pr = example.slice(example.indexOf('## PR-01 '), example.indexOf('## Close the program'));
const two = example.replace('## Close the program', `${pr.replaceAll('PR-01', 'PR-02').replace('**Depends on.** None.', '**Depends on.** PR-01.')}## Close the program`);

function docsPlan() {
  return example.replace('Kind. Behavior.', 'Kind. Docs.').replace('Surfaces. API, Web.', 'Surfaces. None.').replace('Interaction. Yes.', 'Interaction. No.')
    .replace(/\*\*Verify, live\.\*\*[\s\S]*?(?=\*\*Verify, perf\.)/, '**Verify, live.** Not applicable. Reference text only; no runtime changes.\n\n')
    .replace(/\*\*Verify, perf\.\*\*[\s\S]*?(?=\*\*Review gate\.)/, '**Verify, perf.** Not applicable. No executable or build input changes.\n\n')
    .replace(/\*\*Review gate\.\*\*[\s\S]*?(?=\*\*Merge\.)/, '**Review gate.** Not applicable. No user interaction changes.\n\n');
}

test('accepts the published two-surface example', () => assert.deepEqual(checkPlan(example).problems, []));
test('accepts sequential PRs with a known dependency', () => assert.deepEqual(checkPlan(two).problems, []));
test('accepts a documentation change with concrete non-applicability reasons', () => assert.deepEqual(checkPlan(docsPlan()).problems, []));
test('rejects unfilled template placeholders', () => {
  const template = fs.readFileSync(path.join(here, '../references/plan-template.md'), 'utf8');
  assert.match(messages(template), /placeholder/);
});
test('rejects a Draft instead of treating its structure as approval', () => assert.match(messages(example.replace('Status. Ready.', 'Status. Draft.')), /not Ready/));
test('rejects declared or missing design blockers in a ready plan', () => {
  assert.match(messages(example.replace('Blockers. None.', 'Blockers. Gateway probe pending.')), /ready plan must declare/);
  assert.match(messages(example.replace('Blockers. None.', '')), /Blockers/);
});
test('rejects unresolved command ports and whitespace-only evidence destinations', () => {
  assert.match(messages(example.replace('node artifacts/credit-retry/driver.mjs', 'PORT=<port> node artifacts/credit-retry/driver.mjs')), /placeholder/);
  assert.match(messages(example.replace('`artifacts/credit-retry/diff.patch`', '`  `')), /each box needs Evidence/);
});
test('rejects a missing structural section', () => assert.match(messages(example.replace('## Appendix C. Risks', '## Risks')), /H2 sections/));
test('rejects empty global boot instructions', () => assert.match(messages(example.replace(/(### Boot recipe\n)[\s\S]*?(?=### Verdict)/, '$1\n')), /empty program subsection Boot recipe/));
test('rejects missing version and invalidation fields', () => {
  for (const field of ['Versions', 'Invalidation', 'Input boundary']) assert.match(messages(example.replace(new RegExp(`^${field}\\. .+$`, 'm'), '')), new RegExp(field));
});
test('rejects repeated or unknown PR IDs', () => {
  assert.match(messages(two.replaceAll('PR-02', 'PR-01')), /duplicate PR ID/);
  assert.match(messages(example.replace('**Depends on.** None.', '**Depends on.** PR-99.')), /unknown dependency/);
});
test('rejects self dependency and a dependency cycle', () => {
  assert.match(messages(example.replace('**Depends on.** None.', '**Depends on.** PR-01.')), /self-dependency/);
  assert.match(messages(two.replace('**Depends on.** None.', '**Depends on.** PR-02.')), /dependency cycle/);
});
test('rejects an absent or reordered PR block', () => {
  assert.match(messages(example.replace('**Build.**', '**Implementation.**')), /nine PR blocks/);
  assert.match(messages(example.replace('**Build.**', '**Files.**')), /nine PR blocks/);
});
test('rejects evidence-free and prechecked future boxes', () => {
  assert.match(messages(example.replace(' Evidence. `artifacts/credit-retry/diff.patch`.', '')), /each box needs Evidence/);
  assert.match(messages(example.replace('- [ ] Edit', '- [x] Edit')), /must be unchecked/);
});
test('rejects automated or live omissions in behavior changes', () => {
  for (const block of ['unit', 'live']) assert.match(messages(example.replace(`**Verify, ${block}.** Required.`, `**Verify, ${block}.** Not applicable. Faster to skip.`)), /behavior requires automated and live/);
});
test('rejects missing pass predicates and trunk regressions', () => {
  assert.match(messages(example.replace('Pass when all cases match', 'Expected: all cases match')), /needs Pass when/);
  assert.match(messages(example.replace('Regression against trunk.', 'Check head only.')), /needs Regression against trunk/);
});
test('requires every declared surface to have a live scenario', () => assert.match(messages(example.replace('Surface. Web.', 'Surface. API.')), /does not cover surface Web/));
test('rejects empty non-applicability reasons', () => assert.match(messages(docsPlan().replace('Not applicable. No executable or build input changes.', 'Not applicable.')), /specific reason/));
test('requires all four perf fields and a numeric limit with units', () => {
  assert.match(messages(example.replace('- [ ] Baseline.', '- [ ] Starting point.')), /Metric, Probe, Baseline, Rule/);
  assert.match(messages(example.replace('Limit. 50 ms.', 'Limit. fast.')), /number and unit/);
});
test('enforces interaction review and the media/approval contract', () => {
  assert.match(messages(example.replace('Interaction. Yes.', 'Interaction. No.')), /must match Interaction/);
  assert.match(messages(example.replace('screenshots and video', 'screenshots only')), /screenshots, video, operator, and approval/);
});
test('requires feasibility, acceptance, review entity and change-control contracts', () => {
  for (const field of ['Feasibility', 'Acceptance', 'Changes', 'Review entity', 'Verdict']) {
    assert.match(messages(example.replace(new RegExp(`^${field}\\. .+$`, 'm'), '')), new RegExp(field));
    assert.match(messages(example.replace(new RegExp(`^${field}\\. .+$`, 'm'), `${field}. None.`)), /specific contract/);
  }
});
test('requires per-PR branch, write ownership, resources and interface compatibility', () => {
  for (const field of ['Base', 'Writes', 'Resources', 'Contract']) assert.match(messages(example.replace(new RegExp(`^${field}\\. .+$`, 'm'), '')), new RegExp(field));
  assert.match(messages(example.replace('Base. Trunk.', 'Base. PR-99.')), /Base must/);
  assert.match(messages(example.replace(/^Writes\. .+$/m, 'Writes. The backend.')), /backticked owned paths/);
  assert.match(messages(example.replace(/^Resources\. .+$/m, 'Resources. None.')), /isolation\/compatibility/);
});
test('accepts independent parallel PRs with disjoint ownership', () => {
  const parallel = two.replace('**Depends on.** PR-01.', '**Depends on.** None.')
    .replace('Parallel. None. This plan has one PR; run the API and Web integration checks together before handoff.', 'Parallel. PR-01, PR-02.')
    .replace(/(## PR-02[\s\S]*?Writes\.)[^\n]+/, '$1 `src/report.mjs`.');
  assert.deepEqual(checkPlan(parallel).problems, []);
});
test('rejects dependent parallel groups and shared writes', () => {
  const parallel = two.replace(/^Parallel\. .+$/m, 'Parallel. PR-01, PR-02.');
  assert.match(messages(parallel), /have a dependency/);
  assert.match(messages(parallel), /share declared write paths/);
  assert.match(messages(example.replace(/^Parallel\. .+$/m, 'Parallel. PR-01, PR-99.')), /unknown PR PR-99/);
  assert.match(messages(example.replace(/^Parallel\. .+$/m, 'Parallel. None.')), /at least two/);
});
test('rejects transitive dependencies inside a declared parallel wave', () => {
  const third = pr.replaceAll('PR-01', 'PR-03').replace('**Depends on.** None.', '**Depends on.** PR-02.');
  const three = two.replace('## Close the program', third + '## Close the program').replace(/^Parallel\. .+$/m, 'Parallel. PR-01, PR-03.');
  assert.match(messages(three), /have a dependency/);
});
test('requires sensitivity and non-author Behavior verification', () => {
  assert.match(messages(example.replace(/^Sensitivity\. .+$/m, '')), /Sensitivity/);
  assert.match(messages(example.replace('Verifier. Independent.', 'Verifier. Self.')), /Behavior needs Verifier/);
  assert.deepEqual(checkPlan(docsPlan().replace('Verifier. Independent.', 'Verifier. Review only.')).problems, []);
});
test('ignores frontmatter and fenced examples, preserving line numbers', () => {
  const text = `---\ntitle: Example\n---\n${example}\n\n~~~markdown\n## Fake PR\n{{not a template field}}\n~~~\n`;
  assert.deepEqual(checkPlan(text).problems, []);
  const broken = text.replace('Status. Ready.', 'Status. Draft.');
  assert.equal(checkPlan(broken).problems.find(p => p.message.includes('not Ready')).line, 8);
});
test('handles nested and longer code fences and rejects unclosed ones', () => {
  assert.deepEqual(checkPlan(`${example}\n\n  \`\`\`\`md\n\`\`\`md\n## Fake\n\`\`\`\n  \`\`\`\`\`\n`).problems, []);
  assert.match(messages(`${example}\n\`\`\`\n## ignored\n`), /unclosed code fence/);
  assert.match(messages(`---\ntitle: broken\n${example}`), /unclosed frontmatter/);
});
test('CLI reports valid/invalid/read-error exit codes and never rewrites input', t => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'multi-phase-plan-test-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const file = path.join(dir, 'plan with spaces.md');
  const run = args => spawnSync(process.execPath, [path.join(here, 'check-plan.mjs'), ...args], { encoding: 'utf8' });
  fs.writeFileSync(file, example);
  assert.equal(run([file]).status, 0);
  assert.equal(fs.readFileSync(file, 'utf8'), example);
  fs.writeFileSync(file, example.replace('Status. Ready.', 'Status. Draft.'));
  assert.equal(run([file]).status, 1);
  assert.equal(run([path.join(dir, 'missing.md')]).status, 2);
  assert.equal(run([]).status, 2);
  assert.equal(run(['--help']).status, 0);
});
