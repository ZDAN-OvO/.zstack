# -*- coding: utf-8 -*-
"""构建 Q3 2026 QBR 演示文稿"""
import csv
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

# ---------------- 主题 ----------------
INK    = RGBColor(0x10, 0x23, 0x3A)
BODY   = RGBColor(0x33, 0x43, 0x55)
MUTED  = RGBColor(0x6B, 0x7C, 0x8F)
ACCENT = RGBColor(0x2E, 0x6F, 0x95)
RED    = RGBColor(0xC0, 0x45, 0x3F)
GREEN  = RGBColor(0x4C, 0x8C, 0x6B)
GOLD   = RGBColor(0xC9, 0x9A, 0x2E)
LIGHT  = RGBColor(0xF4, 0xF6, 0xF8)
RULE   = RGBColor(0xE3, 0xE8, 0xEE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

LATIN = "Arial"
EA    = "Microsoft YaHei"

W, H = 13.333, 7.5
ML, MR = 0.85, 0.85
CW = W - ML - MR

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
BLANK = prs.slide_layouts[6]

ROWS = list(csv.DictReader(open("data/q3-metrics.csv", encoding="utf-8")))
REV = [int(r["revenue_usd"]) for r in ROWS]
NEW = [int(r["new_customers"]) for r in ROWS]
CHURN = [int(r["churned_customers"]) for r in ROWS]
NPS = [int(r["nps"]) for r in ROWS]
TOT_REV = sum(REV)
TOT_NEW = sum(NEW)
TOT_CH = sum(CHURN)
NET = [n - c for n, c in zip(NEW, CHURN)]


# ---------------- 基础工具 ----------------
def set_font(run, size=14, bold=False, color=BODY, latin=LATIN, ea=EA, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = latin
    rPr = run._r.get_or_add_rPr()
    for tag, face in (("a:latin", latin), ("a:ea", ea), ("a:cs", latin)):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", face)
    return run


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tb


def para(tf, first=False, space_before=0, space_after=0, line=None, align=PP_ALIGN.LEFT):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if line:
        p.line_spacing = line
    return p


def bullet(p, char="▪", color=ACCENT, marL=0.26, indent=-0.26):
    pPr = p._pPr if p._pPr is not None else p._p.get_or_add_pPr()
    pPr.set("marL", str(Emu(Inches(marL)).emu if hasattr(Emu(Inches(marL)), "emu") else int(Inches(marL))))
    pPr.set("marL", str(int(Inches(marL))))
    pPr.set("indent", str(int(Inches(indent))))
    for tag in ("a:buClr", "a:buSzPct", "a:buFont", "a:buChar"):
        pPr.append(etree.SubElement(pPr, qn(tag)))
    buClr, buSz, buFont, buChar = (pPr.find(qn(t)) for t in
                                   ("a:buClr", "a:buSzPct", "a:buFont", "a:buChar"))
    srgb = etree.SubElement(buClr, qn("a:srgbClr"))
    srgb.set("val", str(color))
    buSz.set("val", "90000")
    buFont.set("typeface", "Arial")
    buChar.set("char", char)


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE, adj=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if adj is not None:
        try:
            s.adjustments[0] = adj
        except Exception:
            pass
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    s.shadow.inherit = False
    style = s._element.find(qn("p:style"))
    if style is not None:
        s._element.remove(style)
    s.text_frame.word_wrap = True
    return s


def hline(slide, x, y, w, color=RULE, lw=1.0):
    h = max(0.009, lw / 72.0)
    return rect(slide, x, y, w, h, fill=color)


PAGE = [0]


def new_slide(eyebrow=None, title=None, source=None):
    s = prs.slides.add_slide(BLANK)
    PAGE[0] += 1
    if title:
        tb = textbox(s, ML, 0.44, CW, 0.3)
        p = para(tb.text_frame, first=True)
        set_font(p.add_run(), size=11, bold=True, color=ACCENT)
        p.runs[0].text = eyebrow or ""
        tb2 = textbox(s, ML, 0.78, CW, 0.6)
        p2 = para(tb2.text_frame, first=True)
        r = p2.add_run()
        r.text = title
        set_font(r, size=29, bold=True, color=INK)
        hline(s, ML, 1.55, CW, RULE, 1.0)
    # 页脚
    ft = textbox(s, ML, 7.02, 6.0, 0.25)
    p = para(ft.text_frame, first=True)
    r = p.add_run()
    r.text = "2026 Q3 业务回顾  ·  内部"
    set_font(r, size=9.5, color=MUTED)
    pn = textbox(s, W - MR - 1.0, 7.02, 1.0, 0.25)
    p2 = para(pn.text_frame, first=True, align=PP_ALIGN.RIGHT)
    r2 = p2.add_run()
    r2.text = f"{PAGE[0]:02d}"
    set_font(r2, size=9.5, bold=True, color=INK)
    if source:
        st = textbox(s, ML, 6.72, CW, 0.25)
        p3 = para(st.text_frame, first=True)
        r3 = p3.add_run()
        r3.text = "注：" + source
        set_font(r3, size=9, color=MUTED)
    return s


def kpi(slide, x, y, w, h, label, value, sub, sub_color=MUTED, accent=ACCENT):
    rect(slide, x, y, w, h, fill=LIGHT)
    rect(slide, x, y, 0.055, h, fill=accent)
    tb = textbox(slide, x + 0.3, y + 0.24, w - 0.5, 0.3)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = label
    set_font(r, size=11, bold=True, color=MUTED)
    tb = textbox(slide, x + 0.3, y + 0.56, w - 0.5, 0.55)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = value
    set_font(r, size=27, bold=True, color=INK)
    tb = textbox(slide, x + 0.3, y + 1.14, w - 0.45, 0.5)
    p = para(tb.text_frame, first=True, line=1.15)
    r = p.add_run(); r.text = sub
    set_font(r, size=10.5, color=sub_color)


def bullets(slide, x, y, w, items, size=13, gap=11, line=1.38, color=BODY):
    tb = textbox(slide, x, y, w, 4.0)
    tf = tb.text_frame
    for i, it in enumerate(items):
        p = para(tf, first=(i == 0), space_after=gap, line=line)
        if isinstance(it, tuple):
            label, body = it
            r = p.add_run(); r.text = label
            set_font(r, size=size, bold=True, color=INK)
            r = p.add_run(); r.text = body
            set_font(r, size=size, color=color)
        else:
            r = p.add_run(); r.text = it
            set_font(r, size=size, color=color)
        bullet(p)
    return tb


# =====================================================================
# 1. 封面
# =====================================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, H, fill=ACCENT)
rect(s, 0.22, 0, W - 0.22, 0.14, fill=INK)

tb = textbox(s, 1.35, 1.62, 9.0, 0.3)
p = para(tb.text_frame, first=True)
r = p.add_run(); r.text = "2026 Q3  ·  QUARTERLY BUSINESS REVIEW"
set_font(r, size=12.5, bold=True, color=ACCENT)

tb = textbox(s, 1.3, 2.05, 10.0, 1.1)
p = para(tb.text_frame, first=True)
r = p.add_run(); r.text = "Q3 业务回顾"
set_font(r, size=54, bold=True, color=INK)

tb = textbox(s, 1.35, 3.22, 9.6, 0.9)
p = para(tb.text_frame, first=True, line=1.3)
r = p.add_run(); r.text = "收入小幅下滑，但增长引擎已经失速："
set_font(r, size=19, color=BODY)
r = p.add_run(); r.text = "净增近乎归零，NPS 跌破预警线"
set_font(r, size=19, bold=True, color=RED)

hline(s, 1.35, 4.42, 3.2, ACCENT, 3)

meta = [("汇报对象", "VP / 管理层"), ("汇报人", "产品与增长团队"), ("数据截止", "2026-09-30")]
for i, (k, v) in enumerate(meta):
    x = 1.35 + i * 2.6
    tb = textbox(s, x, 5.55, 2.4, 0.25)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = k
    set_font(r, size=10, bold=True, color=MUTED)
    tb = textbox(s, x, 5.85, 2.4, 0.3)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = v
    set_font(r, size=12.5, color=INK)

# =====================================================================
# 2. 执行摘要
# =====================================================================
s = new_slide("EXECUTIVE SUMMARY", "一页结论：收入是「慢性下滑」，客户与体验才是「急症」",
              source="收入为客户付费口径的月度合计；流失/新增比为当月流失数 ÷ 当月新增数。")

kw = (CW - 3 * 0.2) / 4
cards = [
    ("季度收入", f"${TOT_REV/1000:.0f}k", "7→9 月累计 -6.0%", RED, RED),
    ("新增客户", f"{TOT_NEW}", "41 → 35 → 30，逐月走低", MUTED, ACCENT),
    ("流失客户", f"{TOT_CH}", "12 → 24，两个月翻倍", RED, RED),
    ("NPS", f"{NPS[-1]}", "较 7 月 -11 分，已破 30", RED, RED),
]
for i, (l, v, sub, sc, ac) in enumerate(cards):
    kpi(s, ML + i * (kw + 0.2), 1.85, kw, 1.72, l, v, sub, sc, ac)

tb = textbox(s, ML, 3.88, CW, 0.62)
p = para(tb.text_frame, first=True, line=1.25)
r = p.add_run(); r.text = "一句话："
set_font(r, size=15, bold=True, color=INK)
r = p.add_run()
r.text = ("收入滑坡是结果，不是原因。真正在恶化的是「新增 − 流失」的转化效率："
          "9 月每 10 个新客户进来，就有 8 个老客户离开。")
set_font(r, size=15, color=BODY)

items = [
    ("收入：", "连续两个月环比下滑（-3.3%、-2.8%），季内累计 -6.0%。跌幅温和，但方向单一、无反弹迹象。"),
    ("客户：", "流失从 12 家升至 24 家，新增从 41 家降至 30 家，净增由 +29 掉到 +6——增长几乎停摆。"),
    ("体验：", "NPS 38 → 31 → 27 连续下滑并跌破 30 预警线；9 月起「太难上手」类工单明显增多。"),
    ("时间线：", "8 月中旬试用期由 14 天改为 7 天，与 9 月流失与投诉的抬升在时间上吻合（相关性，待验证）。"),
]
bullets(s, ML + 0.05, 4.72, CW - 0.1, items, size=12.5, gap=8, line=1.3)

# =====================================================================
# 3. 收入
# =====================================================================
s = new_slide("01 · 收入", "收入连续两月环比下滑，季内累计 -6.0%",
              source="月度收入取自 data/q3-metrics.csv；无 Q2 基线，故只能呈现季内环比。")
s.shapes.add_picture("chart_revenue.png", Inches(ML - 0.1), Inches(1.95), height=Inches(3.5))

# 右侧要点
px = 7.55
rect(s, px, 1.95, 0.045, 3.5, fill=RULE)
facts = [
    ("$529k", "季度合计收入"),
    ("-6.0%", "季内累计变化（7 月 → 9 月）"),
    ("-3.3% / -2.8%", "8 月、9 月环比"),
]
y = 2.0
for v, l in facts:
    tb = textbox(s, px + 0.35, y, 4.4, 0.45)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = v
    set_font(r, size=24, bold=True, color=INK if v != "-6.0%" else RED)
    tb = textbox(s, px + 0.35, y + 0.44, 4.4, 0.35)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = l
    set_font(r, size=11, color=MUTED)
    y += 1.02

tb = textbox(s, ML, 5.62, CW, 1.0)
p = para(tb.text_frame, first=True, line=1.35)
r = p.add_run(); r.text = "怎么看这件事："
set_font(r, size=13, bold=True, color=INK)
r = p.add_run()
r.text = ("单看收入，这只是一个 -6% 的「温和季度」，容易被解释为季节性波动。"
          "但收入 = 客户数 × 客单价，而客户净增已经从 +29 掉到 +6——"
          "如果净增不能止跌，Q4 的收入下滑会比 Q3 陡得多。")
set_font(r, size=12.5, color=BODY)

# =====================================================================
# 4. 客户
# =====================================================================
s = new_slide("02 · 客户", "新增在放缓，流失在翻倍：净增已被压缩到 +6",
              source="流失/新增比 = 当月流失客户数 ÷ 当月新增客户数；该比值接近 1 意味着增长基本停滞。")
s.shapes.add_picture("chart_customers.png", Inches(ML - 0.1), Inches(1.95), height=Inches(3.4))

px = 7.55
rect(s, px, 1.95, 0.045, 3.4, fill=RULE)
ratio = [c / n for c, n in zip(CHURN, NEW)]
facts = [("0.29 → 0.80", "流失 / 新增比（7 月 → 9 月）"),
         ("+29 → +6", "月度净增客户"),
         ("-48%", "新增客户三个月降幅（41 → 30）")]
y = 2.0
for v, l in facts:
    tb = textbox(s, px + 0.35, y, 4.4, 0.45)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = v
    set_font(r, size=23, bold=True, color=RED if "0.29" in v else INK)
    tb = textbox(s, px + 0.35, y + 0.44, 4.4, 0.4)
    p = para(tb.text_frame, first=True, line=1.1)
    r = p.add_run(); r.text = l
    set_font(r, size=11, color=MUTED)
    y += 1.02

tb = textbox(s, ML, 5.62, CW, 1.0)
p = para(tb.text_frame, first=True, line=1.35)
r = p.add_run(); r.text = "需要提醒 VP 的一点："
set_font(r, size=13, bold=True, color=RED)
r = p.add_run()
r.text = ("按 7→9 月的斜率线性外推，10 月的净增会接近 0、11 月转负。"
          "这不是预测，而是一个提醒——留给我们的止血窗口大概只有 4–6 周。")
set_font(r, size=12.5, color=BODY)

# =====================================================================
# 5. NPS
# =====================================================================
s = new_slide("03 · 体验", "NPS 三个月掉了 11 分，且已跌破 30 预警线",
              source="NPS 为月度调研结果；NPS 属滞后指标，其拐点通常晚于实际体验变化 1–2 个月。")
s.shapes.add_picture("chart_nps.png", Inches(ML - 0.1), Inches(2.02), height=Inches(3.25))

px = 7.55
rect(s, px, 2.0, 0.045, 3.1, fill=RULE)
tb = textbox(s, px + 0.35, 2.02, 4.5, 0.3)
p = para(tb.text_frame, first=True)
r = p.add_run(); r.text = "现场证据（来自团队工作日志）"
set_font(r, size=10.5, bold=True, color=MUTED)

ev = [
    ("9/8 起：", "客服工单中「太难上手」的投诉明显变多。"),
    ("8 月中：", "免费试用期由 14 天缩短为 7 天。"),
    ("10 月：", "NPS 仍有下行惯性，不动手大概率继续走低。"),
]
y = 2.42
for k, v in ev:
    tb = textbox(s, px + 0.35, y, 4.5, 0.75)
    p = para(tb.text_frame, first=True, line=1.3)
    r = p.add_run(); r.text = k
    set_font(r, size=12, bold=True, color=INK)
    r = p.add_run(); r.text = v
    set_font(r, size=12, color=BODY)
    y += 0.82

tb = textbox(s, ML, 5.62, CW, 1.0)
p = para(tb.text_frame, first=True, line=1.35)
r = p.add_run(); r.text = "结论："
set_font(r, size=13, bold=True, color=INK)
r = p.add_run()
r.text = ("流失、新增、NPS 三条曲线拐点几乎在同一个月（9 月）出现，"
          "说明这不是三个独立问题，而更可能是同一个体验问题在不同指标上的投影。")
set_font(r, size=12.5, color=BODY)

# =====================================================================
# 6. 归因
# =====================================================================
s = new_slide("04 · 归因", "主假设：试用期缩短 → 上手不足 → 早期流失",
              source="以下为基于现有数据的假设，尚未经客户访谈与分群验证，不作为定论呈现。")

# 时间线
ly = 2.52
hline(s, ML + 0.05, ly, CW - 0.1, RULE, 2)
tl = [
    ("8 月中", "试用期 14 天 → 7 天", ACCENT),
    ("9 月初", "「太难上手」工单上升", GOLD),
    ("9 月底", "流失 24 家 / NPS 27", RED),
]
xs = [ML + 1.28, ML + 5.82, W - MR - 1.28]
for i, (when, what, col) in enumerate(tl):
    cx = xs[i]
    rect(s, cx - 0.085, ly - 0.085, 0.17, 0.17, fill=col, shape=MSO_SHAPE.OVAL)
    tb = textbox(s, cx - 1.3, ly - 0.62, 2.6, 0.32)
    p = para(tb.text_frame, first=True, align=PP_ALIGN.CENTER)
    r = p.add_run(); r.text = when
    set_font(r, size=11, bold=True, color=col)
    tb = textbox(s, cx - 1.4, ly + 0.24, 2.8, 0.55)
    p = para(tb.text_frame, first=True, align=PP_ALIGN.CENTER, line=1.25)
    r = p.add_run(); r.text = what
    set_font(r, size=12.5, color=INK)

# 三个卡片
cy = 3.35
cw = (CW - 2 * 0.22) / 3
hyp = [
    ("主假设 · 置信度 中高", "试用期压缩过快", "7 天不足以让新用户完成「首次价值体验」。"
     "用户在还没感受到价值时就被要求付费，直接转化为早期流失。", ACCENT),
    ("待验证 · 置信度 低", "获客质量下降", "新增从 41 掉到 30，也可能是渠道结构变化带来的低意向流量。"
     "需要按渠道拆分新增客户的 30 天留存。", MUTED),
    ("待验证 · 置信度 低", "交付 / 服务能力瓶颈", "工单集中在「上手」环节，也可能是引导缺失或产品复杂度上升。"
     "需拆解工单类型与产品使用路径。", MUTED),
]
for i, (tag, head, body, col) in enumerate(hyp):
    x = ML + i * (cw + 0.22)
    h = 2.15
    rect(s, x, cy, cw, h, fill=LIGHT)
    rect(s, x, cy, cw, 0.045, fill=col)
    tb = textbox(s, x + 0.28, cy + 0.26, cw - 0.56, 0.25)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = tag
    set_font(r, size=9.5, bold=True, color=col)
    tb = textbox(s, x + 0.28, cy + 0.56, cw - 0.56, 0.32)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = head
    set_font(r, size=15, bold=True, color=INK)
    tb = textbox(s, x + 0.28, cy + 0.98, cw - 0.52, 1.0)
    p = para(tb.text_frame, first=True, line=1.3)
    r = p.add_run(); r.text = body
    set_font(r, size=11, color=BODY)

tb = textbox(s, ML, 5.78, CW, 0.7)
p = para(tb.text_frame, first=True, line=1.3)
r = p.add_run(); r.text = "要验证主假设，我们需要："
set_font(r, size=12, bold=True, color=INK)
r = p.add_run()
r.text = ("9 月流失客户中「注册时间 / 试用时长 / 是否完成关键动作 / 流失原因标签」四项数据。"
          "现有报表里没有这四项，建议本周由数据同学补一版。")
set_font(r, size=12, color=BODY)

# =====================================================================
# 7. Q4 计划
# =====================================================================
s = new_slide("05 · Q4 计划", "四件事止血：先把流失按住，再谈增长",
              source="目标值为团队内部提案，需与 VP 对齐后锁定；负责人为建议人选。")

rows = [
    ("1", "上手体验专项", "7 天试用内嵌入 3 步关键引导\n试用期策略做 A/B（7 天 vs 14 天 + 引导）",
     "10/15 上线", "11 月流失 ≤15 家/月", "产品 · 增长"),
    ("2", "流失原因闭环", "逐笔标注流失原因，9 月 24 家 100% 回访\n每周五固定流失复盘会",
     "本周启动", "100% 标签覆盖", "客服 · 数据"),
    ("3", "新增回暖", "渠道分层看板 + 30 天留存\n预算从低留存渠道转向高意向渠道",
     "10 月起周报", "新增回到 40+/月", "市场 · 销售"),
    ("4", "NPS 修复与监测", "NPS 拆到场景级，跌破 30 自动触发复盘\n不等季度末再处理",
     "11 月首份", "NPS ≥33", "产品 · 客服"),
]
head_y = 1.82
cols = [(ML, 0.45), (ML + 0.5, 2.15), (ML + 2.72, 4.20), (ML + 7.35, 1.35),
        (ML + 8.75, 1.65), (ML + 10.5, 1.1)]
heads = ["#", "举措", "具体动作", "时间", "衡量目标", "负责"]
for (x, w), h in zip(cols, heads):
    tb = textbox(s, x, head_y, w, 0.25)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = h
    set_font(r, size=10, bold=True, color=MUTED)
hline(s, ML, head_y + 0.3, CW, RULE, 1)

y = head_y + 0.42
for i, (n, name, act, when, goal, owner) in enumerate(rows):
    rh = 0.90
    if i % 2 == 0:
        rect(s, ML - 0.12, y - 0.08, CW + 0.24, rh, fill=LIGHT)
    tb = textbox(s, cols[0][0], y, 0.4, 0.3)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = n
    set_font(r, size=14, bold=True, color=ACCENT)
    tb = textbox(s, cols[1][0], y - 0.02, cols[1][1], 0.6)
    p = para(tb.text_frame, first=True, line=1.2)
    r = p.add_run(); r.text = name
    set_font(r, size=13, bold=True, color=INK)
    tb = textbox(s, cols[2][0], y - 0.02, cols[2][1], 0.8)
    for j, ln in enumerate(act.split("\n")):
        p = para(tb.text_frame, first=(j == 0), line=1.3)
        r = p.add_run(); r.text = ln
        set_font(r, size=11, color=BODY)
    for (x, w), txt, sz, bold, col in [
        (cols[3], when, 11, False, MUTED),
        (cols[4], goal, 11, True, INK),
        (cols[5], owner, 11, False, MUTED),
    ]:
        tb = textbox(s, x, y - 0.02, w, 0.8)
        p = para(tb.text_frame, first=True, line=1.2)
        r = p.add_run(); r.text = txt
        set_font(r, size=sz, bold=bold, color=col)
    y += rh

# 目标对比条
ty = 5.92
rect(s, ML - 0.12, ty, CW + 0.24, 0.98, fill=INK)
tb = textbox(s, ML + 0.16, ty + 0.34, 1.15, 0.3)
p = para(tb.text_frame, first=True)
r = p.add_run(); r.text = "Q4 目标"
set_font(r, size=11, bold=True, color=RGBColor(0x9F, 0xB6, 0xC8))
goals = [("月度净增", "+6 → ≥25"), ("流失/新增比", "0.80 → ≤0.35"),
         ("NPS", "27 → ≥33"), ("月均收入", "$176k → ≥$180k")]
for i, (k, v) in enumerate(goals):
    x = ML + 1.42 + i * 2.72
    tb = textbox(s, x, ty + 0.14, 2.6, 0.25)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = k
    set_font(r, size=9.5, color=RGBColor(0x9F, 0xB6, 0xC8))
    tb = textbox(s, x, ty + 0.42, 2.6, 0.4)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = v
    set_font(r, size=15, bold=True, color=WHITE)

# =====================================================================
# 8. 附录：月度明细
# =====================================================================
s = new_slide("APPENDIX", "附录：Q3 月度明细与数据说明")
heads = ["月份", "收入 (USD)", "环比", "新增客户", "流失客户", "净增", "NPS"]
cwid = [1.7, 2.0, 1.6, 1.9, 1.9, 1.5, 1.4]
y = 1.85
x = ML
for w, h in zip(cwid, heads):
    tb = textbox(s, x, y, w, 0.25)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = h
    set_font(r, size=10, bold=True, color=MUTED)
    x += w
hline(s, ML, y + 0.32, CW, RULE, 1)

y += 0.45
prev = None
for i, rw in enumerate(ROWS):
    vals = [rw["month"].replace("2026-", "2026 / "),
            f"${int(rw['revenue_usd']):,}",
            "—" if prev is None else f"{(int(rw['revenue_usd'])/prev-1)*100:+.1f}%",
            rw["new_customers"], rw["churned_customers"],
            f"+{int(rw['new_customers'])-int(rw['churned_customers'])}",
            rw["nps"]]
    prev = int(rw["revenue_usd"])
    x = ML
    for j, (w, v) in enumerate(zip(cwid, vals)):
        col = RED if j in (2, 4, 6) and v != "—" else INK
        tb = textbox(s, x, y, w, 0.3)
        p = para(tb.text_frame, first=True)
        r = p.add_run(); r.text = str(v)
        set_font(r, size=12, bold=(j in (1, 6)), color=col if j != 0 else INK)
        x += w
    y += 0.40
hline(s, ML, y + 0.04, CW, RULE, 1)
y += 0.14
tot = [("合计 / 期末", f"${TOT_REV:,}", "−6.0%", str(TOT_NEW), str(TOT_CH), f"+{TOT_NEW-TOT_CH}", str(NPS[-1]))]
x = ML
for j, (w, v) in enumerate(zip(cwid, tot[0])):
    tb = textbox(s, x, y, w, 0.32)
    p = para(tb.text_frame, first=True)
    r = p.add_run(); r.text = str(v)
    set_font(r, size=12, bold=True, color=INK if j != 2 else RED)
    x += w

# 数据说明
ny = 4.05
rect(s, ML - 0.12, ny, CW + 0.24, 2.45, fill=LIGHT)
tb = textbox(s, ML + 0.1, ny + 0.26, CW - 0.4, 0.3)
p = para(tb.text_frame, first=True)
r = p.add_run(); r.text = "数据说明与待确认事项"
set_font(r, size=12.5, bold=True, color=INK)

notes = [
    ("数据来源：", "data/q3-metrics.csv（2026-07 至 2026-09 月度汇总），本报告所有数字均由该文件计算得出，未做任何估算或补充。"),
    ("口径限制：", "缺 Q2 基线，无法给出同比 / 季度环比；缺 ARPU、渠道、成本、流失原因，因此收入波动只能做客户量层面的解释。"),
    ("待确认 ①：", "模板中「本季收入」应填季度合计 $529k 还是 9 月单月 $171k。本稿封面与摘要用合计，明细页两者都给。"),
    ("待确认 ②：", "流失口径（主动退订 / 未续费 / 沉默注销）与 8 月试用期调整的决策依据、灰度范围。"),
]
yy = ny + 0.72
for k, v in notes:
    tb = textbox(s, ML + 0.1, yy, CW - 0.45, 0.6)
    p = para(tb.text_frame, first=True, line=1.32)
    r = p.add_run(); r.text = k
    set_font(r, size=11, bold=True, color=ACCENT)
    r = p.add_run(); r.text = v
    set_font(r, size=11, color=BODY)
    yy += 0.44


# =====================================================================
# 演讲者备注
# =====================================================================
NOTES = [
    "开场（30 秒）：这是 Q3 季度回顾。今天只讲三件事——Q3 发生了什么、为什么、我们接下来怎么做。"
    "基调先说清楚：收入本身问题不大，真正需要立刻处理的是增长引擎和体验指标。",

    "如果今天只能记住一页，就是这一页。收入 -6% 可以被解释成季节性波动；"
    "但净增从 +29 掉到 +6、NPS 从 38 掉到 27，这两件事不能。"
    "注意四个 KPI 卡里三个是红的，红不是情绪，是口径——它们都指向同一个方向。",

    "收入页：7 月到 9 月连续两个月环比下滑，累计 -6.0%。"
    "要主动交代口径：我们没有 Q2 基线，所以给不出同比和季度环比，这里只能给季内环比，"
    "如果 VP 要同比，需要数据同学补一版（已写在附录待确认）。"
    "另外收入 = 客户数 × 客单价，目前缺客单价数据，只能确认客户侧在恶化。",

    "客户页是全篇最重要的一页。流失 12 → 19 → 24，新增 41 → 35 → 30，两头同时走坏。"
    "我建议用流失/新增比来沟通：0.29 → 0.80，意思是 9 月每 10 个新客户进来、8 个老客户离开。"
    "后面的线性外推要明确说是提醒、不是预测，避免被当成承诺。",

    "NPS 三个月掉 11 分，9 月 27 分已经跌破我们自己设的 30 预警线。"
    "要强调 NPS 是滞后指标，10 月大概率还会低——所以不要等它回升，要现在就动。"
    "这一页的落点是：三条曲线的拐点都在 9 月，说明大概率是同一个问题。",

    "归因页请注意措辞：这是假设，不是结论。主假设是 8 月中试用期从 14 天改到 7 天，"
    "用户还没感受到价值就被要求付费，直接变成早期流失。"
    "时间上吻合，但我们没有分群数据，不能证明因果。所以要主动要数据："
    "9 月流失客户的注册时间、试用时长、是否完成关键动作、流失原因标签。",

    "计划页：四件事，前两件是 10 月止血，后两件是 11 月修复。"
    "这里需要 VP 当场拍两件事：① 试用期策略允许做 A/B 并保留回滚；② Q4 目标值是否认可。"
    "负责人是建议人选，会后确认。",

    "附录页留给 Q&A：口径、数据限制和两个待确认事项都在这。"
    "如果被问到「为什么三个月才发现」，坦诚回答：我们只有月度快照，没有预警看板，"
    "计划里的第 4 项就是补这个机制。",
]
for sl, txt in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = txt

prs.save("Q3-2026-QBR.pptx")
print("saved Q3-2026-QBR.pptx, slides =", len(prs.slides.__iter__.__self__._sldIdLst))
