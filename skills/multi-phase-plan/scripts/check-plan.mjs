#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const BLOCKS = ['Depends on.', 'Files.', 'Build.', 'You see.', 'Verify, unit.', 'Verify, live.', 'Verify, perf.', 'Review gate.', 'Merge.'];
const PREFIX = ['How to read this', 'Program checklist'];
const SUFFIX = ['Close the program', 'Appendix A. Spike evidence', 'Appendix B. Alternatives rejected', 'Appendix C. Risks', 'Appendix D. Links and decisions'];
const PROGRAM = ['Start and sequence', 'Evidence rules', 'Boot recipe', 'Verdict and handoff'];
const BOX = /^\s*- \[([ xX])\] (.+)$/;
const PLACEHOLDER = /\{\{[^}]*\}\}|\b(?:TODO|TBD|FIXME)\b|<(?:(?:path|command|predicate|program|head SHA|head-branch|topic|pr id|metric|value|slug|surface|artifact|budget|port|number|unit)(?:\b[^>]*))>/i;

// This parser intentionally accepts the documented template, not arbitrary Markdown.
function proseLines(text, fail) {
  const raw = text.split(/\r?\n/);
  let start = 0;
  if (raw[0] === '---') {
    const end = raw.indexOf('---', 1);
    if (end < 0) fail(1, 'unclosed frontmatter');
    else start = end + 1;
  }
  const lines = [];
  let fence = null;
  for (let i = start; i < raw.length; i++) {
    const text = raw[i];
    if (fence) {
      const close = text.match(/^ {0,3}(`+|~+)[ \t]*$/);
      if (close && close[1][0] === fence.char && close[1].length >= fence.length) fence = null;
      continue;
    }
    const open = text.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
    if (open && !(open[1][0] === '`' && open[2].includes('`'))) {
      fence = { char: open[1][0], length: open[1].length, line: i + 1 };
      continue;
    }
    lines.push({ text, n: i + 1 });
  }
  if (fence) fail(fence.line, 'unclosed code fence');
  return lines;
}

export function checkPlan(text) {
  const problems = [];
  const fail = (line, message) => problems.push({ line, message });
  const lines = proseLines(text, fail);
  const sections = [];
  for (const line of lines) {
    const h = /^## (.+)$/.exec(line.text);
    if (h) sections.push({ title: h[1].trim(), n: line.n, body: [] });
    else if (sections.length) sections.at(-1).body.push(line);
    if (PLACEHOLDER.test(line.text)) fail(line.n, 'unfilled placeholder or unresolved TODO/TBD/FIXME');
  }
  if (lines.filter(l => /^# /.test(l.text)).length !== 1) fail(1, 'expected one H1 title');
  const prs = sections.filter(s => /^PR-\d+\b/.test(s.title));
  const expected = [...PREFIX, ...prs.map(s => s.title), ...SUFFIX];
  if (sections.map(s => s.title).join('|') !== expected.join('|')) fail(1, 'H2 sections must follow the template order, with PR sections between Program checklist and Close the program');
  if (!prs.length) fail(1, 'no PR sections');
  const section = title => sections.find(s => s.title === title);
  const content = s => (s?.body ?? []).map(l => l.text).join('\n');
  const meaningful = value => value.trim().length > 0 && !/^(?:none|n\/a|not applicable)[.!]?$/i.test(value.trim());
  const requireField = (s, name) => {
    const matches = (s?.body ?? []).filter(l => l.text.startsWith(`${name}. `));
    if (matches.length !== 1 || !(matches[0]?.text.slice(name.length + 2).trim())) fail(s?.n ?? 1, `expected one nonempty ${name}. field`);
    return matches[0]?.text.slice(name.length + 2).trim() ?? '';
  };
  const how = section('How to read this');
  if (requireField(how, 'Status') !== 'Ready.') fail(how?.n ?? 1, 'plan is not Ready; resolve blockers before readiness checking');
  if (requireField(how, 'Blockers') !== 'None.') fail(how?.n ?? 1, 'ready plan must declare Blockers. None.');
  for (const name of ['Execution', 'Roles', 'Permissions']) requireField(how, name);
  const program = section('Program checklist');
  const subheads = (program?.body ?? []).filter(l => /^### /.test(l.text)).map(l => l.text.slice(4).trim());
  if (subheads.join('|') !== PROGRAM.join('|')) fail(program?.n ?? 1, 'Program checklist must include the four template H3 sections in order');
  for (const name of PROGRAM) {
    const body = program?.body ?? [];
    const at = body.findIndex(l => l.text === `### ${name}`);
    const end = body.findIndex((l, i) => i > at && /^### /.test(l.text));
    const chunk = at < 0 ? '' : body.slice(at + 1, end < 0 ? undefined : end).map(l => l.text).join('\n');
    if (!meaningful(chunk)) fail(program?.n ?? 1, `empty program subsection ${name}`);
  }
  for (const name of ['Versions', 'Invalidation', 'Input boundary', 'Feasibility', 'Acceptance', 'Changes', 'Review entity', 'Verdict']) {
    if (!meaningful(requireField(program, name))) fail(program?.n ?? 1, `${name}. needs a specific contract, not None`);
  }
  const parallelText = requireField(program, 'Parallel');
  const parallelGroups = [];
  if (/^None\.\s+\S/.test(parallelText)) {
    // A sequential program still needs an explicit reason.
  } else {
    for (const group of parallelText.replace(/\.$/, '').split(/;\s*/)) {
      const members = group.split(/,\s*/);
      if (members.length < 2 || members.some(id => !/^PR-\d+$/.test(id)) || new Set(members).size !== members.length) {
        fail(program?.n ?? 1, 'Parallel. must name groups of at least two unique PR IDs, or None. with a reason');
      } else parallelGroups.push(members);
    }
  }
  for (const title of SUFFIX) if (!meaningful(content(section(title)))) fail(section(title)?.n ?? 1, `${title} needs content or a reason`);

  const graph = new Map();
  const writes = new Map();
  const ids = new Set();
  for (const pr of prs) {
    const id = pr.title.match(/^PR-\d+/)[0];
    if (ids.has(id)) fail(pr.n, `duplicate PR ID ${id}`);
    ids.add(id);
    const blocks = [];
    for (const l of pr.body) {
      const m = /^\*\*([^*]+)\*\*(.*)$/.exec(l.text);
      if (m) blocks.push({ name: m[1], rest: m[2].trim(), n: l.n, body: [] });
      else if (blocks.length) blocks.at(-1).body.push(l);
      else if (l.text.trim()) fail(l.n, `${id}: content before Depends on.`);
    }
    if (blocks.map(b => b.name).join('|') !== BLOCKS.join('|')) fail(pr.n, `${id}: expected the nine PR blocks in template order`);
    const get = name => blocks.find(b => b.name === name);
    const boxes = b => (b?.body ?? []).filter(l => BOX.test(l.text)).map(l => ({ ...l, check: l.text.match(BOX)[1], value: l.text.match(BOX)[2] }));
    const depends = get('Depends on.');
    const depText = depends?.rest ?? '';
    let deps = [];
    if (depText !== 'None.') {
      const names = depText.replace(/\.$/, '').split(/,\s*/);
      if (!names.length || names.some(d => !/^PR-\d+$/.test(d))) fail(depends?.n ?? pr.n, `${id}: Depends on must be None. or comma-separated PR IDs`);
      else deps = names;
    }
    graph.set(id, deps);
    const files = get('Files.');
    const base = requireField(files, 'Base');
    if (base !== 'Trunk.' && (!/^PR-\d+\.$/.test(base) || !deps.includes(base.slice(0, -1)))) fail(files?.n ?? pr.n, `${id}: Base must be Trunk. or a declared prerequisite PR ID followed by a period`);
    const ownership = requireField(files, 'Writes');
    const paths = [...ownership.matchAll(/`([^`\n]+)`/g)].map(m => m[1].replace(/^\.\//, '').replace(/\/$/, ''));
    if (!paths.length || paths.some(p => !p.trim())) fail(files?.n ?? pr.n, `${id}: Writes needs backticked owned paths/globs`);
    writes.set(id, paths);
    for (const field of ['Resources', 'Contract']) if (!meaningful(requireField(files, field))) fail(files?.n ?? pr.n, `${id}: ${field} needs an isolation/compatibility contract or specific reason`);
    for (const b of blocks) {
      for (const box of boxes(b)) {
        if (box.check !== ' ') fail(box.n, `${id}: future implementation boxes must be unchecked`);
        if (!box.value.match(/Evidence\. `([^`\n]+)`/)?.[1].trim()) fail(box.n, `${id}: each box needs Evidence. followed by a backticked destination`);
      }
    }
    for (const name of ['Files.', 'Build.', 'You see.', 'Merge.']) if (!boxes(get(name)).length) fail(pr.n, `${id}: ${name} needs at least one box`);
    const see = get('You see.');
    const kind = requireField(see, 'Kind');
    if (!['Behavior.', 'Docs.'].includes(kind)) fail(see?.n ?? pr.n, `${id}: Kind must be Behavior. or Docs.`);
    const surfacesText = requireField(see, 'Surfaces');
    const surfaces = surfacesText.replace(/\.$/, '').split(/,\s*/).filter(Boolean);
    const interaction = requireField(see, 'Interaction');
    if (!['Yes.', 'No.'].includes(interaction)) fail(see?.n ?? pr.n, `${id}: Interaction must be Yes. or No.`);
    if (kind === 'Behavior.' && (!surfaces.length || surfaces.includes('None'))) fail(see?.n ?? pr.n, `${id}: behavior needs named surfaces`);
    if (kind === 'Docs.' && (surfacesText !== 'None.' || interaction !== 'No.')) fail(see?.n ?? pr.n, `${id}: Docs uses Surfaces. None. and Interaction. No.`);
    const applicability = name => {
      const b = get(name);
      if (b?.rest === 'Required.') return true;
      const m = /^Not applicable\. (.+)$/.exec(b?.rest ?? '');
      if (!m || !meaningful(m[1])) fail(b?.n ?? pr.n, `${id}: ${name} must be Required. or Not applicable. with a specific reason`);
      if (boxes(b).length) fail(b?.n ?? pr.n, `${id}: non-applicable ${name} cannot have boxes`);
      return false;
    };
    const unit = applicability('Verify, unit.');
    const live = applicability('Verify, live.');
    const perf = applicability('Verify, perf.');
    const review = applicability('Review gate.');
    if (kind === 'Behavior.' && (!unit || !live)) fail(pr.n, `${id}: behavior requires automated and live verification`);
    if ((interaction === 'Yes.') !== review) fail(pr.n, `${id}: Review gate must match Interaction`);
    if (kind === 'Behavior.' && !meaningful(requireField(get('Verify, unit.'), 'Sensitivity'))) fail(pr.n, `${id}: critical checks need a Sensitivity contract`);
    const verifier = requireField(get('Merge.'), 'Verifier');
    if (kind === 'Behavior.' ? verifier !== 'Independent.' : !['Independent.', 'Review only.'].includes(verifier)) fail(pr.n, `${id}: Behavior needs Verifier. Independent.; Docs needs Independent. or Review only.`);
    for (const name of ['Verify, unit.', 'Verify, live.']) {
      const required = name === 'Verify, unit.' ? unit : live;
      if (!required) continue;
      const checks = boxes(get(name));
      if (!checks.length) fail(pr.n, `${id}: ${name} needs scenarios`);
      for (const box of checks) if (!/Pass when\s+\S/.test(box.value)) fail(box.n, `${id}: verification scenario needs Pass when`);
    }
    if (live) {
      const checks = boxes(get('Verify, live.'));
      if (!checks.some(b => b.value.includes('Regression against trunk.'))) fail(pr.n, `${id}: live verification needs Regression against trunk.`);
      for (const surface of surfaces) {
        if (surface !== 'None' && !checks.some(b => b.value.includes(`Surface. ${surface}.`))) fail(pr.n, `${id}: live verification does not cover surface ${surface}`);
      }
    }
    if (perf) {
      const checks = boxes(get('Verify, perf.'));
      const labels = checks.map(b => b.value.split(' ')[0]);
      if (labels.join('|') !== 'Metric.|Probe.|Baseline.|Rule.') fail(pr.n, `${id}: perf requires Metric, Probe, Baseline, Rule boxes in order`);
      const rule = checks.find(b => b.value.startsWith('Rule.'));
      if (rule && !/Limit\. \d+(?:\.\d+)?\s+[^\s.]+/.test(rule.value)) fail(rule.n, `${id}: perf Rule needs Limit. followed by a number and unit`);
    }
    if (review) {
      const checks = boxes(get('Review gate.'));
      const text = checks.map(b => b.value).join('\n');
      if (!checks.length || !['screenshots', 'video', 'operator', 'approval'].every(w => text.includes(w))) fail(pr.n, `${id}: review needs screenshots, video, operator, and approval`);
    }
  }
  for (const [id, deps] of graph) for (const dep of deps) {
    if (!ids.has(dep)) fail(prs.find(p => p.title.startsWith(`${id} `))?.n ?? 1, `${id}: unknown dependency ${dep}`);
    if (dep === id) fail(1, `${id}: self-dependency`);
  }
  const visiting = new Set();
  const done = new Set();
  function visit(id) {
    if (visiting.has(id)) { fail(1, `dependency cycle at ${id}`); return; }
    if (done.has(id)) return;
    visiting.add(id);
    for (const dep of graph.get(id) ?? []) if (ids.has(dep)) visit(dep);
    visiting.delete(id);
    done.add(id);
  }
  for (const id of ids) visit(id);
  function dependsOn(id, target, seen = new Set()) {
    if (seen.has(id)) return false;
    seen.add(id);
    return (graph.get(id) ?? []).some(dep => dep === target || dependsOn(dep, target, seen));
  }
  for (const group of parallelGroups) {
    for (const id of group) if (!ids.has(id)) fail(program?.n ?? 1, `Parallel: unknown PR ${id}`);
    for (let i = 0; i < group.length; i++) for (let j = i + 1; j < group.length; j++) {
      const a = group[i], b = group[j];
      if (dependsOn(a, b) || dependsOn(b, a)) fail(program?.n ?? 1, `Parallel: ${a} and ${b} have a dependency`);
      const overlap = (writes.get(a) ?? []).filter(p => (writes.get(b) ?? []).includes(p));
      if (overlap.length) fail(program?.n ?? 1, `Parallel: ${a} and ${b} share declared write paths: ${overlap.join(', ')}`);
    }
  }
  return { prCount: prs.length, problems };
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 1 && args[0] === '--help') {
    console.log('Usage: node check-plan.mjs <plan.md>\nChecks readiness structure, not feasibility or evidence truth. Exit 0 valid, 1 invalid, 2 usage/read error.');
    return;
  }
  if (args.length !== 1 || args[0].startsWith('-')) {
    console.error('Usage: node check-plan.mjs <plan.md>');
    process.exitCode = 2;
    return;
  }
  let text;
  try { text = fs.readFileSync(args[0], 'utf8'); }
  catch (error) { console.error(`${args[0]}: ${error.message}`); process.exitCode = 2; return; }
  const { prCount, problems } = checkPlan(text);
  for (const { line, message } of problems) console.error(`${args[0]}:${line}: ${message}`);
  console.log(`${prCount} PR sections, ${problems.length} problems`);
  process.exitCode = problems.length ? 1 : 0;
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) main();
