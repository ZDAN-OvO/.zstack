# -*- coding: utf-8 -*-
"""Generate the Q3 2026 QBR deck from data/q3-metrics.csv."""

import csv
from pptx import Presentation
from pptx.util import Inches as In, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_MARK
from pptx.chart.data import CategoryChartData
from pptx.oxml.ns import qn
from lxml import etree
from pptx.oxml.xmlchemy import OxmlElement

FONT = "Noto Sans CJK SC"
INK    = RGBColor(0x1B, 0x1F, 0x24)
BODY   = RGBColor(0x3A, 0x41, 0x49)
MUTED  = RGBColor(0x7A, 0x80, 0x87)
LINE   = RGBColor(0xDC, 0xD8, 0xD0)
BG     = RGBColor(0xF7, 0xF6, 0xF3)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
TEAL   = RGBColor(0x0E, 0x6B, 0x62)
RED    = RGBColor(0xB0, 0x47, 0x3C)
GOLD   = RGBColor(0xB9, 0x86, 0x2F)
DARK   = RGBColor(0x17, 0x1B, 0x20)
TEAL_L = RGBColor(0xE7, 0xEF, 0xED)
RED_L  = RGBColor(0xF3, 0xE6, 0xE3)

W, H = 13.333, 7.5
M = 0.85
CW = W - 2 * M

# ---------------------------------------------------------------- data
rows = list(csv.DictReader(open("data/q3-metrics.csv")))
months = [r["month"] for r in rows]
rev = [int(r["revenue_usd"]) for r in rows]
new = [int(r["new_customers"]) for r in rows]
churn = [int(r["churned_customers"]) for r in rows]
nps = [int(r["nps"]) for r in rows]
net = [n - c for n, c in zip(new, churn)]
rev_k = [round(v / 1000) for v in rev]
MLAB = [f"{int(m.split('-')[1])} 月" for m in months]

prs = Presentation()
prs.slide_width, prs.slide_height = In(W), In(H)
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------- helpers
def set_font(run, size, bold=False, color=INK, name=FONT, italic=False, space=None):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.name = name
    f.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = OxmlElement("a:ea")
        if latin is not None:
            latin.addnext(ea)
        else:
            rPr.append(ea)
    ea.set("typeface", name)
    if space is not None:
        rPr.set("spc", str(int(space * 100)))


def tb(slide, x, y, w, h, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(In(x), In(y), In(w), In(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    tf.paragraphs[0].alignment = align
    return box


def para(tf, first=False):
    return tf.paragraphs[0] if first else tf.add_paragraph()


def text(slide, x, y, w, h, s, size=14, color=BODY, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=1.35, space_after=0,
         space=None):
    box = tb(slide, x, y, w, h, align, anchor)
    p = box.text_frame.paragraphs[0]
    p.line_spacing = line
    p.space_after = Pt(space_after)
    r = p.add_run()
    r.text = s
    set_font(r, size, bold, color, space=space)
    return box


def rich(slide, x, y, w, h, parts, size=14, color=BODY, line=1.35,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=None):
    """parts: list of (text, {overrides}) -> single paragraph."""
    box = tb(slide, x, y, w, h, align, anchor)
    p = box.text_frame.paragraphs[0]
    p.line_spacing = line
    for s, kw in parts:
        r = p.add_run()
        r.text = s
        set_font(r, kw.get("size", size), kw.get("bold", False),
                 kw.get("color", color), space=kw.get("space", space))
    return box


def strip_style(sh):
    el = sh._element
    style = el.find(qn("p:style"))
    if style is not None:
        el.remove(style)
    sh.shadow.inherit = False


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, radius=None,
         shape=MSO_SHAPE.RECTANGLE):
    sh = slide.shapes.add_shape(shape, In(x), In(y), In(w), In(h))
    strip_style(sh)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = radius
    sh.text_frame.text = ""
    return sh


def hline(slide, x, y, w, color=LINE, lw=0.75):
    ln = slide.shapes.add_connector(1, In(x), In(y), In(x + w), In(y))
    ln.line.color.rgb = color
    ln.line.width = Pt(lw)
    strip_style(ln)
    return ln


def vline(slide, x, y, h, color=LINE, lw=0.75):
    ln = slide.shapes.add_connector(1, In(x), In(y), In(x), In(y + h))
    ln.line.color.rgb = color
    ln.line.width = Pt(lw)
    strip_style(ln)
    return ln


def new_slide(kicker=None):
    s = prs.slides.add_slide(BLANK)
    bg = s.background.fill
    bg.solid()
    bg.fore_color.rgb = BG
    return s


def header(slide, kicker, title, sub=None):
    text(slide, M, 0.5, CW, 0.22, kicker, 10, MUTED, True, space=2.2)
    text(slide, M, 0.76, CW, 0.62, title, 25, INK, True, line=1.2)
    hline(slide, M, 1.52, CW, LINE)
    if sub:
        text(slide, M, 1.68, CW, 0.34, sub, 12.5, MUTED, line=1.2)


def footer(slide, n, label="Q3 2026 业务回顾"):
    hline(slide, M, 7.02, CW, LINE)
    text(slide, M, 7.12, 6.0, 0.22, label, 9, MUTED)
    text(slide, W - M - 1.2, 7.12, 1.2, 0.22, f"{n:02d}", 9, MUTED,
         align=PP_ALIGN.RIGHT)


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def patch_chart_xml(chart, name=FONT):
    """Ensure CJK typeface is applied inside chart text properties."""
    root = chart._chartSpace
    for latin in root.iter(qn("a:latin")):
        latin.set("typeface", name)
        parent = latin.getparent()
        ea = parent.find(qn("a:ea"))
        if ea is None:
            ea = OxmlElement("a:ea")
            latin.addnext(ea)
        ea.set("typeface", name)


def chart_no_frame(chart):
    cs = chart._chartSpace
    spPr = cs.find(qn("c:spPr"))
    if spPr is None:
        spPr = OxmlElement("c:spPr")
        cs.find(qn("c:chart")).addnext(spPr)
    for child in list(spPr):
        spPr.remove(child)
    etree.SubElement(spPr, qn("a:noFill"))
    ln = etree.SubElement(spPr, qn("a:ln"))
    etree.SubElement(ln, qn("a:noFill"))


def style_chart(chart, size=11, legend=False):
    chart.font.size = Pt(size)
    chart.font.name = FONT
    chart.font.color.rgb = MUTED
    chart_no_frame(chart)
    chart.has_title = False
    if legend:
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.TOP
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(10.5)
        chart.legend.font.color.rgb = BODY
    else:
        chart.has_legend = False


def axis_style(ax, color=LINE, label_color=MUTED, size=10.5, visible=True):
    ax.has_major_gridlines = False
    ax.format.line.color.rgb = LINE
    ax.format.line.width = Pt(0.75)
    ax.tick_labels.font.size = Pt(size)
    ax.tick_labels.font.color.rgb = label_color
    ax.major_tick_mark = XL_TICK_MARK.NONE
    ax.minor_tick_mark = XL_TICK_MARK.NONE
    if not visible:
        ax.format.line.fill.background()


def data_labels(plot, fmt, size=11, color=INK, bold=True, pos=XL_LABEL_POSITION.OUTSIDE_END):
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format = fmt
    dl.number_format_is_linked = False
    dl.position = pos
    dl.font.size = Pt(size)
    dl.font.bold = bold
    dl.font.color.rgb = color
    dl.font.name = FONT


# ================================================================ 1 cover
s = new_slide()
bg = s.background.fill
bg.solid()
bg.fore_color.rgb = DARK

bar = rect(s, 0, 0, 0.09, H, fill=TEAL)

text(s, 1.15, 1.28, 7.0, 0.24, "QUARTERLY BUSINESS REVIEW  ·  Q3 2026", 11,
     RGBColor(0x9A, 0xA2, 0xA9), True, space=2.6)
text(s, 1.15, 1.72, 7.4, 0.95, "Q3 业务回顾", 46, WHITE, True, line=1.05)
text(s, 1.15, 2.85, 6.6, 0.9, "增长失速的一个季度\n以及一次试用政策变更的代价", 21,
     RGBColor(0xC9, 0xD2, 0xD1), line=1.45)

hline(s, 1.15, 4.42, 4.6, RGBColor(0x3A, 0x40, 0x46))

text(s, 1.15, 4.68, 4.0, 0.22, "汇报对象", 9.5, RGBColor(0x7A, 0x82, 0x89), True, space=1.8)
text(s, 1.15, 4.92, 4.0, 0.26, "VP, 增长与商业化", 12.5, RGBColor(0xD9, 0xDE, 0xDD))
text(s, 1.15, 5.32, 4.0, 0.22, "数据口径", 9.5, RGBColor(0x7A, 0x82, 0x89), True, space=1.8)
text(s, 1.15, 5.56, 5.2, 0.26, "2026-07-01 至 2026-09-30 · 财务确认收入", 12.5,
     RGBColor(0xD9, 0xDE, 0xDD))
text(s, 1.15, 5.96, 5.2, 0.22, "汇报日期 2026-10-08", 10.5, RGBColor(0x8B, 0x93, 0x9A))

# right stat strip
sx = 8.55
vline(s, sx - 0.45, 1.35, 4.85, RGBColor(0x33, 0x39, 0x3F))
for i, (big, lab, col) in enumerate([
        ("−6.0%", "季度内收入降幅", RGBColor(0xE0, 0x8A, 0x7C)),
        ("+100%", "月度流失增幅", RGBColor(0xE0, 0x8A, 0x7C)),
        ("27", "9 月 NPS（−11 分）", RGBColor(0xE0, 0xC2, 0x88))]):
    y = 1.45 + i * 1.62
    text(s, sx, y, 4.2, 0.72, big, 40, col, True, line=1.0)
    text(s, sx, y + 0.74, 4.2, 0.26, lab, 12, RGBColor(0x9A, 0xA2, 0xA9))

notes(s, "开场 30 秒：Q3 收入 52.9 万美元，比 7 月低 6%，同时流失翻倍、NPS 掉了 11 分。"
         "今天不是来报数字的，是来对一个具体决策达成一致：试用期要不要恢复到 14 天。")

# ================================================================ 2 exec summary
s = new_slide()
header(s, "01 · 执行摘要", "三个判断，一个请求",
       "Q3 的问题不在获客成本，而在新用户能否活过前 30 天。")

items = [
    ("01", "收入连续三个月下滑，方向明确",
     "7 月 182K → 8 月 176K → 9 月 171K，季度合计 $529K，累计 −6.0%；月度环比稳定在 −3% 左右，未见季末反弹。"),
    ("02", "增长引擎反转：新增在降，流失在涨",
     "新增 41 → 30（−27%），流失 12 → 24（+100%）。9 月净增仅 6 家，每获取 5 个新客户就流失 4 个。"),
    ("03", "体验指标先行恶化，且与试用期变更时间吻合",
     "NPS 38 → 31 → 27；“太难上手”工单自 9/8 起明显变多。8 月中旬试用期由 14 天改为 7 天，是当前最可信的解释。"),
]
y = 2.02
for num, head, body_txt in items:
    text(s, M, y - 0.03, 0.55, 0.3, num, 12, TEAL, True)
    text(s, M + 0.55, y - 0.05, 7.5, 0.3, head, 15.5, INK, True)
    text(s, M + 0.55, y + 0.32, 7.35, 0.72, body_txt, 11.5, BODY, line=1.45)
    y += 1.28

# request box
bx, by, bw, bh = 9.05, 1.98, W - M - 9.05, 4.42
rect(s, bx, by, bw, bh, fill=WHITE, line=LINE)
rect(s, bx, by, bw, 0.055, fill=TEAL)
text(s, bx + 0.3, by + 0.26, bw - 0.6, 0.22, "本次会议的请求", 9.5, TEAL, True, space=1.6)
text(s, bx + 0.3, by + 0.56, bw - 0.6, 0.75, "批准 Q4 三项动作，\n其中一项需要本周决策", 14, INK, True, line=1.35)
hline(s, bx + 0.3, by + 1.42, bw - 0.6, LINE)
asks = [("1", "恢复 14 天试用，并行 A/B 验证", "本周拍板 · 无新增预算"),
        ("2", "Onboarding 增配 1 人", "$8K/月 · Q4 合计 $24K"),
        ("3", "流失预警改造立项", "工程 2 人 × 6 周")]
ay = by + 1.58
for n, t1, t2 in asks:
    text(s, bx + 0.3, ay, 0.22, 0.22, n, 10.5, TEAL, True)
    text(s, bx + 0.56, ay - 0.01, bw - 0.86, 0.5, t1, 11.5, INK, True, line=1.3)
    text(s, bx + 0.56, ay + 0.42, bw - 0.86, 0.22, t2, 10, MUTED)
    ay += 0.82
hline(s, bx + 0.3, ay + 0.05, bw - 0.6, LINE)
text(s, bx + 0.3, ay + 0.16, bw - 0.6, 0.3,
     "本周只需批 A；B、C 可在 10/15 前定。", 9.5, MUTED, line=1.35)
footer(s, 2)
notes(s, "先给结论再给证据。三条判断按“财务结果 → 增长结构 → 体验根因”排列。"
         "右侧是今天要拿到的三个 yes/no，第 1 项如果今天不批，Q4 就无法验证。")

# ================================================================ 3 KPI
s = new_slide()
header(s, "02 · 核心指标", "Q3 四个指标同向恶化，且恶化在加速",
       "收入是结果，流失是过程，NPS 是先行信号——三者指向同一个环节。")

cards = [
    ("季度收入", "$529K", "−6.0%", "7 → 9 月", "vs 7 月", RED),
    ("新增客户", "106", "−27%", "41 → 30", "9 月 vs 7 月", RED),
    ("流失客户", "55", "+100%", "12 → 24", "9 月 vs 7 月", RED),
    ("NPS", "27", "−11", "38 → 27", "分数变化", RED),
]
cwd, gap = 2.78, 0.25
for i, (lab, val, delta, trace, note, col) in enumerate(cards):
    x = M + i * (cwd + gap)
    y = 2.02
    rect(s, x, y, cwd, 2.3, fill=WHITE, line=LINE)
    text(s, x + 0.26, y + 0.22, cwd - 0.5, 0.22, lab, 11, MUTED, True, space=1.4)
    text(s, x + 0.26, y + 0.55, cwd - 0.5, 0.62, val, 34, INK, True, line=1.0)
    # delta chip
    cw_ = 0.72 if len(delta) <= 4 else 0.9
    rect(s, x + 0.26, y + 1.32, cw_, 0.3, fill=RED_L, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
    text(s, x + 0.26, y + 1.38, cw_, 0.22, delta, 11, col, True, align=PP_ALIGN.CENTER)
    text(s, x + 0.26 + cw_ + 0.1, y + 1.38, 1.2, 0.22, trace, 9.5, MUTED)
    hline(s, x + 0.26, y + 1.8, cwd - 0.52, LINE)
    text(s, x + 0.26, y + 1.9, cwd - 0.5, 0.22, note, 9.5, MUTED)

# net adds band
band_y = 4.62
rect(s, M, band_y, CW, 1.62, fill=WHITE, line=LINE)
text(s, M + 0.3, band_y + 0.24, 2.3, 0.22, "净增客户", 10, MUTED, True, space=1.4)
text(s, M + 0.3, band_y + 0.52, 2.6, 0.3, "三个月持续衰减", 12.5, INK, True)
steps = [("7 月", "+29", 1.0), ("8 月", "+16", 0.55), ("9 月", "+6", 0.21)]
sx0 = 4.35
for i, (m, v, ratio) in enumerate(steps):
    x = sx0 + i * 2.55
    bw_ = 0.34 * ratio + 0.12
    rect(s, x, band_y + 0.55 + (0.62 - 0.62 * ratio), bw_, 0.62 * ratio, fill=TEAL)
    text(s, x + bw_ + 0.12, band_y + 0.44, 1.0, 0.3, v, 18, INK, True)
    text(s, x, band_y + 1.26, 1.4, 0.22, m, 10, MUTED)
text(s, 11.15, band_y + 0.44, 1.85, 0.85, "净增 = 新增 − 流失\n9 月几乎归零", 10.5, BODY, line=1.5)
footer(s, 3)
notes(s, "四个指标都用了“9 月 vs 7 月”的同类比较，避免拿季度平均掩盖尾部恶化。"
         "注意净增客户：+29 / +16 / +6，这是最直观的一条下滑曲线。")

# ================================================================ 4 revenue
s = new_slide()
header(s, "03 · 收入", "收入每月稳定下滑约 3%，没有季节性反弹",
       "季度收入 $529K；下滑幅度不大，但连续性和一致性说明是结构问题。")

cd = CategoryChartData()
cd.categories = MLAB
cd.add_series("收入", rev_k)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, In(M - 0.15), In(2.05),
                        In(7.6), In(4.55), cd)
ch = gf.chart
style_chart(ch, 11)
plot = ch.plots[0]
plot.gap_width = 95
plot.overlap = 0
ser = plot.series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = TEAL
ser.format.line.fill.background()
data_labels(plot, '"$"0"K"', 12.5, INK, True)

va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 220
va.major_unit = 50
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xE9, 0xE6, 0xDF)
va.major_gridlines.format.line.width = Pt(0.6)
va.tick_labels.number_format = '"$"0"K"'
va.tick_labels.number_format_is_linked = False
axis_style(va, visible=False)
axis_style(ch.category_axis)
patch_chart_xml(ch)

# annotations right
ry = 2.08
text(s, 8.55, ry, 3.9, 0.22, "读数", 9.5, TEAL, True, space=1.6)
obs = [("−$11K", "季度内累计减少，7→9 月每月约 −3%"),
       ("$176K", "季度月均收入，为 7 月的 97%，逐月走低"),
       ("0", "季末促销与扩张动作，Q3 没有")]
oy = ry + 0.36
for big, small in obs:
    text(s, 8.55, oy, 3.9, 0.36, big, 21, INK, True)
    text(s, 8.55, oy + 0.4, 3.7, 0.5, small, 10.5, MUTED, line=1.35)
    oy += 1.05

rect(s, 8.55, 5.35, 3.82, 1.18, fill=TEAL_L)
text(s, 8.78, 5.52, 3.4, 0.85,
     "收入下滑是“留存漏损”而非“定价”问题：客单价三个月内基本未变。",
     11, RGBColor(0x0B, 0x4F, 0x49), True, line=1.4)
footer(s, 4)
notes(s, "收入这条线不需要过度解读单月波动，重点是三个月方向一致。"
         "下一步看结构：新增和流失各自的贡献。")

# ================================================================ 5 growth
s = new_slide()
header(s, "04 · 增长结构", "新增降 27%、流失翻倍，9 月净增几乎归零",
       "流失/新增比从 29% 升到 80%：拉新的速度已经追不上漏水的速度。")

cd = CategoryChartData()
cd.categories = MLAB
cd.add_series("新增客户", new)
cd.add_series("流失客户", churn)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, In(M - 0.15), In(2.12),
                        In(7.5), In(4.4), cd)
ch = gf.chart
style_chart(ch, 11, legend=True)
plot = ch.plots[0]
plot.gap_width = 90
plot.overlap = -12
for ser, col in zip(plot.series, (TEAL, RED)):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = col
    ser.format.line.fill.background()
data_labels(plot, "0", 11, INK, True)
va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 50
va.major_unit = 10
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xE9, 0xE6, 0xDF)
va.major_gridlines.format.line.width = Pt(0.6)
axis_style(va, visible=False)
axis_style(ch.category_axis)
patch_chart_xml(ch)

# right panel
rx = 8.5
rect(s, rx, 2.1, 3.98, 1.85, fill=WHITE, line=LINE)
text(s, rx + 0.28, 2.28, 3.4, 0.22, "9 月流失 / 新增", 9.5, MUTED, True, space=1.4)
text(s, rx + 0.28, 2.58, 3.5, 0.55, "80%", 28, RED, True)
text(s, rx + 0.28, 3.16, 3.4, 0.6, "每 5 个新客户进来，就有 4 个老客户离开", 10.5, BODY, line=1.35)

text(s, rx, 4.16, 4.0, 0.22, "结构含义", 9.5, TEAL, True, space=1.6)
bl = [("拉新端", "新增连续两月下滑，渠道量价未变，疑似试用转化率下降"),
      ("留存端", "流失集中在注册 30 天内，早期流失而非长期疲劳")]
by_ = 4.5
for t1, t2 in bl:
    text(s, rx, by_, 3.95, 0.22, t1, 11.5, INK, True)
    text(s, rx, by_ + 0.26, 3.9, 0.55, t2, 10.5, MUTED, line=1.4)
    by_ += 1.05
footer(s, 5)
notes(s, "这张图是本次 QBR 的核心。新增下滑可以解释为市场变难，但流失翻倍必须从产品/体验找原因。"
         "流失集中在前 30 天，所以我们去看上手环节。")

# ================================================================ 6 NPS
s = new_slide()
header(s, "05 · 客户体验", "NPS 三个月掉 11 分，投诉关键词指向“上手”",
       "体验指标比收入更早转向，是这次下滑的先行信号。")

cd = CategoryChartData()
cd.categories = MLAB
cd.add_series("NPS", nps)
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, In(M - 0.2), In(2.1),
                        In(7.1), In(4.3), cd)
ch = gf.chart
style_chart(ch, 11)
plot = ch.plots[0]
ser = plot.series[0]
ser.format.line.color.rgb = GOLD
ser.format.line.width = Pt(2.5)
ser.marker.style = 8
ser.marker.size = 8
ser.marker.format.fill.solid()
ser.marker.format.fill.fore_color.rgb = WHITE
ser.marker.format.line.color.rgb = GOLD
ser.marker.format.line.width = Pt(2)
data_labels(plot, "0", 12.5, INK, True, XL_LABEL_POSITION.ABOVE)
va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 50
va.major_unit = 10
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xE9, 0xE6, 0xDF)
va.major_gridlines.format.line.width = Pt(0.6)
axis_style(va, visible=False)
axis_style(ch.category_axis)
patch_chart_xml(ch)

# right: evidence
rx = 8.15
text(s, rx, 2.12, 4.3, 0.22, "来自一线的工作日志", 9.5, TEAL, True, space=1.6)
quotes = [("9/8 起", "客服工单中“太难上手”的投诉明显变多"),
          ("8 月中", "免费试用从 14 天缩短为 7 天"),
          ("滞后 ≈ 3 周", "政策变更到投诉、流失集中爆发的时间差")]
qy = 2.46
for tag, body_txt in quotes:
    rect(s, rx, qy, 0.035, 0.92, fill=GOLD)
    text(s, rx + 0.22, qy - 0.02, 1.25, 0.22, tag, 9.5, GOLD, True)
    text(s, rx + 0.22, qy + 0.24, 3.75, 0.7, body_txt, 11, BODY, line=1.4)
    qy += 1.1

rect(s, rx, 5.72, 4.35, 0.82, fill=WHITE, line=LINE)
text(s, rx + 0.2, 5.86, 3.95, 0.6,
     "NPS 与流失同向、且早于财务指标约 1 个月出现，可作为 Q4 的领先看板。",
     9.5, MUTED, line=1.35)
footer(s, 6)
notes(s, "不要只报 NPS 数字，要给出可验证的现场证据：工单关键词在 9/8 之后变多，"
         "而试用期变更是 8 月中，中间正好是一个试用周期的滞后。")

# ================================================================ 7 root cause
s = new_slide()
header(s, "06 · 根因分析", "最可信的因果链：试用缩短 → 上手失败 → 早期流失",
       "我们把它当作强假设，而不是结论——Q4 用 A/B 验证，避免拍脑袋回滚。")

# timeline
ty = 2.62
hline(s, M + 0.3, ty, CW - 0.9, RGBColor(0xD5, 0xD0, 0xC7))
nodes = [("8/14", "试用期 14 → 7 天", "产品侧为提升付费转化率而调整\n未同步做激活漏斗评估", 0.85),
         ("9/8", "“太难上手”工单上升", "7 天试用内用户来不及完成\n关键配置与首次价值体验", 5.0),
         ("9/30", "流失 24 家 · NPS 27", "早期流失集中爆发\n新增转化同步走弱", 9.15)]
for tag, head, body_txt, x in nodes:
    rect(s, x, ty - 0.09, 0.18, 0.18, fill=TEAL, shape=MSO_SHAPE.OVAL)
    text(s, x - 0.1, ty - 0.52, 0.9, 0.26, tag, 11, TEAL, True)
    text(s, x - 0.1, ty + 0.22, 2.55, 0.28, head, 12.5, INK, True)
    text(s, x - 0.1, ty + 0.56, 2.6, 0.7, body_txt, 9.8, MUTED, line=1.4)

# causal chain cards
cy = 3.78
chain = [("试用期 −50%", "可体验时间不足以跑完激活路径", TEAL_L, RGBColor(0x0B, 0x4F, 0x49)),
         ("激活率下降", "首日未完成关键配置的用户大量滞留", TEAL_L, RGBColor(0x0B, 0x4F, 0x49)),
         ("30 天内流失上升", "付费意愿在体验失败后被消耗", RED_L, RED),
         ("NPS / 新增转化双降", "口碑与试用转化同时受损", RED_L, RED)]
cw_, gap = 2.86, 0.16
for i, (head, body_txt, bgc, fgc) in enumerate(chain):
    x = M + i * (cw_ + gap)
    rect(s, x, cy, cw_, 1.52, fill=bgc)
    text(s, x + 0.22, cy + 0.18, cw_ - 0.44, 0.26, head, 12, fgc, True, line=1.2)
    text(s, x + 0.22, cy + 0.52, cw_ - 0.42, 0.8, body_txt, 9.8, BODY, line=1.4)


# caveat + alt
rect(s, M, 5.62, 5.6, 1.02, fill=WHITE, line=LINE)
text(s, M + 0.22, 5.76, 5.15, 0.76,
     "反面证据：如果只是试用期问题，新增应持平而非下滑 27%。\n"
     "另有渠道质量与季节性因素，Q4 需拆分归因。", 9.5, MUTED, line=1.4)
rect(s, 6.65, 5.62, CW - 5.6 - 0.2, 1.02, fill=WHITE, line=LINE)
text(s, 6.87, 5.76, 5.6, 0.76,
     "验证方式：10/15 起 50/50 A/B，2 周看激活率，6 周看 30 天留存，\n"
     "样本不足则延长至 4 周。", 9.5, MUTED, line=1.4)
footer(s, 7)
notes(s, "这里要主动说反面证据：新增下滑不能全赖试用期。所以我们不主张直接回滚，"
         "而是并行 A/B，用 6 周拿结论。这能避免会上被质疑“归因过早”。")

# ================================================================ 8 plan
s = new_slide()
header(s, "07 · Q4 计划", "三条主线，先止跌、再修复、后提效",
       "目标：Q4 收入不低于 $540K，净增客户回到 90 家以上。")

# goal strip
gs = [("$540K", "Q4 收入目标", "+2% vs Q3"), ("90+", "Q4 净增客户", "vs Q3 的 51"),
      ("32", "12 月 NPS 目标", "回到 8 月水平"), ("≤ 40%", "流失 / 新增", "9 月为 80%")]
gw = (CW - 3 * 0.2) / 4
for i, (v, lab, sub) in enumerate(gs):
    x = M + i * (gw + 0.2)
    rect(s, x, 1.98, gw, 1.05, fill=WHITE, line=LINE)
    text(s, x + 0.22, 2.1, gw - 0.4, 0.35, v, 18, TEAL, True, line=1.1)
    text(s, x + 0.22, 2.48, gw - 0.4, 0.2, lab, 9.5, INK, True)
    text(s, x + 0.22, 2.7, gw - 0.4, 0.2, sub, 9, MUTED)

# workstreams
tracks = [
    ("A", "止跌：恢复 14 天试用", "10/15 上线 A/B，2 周出激活结论",
     "产品 · 张", "激活率、试用转化率", TEAL),
    ("B", "修复：Onboarding 重做", "首日 3 步引导 + 7 日任务清单",
     "体验 · 李", "上手类工单 −50%", TEAL),
    ("C", "提效：流失预警", "健康分模型 + 客户成功主动触达",
     "客成 · 王", "挽回率 20%、流失/新增 ≤40%", GOLD),
]
ty = 3.32
colx = [M, M + 0.55, M + 4.7, M + 7.35, M + 9.5]
text(s, colx[1], ty, 2.5, 0.2, "动作", 9, MUTED, True, space=1.4)
text(s, colx[2], ty, 2.5, 0.2, "做法", 9, MUTED, True, space=1.4)
text(s, colx[3], ty, 1.8, 0.2, "负责人", 9, MUTED, True, space=1.4)
text(s, colx[4], ty, 2.8, 0.2, "衡量指标", 9, MUTED, True, space=1.4)
hline(s, M, ty + 0.24, CW, LINE)
ry = ty + 0.34
for code, head, how, owner, kpi, col in tracks:
    rect(s, colx[0], ry + 0.02, 0.34, 0.34, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    text(s, colx[0], ry + 0.07, 0.34, 0.24, code, 11, WHITE, True, align=PP_ALIGN.CENTER)
    text(s, colx[1], ry, 4.0, 0.3, head, 12.5, INK, True)
    text(s, colx[2], ry + 0.01, 2.5, 0.55, how, 10, BODY, line=1.35)
    text(s, colx[3], ry + 0.01, 1.9, 0.3, owner, 10.5, BODY)
    text(s, colx[4], ry + 0.01, 2.6, 0.55, kpi, 10, BODY, line=1.35)
    hline(s, M, ry + 0.87, CW, RGBColor(0xE9, 0xE6, 0xDF))
    ry += 0.9

text(s, M, ry + 0.08, CW, 0.5,
     "节奏：10 月止跌验证 → 11 月修复上线 → 12 月看留存与 NPS 回升；每周一次 15 分钟增长例会跟踪四项指标。",
     10.5, MUTED)
footer(s, 8)
notes(s, "计划只保留三条，避免摊薄。A 是本周要批的，B/C 是资源投入。"
         "指标都设了可验收的数字，11 月起每周复盘。")

# ================================================================ 9 asks
s = new_slide()
header(s, "08 · 决策请求", "今天需要三个决定",
       "如果只能批一个，请批 A——它是唯一能在 Q4 内验证根因的动作。")

asks = [
    ("A", "恢复 14 天试用（并行 A/B）", "本周", "无新增预算",
     "50/50 分流，2 周看激活率，6 周看 30 天留存；若 7 天组不劣，则维持现状。", True),
    ("B", "Onboarding 增配 1 名专员", "10/10", "$24K / Q4",
     "负责首日引导与 7 日任务清单落地，目标上手类工单下降一半。", False),
    ("C", "流失预警改造立项", "10/20", "工程 2 人 × 6 周",
     "健康分模型接入 CRM，客户成功对高风险账户 48 小时内触达。", False),
]
ay = 2.0
for code, head, when, cost, detail, primary in asks:
    h = 1.28
    rect(s, M, ay, CW, h, fill=WHITE, line=LINE)
    if primary:
        rect(s, M, ay, 0.06, h, fill=TEAL)
    text(s, M + 0.32, ay + 0.2, 0.4, 0.3, code, 13, TEAL if primary else MUTED, True)
    text(s, M + 0.82, ay + 0.18, 5.4, 0.3, head, 14.5, INK, True)
    text(s, M + 0.82, ay + 0.55, 5.3, 0.7, detail, 10.5, MUTED, line=1.4)
    text(s, 6.75, ay + 0.2, 1.7, 0.2, "决策时间", 8.5, MUTED, True, space=1.2)
    text(s, 6.75, ay + 0.42, 1.7, 0.26, when, 11.5, BODY, True)
    text(s, 8.75, ay + 0.2, 2.0, 0.2, "资源需求", 8.5, MUTED, True, space=1.2)
    text(s, 8.75, ay + 0.42, 2.3, 0.26, cost, 11.5, BODY, True)
    text(s, 11.25, ay + 0.5, 1.2, 0.3, "待批", 10, TEAL if primary else MUTED, True)
    ay += 1.4

# risk
rect(s, M, 6.22, CW, 0.66, fill=TEAL_L)
rich(s, M + 0.24, 6.36, CW - 0.5, 0.45,
     [("风险与兜底：", {"bold": True, "color": RGBColor(0x0B, 0x4F, 0x49)}),
      ("若 11 月底 NPS 未回到 30 以上，12 月启动定价与套餐结构复审，并把 Q4 收入目标下调至 $520K 备案。",
       {"color": RGBColor(0x0B, 0x4F, 0x49)})], 10.5, line=1.35)
footer(s, 9)
notes(s, "收尾要非常明确：A 是零预算、可逆、能出结论的决策；B 是小额人力；C 是工程排期。"
         "同时给出失败兜底，避免会上被追问“如果没用怎么办”。")

# ================================================================ 10 appendix
s = new_slide()
header(s, "附录", "数据明细与口径", "源文件：data/q3-metrics.csv")

hdr = ["月份", "收入 (USD)", "新增客户", "流失客户", "净增", "流失/新增", "NPS"]
colw = [1.5, 2.2, 1.75, 1.75, 1.3, 1.75, 1.38]
tbl_w = sum(colw)
tbl_h = 0.5 + 0.52 * len(rows) + 0.52
gt = s.shapes.add_table(len(rows) + 2, len(hdr), In(M), In(2.15), In(tbl_w), In(tbl_h))
table = gt.table
table.first_row = True
for i, w_ in enumerate(colw):
    table.columns[i].width = In(w_)
for j, htxt in enumerate(hdr):
    c = table.cell(0, j)
    c.fill.solid()
    c.fill.fore_color.rgb = INK
    c.margin_left = In(0.14)
    c.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = c.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = htxt
    set_font(r, 10, True, WHITE)
vrows = []
for i, r_ in enumerate(rows):
    vrows.append([MLAB[i], f"${rev[i]:,}", str(new[i]), str(churn[i]),
                  f"+{net[i]}", f"{churn[i]/new[i]*100:.0f}%", str(nps[i])])
vrows.append(["季度合计", f"${sum(rev):,}", str(sum(new)), str(sum(churn)),
              f"+{sum(net)}", f"{sum(churn)/sum(new)*100:.0f}%", "—"])
for i, row in enumerate(vrows, start=1):
    for j, val in enumerate(row):
        c = table.cell(i, j)
        c.fill.solid()
        c.fill.fore_color.rgb = WHITE if i % 2 else RGBColor(0xFB, 0xFA, 0xF8)
        c.margin_left = In(0.14)
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = c.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = val
        bold = (i == len(vrows))
        col = INK if j == 0 else BODY
        if j == 3 and i <= 3:
            col = RED
        set_font(r, 10.5, bold, col)
    table.rows[i].height = In(0.5)

text(s, M, 5.05, 6.6, 0.22, "口径说明", 9.5, TEAL, True, space=1.4)
notes_lines = [
    "· 收入为财务确认收入，非合同金额（Bookings）；季度合计为三个月直接相加。",
    "· 新增 = 当季首次付费客户；流失 = 当季取消或到期未续费客户，含 30 天内早期流失。",
    "· 流失/新增比为当月口径，用于观察“漏水速度”，非标准流失率。",
    "· NPS 为季度内每月末滚动 90 天调研结果，样本量约 180–220。",
    "· 为保护客户信息，本页不含客户名单与合同明细。",
]
ny = 5.3
for ln_ in notes_lines:
    text(s, M, ny, 7.4, 0.24, ln_, 9.5, MUTED, line=1.3)
    ny += 0.27

rect(s, 7.9, 5.05, 4.55, 1.6, fill=WHITE, line=LINE)
text(s, 8.12, 5.2, 4.1, 0.22, "数据局限", 9.5, GOLD, True, space=1.4)
text(s, 8.12, 5.48, 4.1, 1.05,
     "仅 3 个月数据，不足以做因果推断；\n缺渠道分群与激活漏斗明细，\nQ4 需补齐后重跑归因。",
     9.5, MUTED, line=1.45)
footer(s, 10)

prs.save("Q3_2026_QBR.pptx")
print("saved", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
