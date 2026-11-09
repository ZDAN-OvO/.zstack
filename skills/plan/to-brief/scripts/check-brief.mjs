#!/usr/bin/env node
// 校验 /to-brief 产出的 brief 文档格式，只接受 SKILL.md 里的模板，不接受任意 Markdown。
// 用法：node check-brief.mjs [local/briefs/<topic>.md ...]
// 不带参数时校验当前目录下 local/briefs/*.md。无依赖。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const STAGES = ["think", "explore", "decide", "execute"];
export const SLOTS = ["Goal", "Context", "Materials", "Boundaries", "Done"];
export const OPTIONAL = ["Assumptions", "Open questions"];
const MAX_BULLETS = 5;

// 模板残留：尖括号占位、HTML 注释、TODO 类标记
const PLACEHOLDER = /<!--|<(?:one-line outcome|topic|think \|[^>]*|the user's original request[^>]*)>/i;
// 大小写敏感：小写 todo 是普通词（如 Todo 工具），只有全大写标记才算残留
const MARKER = /\b(?:TODO|TBD|FIXME)\b/;
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*\.md$/;
const BULLET = /^- \S/;
const CONTINUATION = /^ {2,}\S/;

/** 返回 { problems: [{ line, message, rule }] }；file 只用于校验文件名。 */
export function checkBrief(text, file = "") {
  const problems = [];
  const fail = (line, message, rule) => problems.push({ line, message, rule });
  const lines = text.split(/\r?\n/);

  if (file) {
    const base = path.basename(file);
    if (!SLUG.test(base)) fail(1, `file name "${base}" is not a kebab-case slug ending in .md`, "slug");
    if (!/(^|[\\/])local[\\/]briefs[\\/][^\\/]+$/.test(path.resolve(file))) fail(1, "brief must live in local/briefs/", "location");
  }

  // 第一行：标题
  if (!/^# Brief: \S/.test(lines[0] ?? "")) fail(1, 'first line must be "# Brief: <one-line outcome>"', "title");

  // 按 H2 切段；代码块里的内容不参与结构判断
  const sections = [];
  const preamble = [];
  let current = null;
  let fence = null;
  for (let i = 1; i < lines.length; i++) {
    const raw = lines[i];
    const n = i + 1;
    if (PLACEHOLDER.test(raw) || MARKER.test(raw)) fail(n, "template placeholder left in the brief", "placeholder");
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
    const h2 = raw.match(/^## (.+?)\s*$/);
    if (h2) {
      current = { name: h2[1], n, body: [] };
      sections.push(current);
      continue;
    }
    if (/^#{1,6} /.test(raw)) {
      fail(n, `unexpected heading "${raw.trim()}"; only "# Brief:" and the slot H2s are allowed`, "heading");
      continue;
    }
    (current?.body ?? preamble).push({ raw, n });
  }
  if (fence) fail(lines.length, "unclosed code fence", "fence");

  checkMeta(preamble, fail);
  checkOrder(sections, fail);
  for (const s of sections) checkBody(s, fail);
  return { problems };
}

// 标题与第一个 H2 之间只能是 Stage、Source 两条
function checkMeta(preamble, fail) {
  const content = preamble.filter((l) => l.raw.trim() !== "");
  const stage = content[0];
  const source = content[1];
  const sm = stage?.raw.match(/^- Stage: (\S+)\s*$/);
  if (!sm) fail(stage?.n ?? 2, 'expected "- Stage: <think | explore | decide | execute>" after the title', "meta");
  else if (!STAGES.includes(sm[1])) fail(stage.n, `stage "${sm[1]}" is not one of ${STAGES.join(", ")}`, "stage");
  if (!/^- Source: \S/.test(source?.raw ?? "")) fail(source?.n ?? 3, 'expected "- Source: <original request>" after Stage', "meta");
  for (const extra of content.slice(2)) fail(extra.n, "only Stage and Source may sit between the title and ## Goal", "meta");
}

// 五个必填栏按序出现；可选栏只能在其后且按序；不得重复或出现未知栏
function checkOrder(sections, fail) {
  const allowed = [...SLOTS, ...OPTIONAL];
  const seen = new Set();
  let last = -1;
  for (const s of sections) {
    const idx = allowed.indexOf(s.name);
    if (idx < 0) {
      fail(s.n, `unknown section "## ${s.name}"; allowed: ${allowed.join(", ")}`, "section");
      continue;
    }
    if (seen.has(s.name)) fail(s.n, `duplicate section "## ${s.name}"`, "section");
    else if (idx < last) fail(s.n, `"## ${s.name}" is out of order; expected ${allowed.join(" → ")}`, "order");
    seen.add(s.name);
    last = Math.max(last, idx);
  }
  for (const slot of SLOTS) if (!seen.has(slot)) fail(1, `missing required section "## ${slot}"`, "missing");
}

// 每栏内容只能是顶层 "- " 条目及其缩进续行；必填栏 1–5 条，可选栏存在则不能为空
function checkBody(section, fail) {
  if (![...SLOTS, ...OPTIONAL].includes(section.name)) return;
  let bullets = 0;
  for (const l of section.body) {
    if (l.fenced || l.raw.trim() === "") continue;
    if (BULLET.test(l.raw)) bullets++;
    else if (CONTINUATION.test(l.raw) && bullets > 0) continue;
    else fail(l.n, `"## ${section.name}" content must be "- " bullets (indent continuation lines)`, "prose");
  }
  if (bullets === 0) {
    const hint = OPTIONAL.includes(section.name) ? "; omit an empty optional section" : "";
    fail(section.n, `"## ${section.name}" has no bullets${hint}`, "empty");
  } else if (SLOTS.includes(section.name) && bullets > MAX_BULLETS) {
    fail(section.n, `"## ${section.name}" has ${bullets} bullets; keep it to ${MAX_BULLETS}`, "length");
  }
}

function main(argv) {
  let files = argv;
  if (files.length === 0) {
    const dir = path.join(process.cwd(), "local", "briefs");
    files = fs.existsSync(dir)
      ? fs.readdirSync(dir).filter((f) => f.endsWith(".md")).map((f) => path.join("local", "briefs", f))
      : [];
    if (files.length === 0) {
      console.error("no briefs found: pass a path or run from a directory with local/briefs/*.md");
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
    const { problems } = checkBrief(fs.readFileSync(file, "utf8"), file);
    for (const p of problems.sort((a, b) => a.line - b.line)) console.log(`${file}:${p.line}: ${p.message} [${p.rule}]`);
    total += problems.length;
  }
  console.log(total === 0 ? `${files.length} brief(s) ok` : `${total} problem${total === 1 ? "" : "s"} found`);
  return total === 0 ? 0 : 1;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  process.exitCode = main(process.argv.slice(2));
}
