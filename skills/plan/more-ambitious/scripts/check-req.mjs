#!/usr/bin/env node
// 校验 /more-ambitious 产出的需求文档格式，只接受 SKILL.md 里的模板，不接受任意 Markdown。
// 用法：node check-req.mjs [local/reqs/<topic>.md ...]
// 不带参数时校验当前目录下 local/reqs/*.md。无依赖。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const REQUIRED = ["Requirement", "Ladder"];
export const OPTIONAL = ["Deeper", "Wider"];
export const TRIALS = "Trials";
export const SECTIONS = [...REQUIRED, ...OPTIONAL, TRIALS];
export const LADDER_HEADER = ["Rung", "Goal", "AI owns", "Needs", "Status"];
export const STATUSES = ["handed", "accepted", "rejected"];
export const VERDICTS = ["accepted", "rejected"];

// 模板残留：SKILL.md 模板里的尖括号占位、HTML 注释、TODO 类标记
const PLACEHOLDER =
  /<!--|<(?:handed rung in a few words|request as (?:the user wrote it|written)|YYYY-MM-DD|the user's (?:restatement|words|verb)|what moved to AI|data, access, checks|N|holds \|[^>]*|suggestion[^>]*|noun|field: technique|technique[^>]*|what the user said fell short)>/i;
// Case-sensitive: "todo" is an ordinary word (e.g. a Todo tool); only the all-caps marker is a leftover.
const MARKER = /\b(?:TODO|TBD|FIXME)\b/;
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*\.md$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const BULLET = /^- \S/;
const CONTINUATION = /^ {2,}\S/;
const TRIAL = /^### (\d{4}-\d{2}-\d{2}) · rung (\d+) · (\S+)\s*$/;

/** 返回 { problems: [{ line, message, rule }] }；file 只用于校验文件名和位置。 */
export function checkReq(text, file = "") {
  const problems = [];
  const fail = (line, message, rule) => problems.push({ line, message, rule });
  const lines = text.split(/\r?\n/);

  if (file) {
    const base = path.basename(file);
    if (!SLUG.test(base)) fail(1, `file name "${base}" is not a kebab-case slug ending in .md`, "slug");
    if (!/(^|[\\/])local[\\/]reqs[\\/][^\\/]+$/.test(path.resolve(file))) fail(1, "requirement must live in local/reqs/", "location");
  }

  if (!/^# Requirement: \S/.test(lines[0] ?? "")) fail(1, 'first line must be "# Requirement: <handed rung in a few words>"', "title");

  // 按 H2 切段；代码块里的内容不参与结构判断；H3 只允许出现在 Trials 里
  const sections = [];
  const preamble = [];
  let current = null;
  let fence = null;
  for (let i = 1; i < lines.length; i++) {
    const raw = lines[i];
    const n = i + 1;
    const fenceMark = raw.match(/^\s*(`{3,}|~{3,})/);
    if (fence) {
      if (fenceMark && fenceMark[1][0] === fence[0] && fenceMark[1].length >= fence.length) fence = null;
      (current?.body ?? preamble).push({ raw, n, fenced: true });
      continue;
    }
    if (fenceMark) {
      fence = fenceMark[1];
      (current?.body ?? preamble).push({ raw, n, fenced: true });
      continue;
    }
    if (PLACEHOLDER.test(raw) || MARKER.test(raw)) fail(n, "template placeholder left in the requirement", "placeholder");
    const h2 = raw.match(/^## (.+?)\s*$/);
    if (h2) {
      current = { name: h2[1], n, body: [] };
      sections.push(current);
      continue;
    }
    if (/^### /.test(raw) && current?.name === TRIALS) {
      current.body.push({ raw, n });
      continue;
    }
    if (/^#{1,6} /.test(raw)) {
      fail(n, `unexpected heading "${raw.trim()}"; only "# Requirement:", the section H2s and Trials entries are allowed`, "heading");
      continue;
    }
    (current?.body ?? preamble).push({ raw, n });
  }
  if (fence) fail(lines.length, "unclosed code fence", "fence");

  checkMeta(preamble, fail);
  checkOrder(sections, fail);
  const ladder = sections.find((s) => s.name === "Ladder");
  const rungs = ladder ? checkLadder(ladder, fail) : null;
  for (const s of sections) {
    if (s.name === "Requirement") checkRequirement(s, fail);
    else if (s.name === "Deeper") checkFields(s, ["Premise"], ["Kept", "Dropped"], fail);
    else if (s.name === "Wider") checkFields(s, ["Noun → verb"], ["Borrowed", "Dropped"], fail);
    else if (s.name === TRIALS) checkTrials(s, rungs, fail);
  }
  return { problems };
}

// 标题与第一个 H2 之间只能是 Source、Date 两条
function checkMeta(preamble, fail) {
  const content = preamble.filter((l) => l.raw.trim() !== "");
  const [source, date] = content;
  if (!/^- Source: \S/.test(source?.raw ?? "")) fail(source?.n ?? 2, 'expected "- Source: <request as the user wrote it>" after the title', "meta");
  const dm = date?.raw.match(/^- Date: (\S+)\s*$/);
  if (!dm) fail(date?.n ?? 3, 'expected "- Date: <YYYY-MM-DD>" after Source', "meta");
  else if (!DATE.test(dm[1])) fail(date.n, `date "${dm[1]}" is not YYYY-MM-DD`, "date");
  for (const extra of content.slice(2)) fail(extra.n, "only Source and Date may sit between the title and ## Requirement", "meta");
}

// 段落按 Requirement → Ladder → Deeper → Wider → Trials 出现；前两段和 Trials 必有，不得重复或未知
function checkOrder(sections, fail) {
  const seen = new Set();
  let last = -1;
  for (const s of sections) {
    const idx = SECTIONS.indexOf(s.name);
    if (idx < 0) {
      fail(s.n, `unknown section "## ${s.name}"; allowed: ${SECTIONS.join(", ")}`, "section");
      continue;
    }
    if (seen.has(s.name)) fail(s.n, `duplicate section "## ${s.name}"`, "section");
    else if (idx < last) fail(s.n, `"## ${s.name}" is out of order; expected ${SECTIONS.join(" → ")}`, "order");
    seen.add(s.name);
    last = Math.max(last, idx);
  }
  for (const name of [...REQUIRED, TRIALS]) if (!seen.has(name)) fail(1, `missing required section "## ${name}"`, "missing");
}

// Requirement 是用户的复述，不能为空
function checkRequirement(section, fail) {
  if (!section.body.some((l) => l.raw.trim() !== "")) fail(section.n, '"## Requirement" is empty; write the user\'s restatement', "empty");
}

const cells = (raw) => raw.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

// 阶梯表：固定表头，rung 从 0 连续编号，rung 0 只写原话；恰好一层 handed，或交出层已 accepted；
// 表后一行 "Handed over: rung N"，N 指向表内的 handed 或 accepted 层
function checkLadder(section, fail) {
  const body = section.body.filter((l) => !l.fenced && l.raw.trim() !== "");
  const table = body.filter((l) => l.raw.trim().startsWith("|"));
  const rest = body.filter((l) => !l.raw.trim().startsWith("|"));
  const rungs = new Map();

  if (table.length < 3) {
    fail(section.n, '"## Ladder" needs the table header, separator and at least rung 0 and rung 1', "ladder");
    return rungs;
  }
  if (cells(table[0].raw).join("|") !== LADDER_HEADER.join("|")) {
    fail(table[0].n, `ladder header must be | ${LADDER_HEADER.join(" | ")} |`, "ladder");
  }
  if (!cells(table[1].raw).every((c) => /^:?-{3,}:?$/.test(c)) || cells(table[1].raw).length !== LADDER_HEADER.length) {
    fail(table[1].n, "second ladder row must be the separator |---|---|---|---|---|", "ladder");
  }
  table.slice(2).forEach((row, i) => {
    const c = cells(row.raw);
    if (c.length !== LADDER_HEADER.length) {
      fail(row.n, `ladder row has ${c.length} cells; expected ${LADDER_HEADER.length}`, "ladder");
      return;
    }
    const [rung, goal, owns, , status] = c;
    if (rung !== String(i)) fail(row.n, `rung "${rung}" breaks the numbering; expected ${i}`, "rung");
    if (!goal) fail(row.n, `rung ${rung} has no Goal`, "ladder");
    if (i === 0 && (owns || c[3] || status)) fail(row.n, "rung 0 is the request as written; leave AI owns, Needs and Status empty", "ladder");
    if (i > 0 && !owns) fail(row.n, `rung ${rung} has no "AI owns"`, "ladder");
    if (i > 0 && status && !STATUSES.includes(status)) fail(row.n, `status "${status}" is not one of ${STATUSES.join(", ")}`, "status");
    rungs.set(Number(rung), { status, n: row.n });
  });
  if (rungs.size < 2) fail(section.n, '"## Ladder" needs at least rung 0 and rung 1', "ladder");

  const handed = [...rungs].filter(([, r]) => r.status === "handed");
  if (handed.length > 1) fail(handed[1][1].n, "more than one rung is marked handed", "handed");

  const hm = rest.map((l) => ({ l, m: l.raw.match(/^Handed over: rung (\d+)\s*$/) })).filter((x) => x.m);
  if (hm.length !== 1) {
    fail(section.n, 'expected exactly one "Handed over: rung <N>" line after the ladder table', "handed");
  } else {
    const n = Number(hm[0].m[1]);
    const r = rungs.get(n);
    if (!r) fail(hm[0].l.n, `handed rung ${n} is not in the ladder`, "handed");
    else if (!["handed", "accepted"].includes(r.status)) fail(hm[0].l.n, `handed rung ${n} has status "${r.status || "empty"}"; expected handed or accepted`, "handed");
    else if (handed.length === 1 && handed[0][0] !== n) fail(hm[0].l.n, `"Handed over" names rung ${n}, but rung ${handed[0][0]} is marked handed`, "handed");
  }
  for (const l of rest) {
    if (!/^Handed over: rung \d+\s*$/.test(l.raw)) fail(l.n, '"## Ladder" holds only the table and the "Handed over" line', "prose");
  }
  return rungs;
}

// Deeper / Wider：只能是 "- 字段: 内容" 条目；首字段恰好一条且在最前，其余字段可多条
function checkFields(section, first, more, fail) {
  const keys = [...first, ...more];
  const counts = Object.fromEntries(keys.map((k) => [k, 0]));
  let bullets = 0;
  for (const l of section.body) {
    if (l.fenced || l.raw.trim() === "") continue;
    if (CONTINUATION.test(l.raw) && bullets > 0) continue;
    const m = l.raw.match(/^- ([^:]+): \S/);
    if (!BULLET.test(l.raw) || !m) {
      fail(l.n, `"## ${section.name}" content must be "- <${keys.join(" | ")}>: ..." bullets`, "prose");
      continue;
    }
    if (!keys.includes(m[1])) {
      fail(l.n, `unknown field "${m[1]}" in "## ${section.name}"; allowed: ${keys.join(", ")}`, "field");
      continue;
    }
    if (bullets === 0 && m[1] !== first[0]) fail(l.n, `"## ${section.name}" must start with "- ${first[0]}:"`, "field");
    bullets++;
    counts[m[1]]++;
  }
  for (const k of first) {
    if (counts[k] !== 1) fail(section.n, `"## ${section.name}" needs exactly one "- ${k}:" line`, "field");
  }
  if (bullets === 0) fail(section.n, `"## ${section.name}" has no bullets; omit the section when the leaf did not run`, "empty");
}

// Trials 可以为空；每条为 "### YYYY-MM-DD · rung N · accepted|rejected" 加至少一条 "- " 说明，rung 须在阶梯里
function checkTrials(section, rungs, fail) {
  let entry = null;
  const close = () => {
    if (entry && entry.bullets === 0) fail(entry.n, "trial entry needs at least one \"- \" line on what happened", "trial");
  };
  for (const l of section.body) {
    if (l.fenced || l.raw.trim() === "") continue;
    if (/^### /.test(l.raw)) {
      close();
      const m = l.raw.match(TRIAL);
      entry = { n: l.n, bullets: 0 };
      if (!m) {
        fail(l.n, 'trial heading must be "### YYYY-MM-DD · rung N · accepted|rejected"', "trial");
        continue;
      }
      if (!VERDICTS.includes(m[3])) fail(l.n, `trial verdict "${m[3]}" is not one of ${VERDICTS.join(", ")}`, "trial");
      if (rungs && rungs.size > 0 && !rungs.has(Number(m[2]))) fail(l.n, `trial names rung ${m[2]}, which is not in the ladder`, "trial");
      continue;
    }
    if (!entry) {
      fail(l.n, '"## Trials" content must sit under a "### YYYY-MM-DD · rung N · verdict" entry', "prose");
      continue;
    }
    if (BULLET.test(l.raw)) entry.bullets++;
    else if (!(CONTINUATION.test(l.raw) && entry.bullets > 0)) fail(l.n, "trial content must be \"- \" bullets", "prose");
  }
  close();
}

function main(argv) {
  let files = argv;
  if (files.length === 0) {
    const dir = path.join(process.cwd(), "local", "reqs");
    files = fs.existsSync(dir)
      ? fs.readdirSync(dir).filter((f) => f.endsWith(".md")).map((f) => path.join("local", "reqs", f))
      : [];
    if (files.length === 0) {
      console.error("no requirements found: pass a path or run from a directory with local/reqs/*.md");
      return 2;
    }
  }
  let total = 0;
  for (const file of files) {
    if (!fs.existsSync(file)) {
      console.error(`${file}: file not found`);
      total++;
      continue;
    }
    const { problems } = checkReq(fs.readFileSync(file, "utf8"), file);
    for (const p of problems.sort((a, b) => a.line - b.line)) console.log(`${file}:${p.line}: ${p.message} [${p.rule}]`);
    total += problems.length;
  }
  console.log(total === 0 ? `${files.length} requirement(s) ok` : `${total} problem${total === 1 ? "" : "s"} found`);
  return total === 0 ? 0 : 1;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  process.exitCode = main(process.argv.slice(2));
}
