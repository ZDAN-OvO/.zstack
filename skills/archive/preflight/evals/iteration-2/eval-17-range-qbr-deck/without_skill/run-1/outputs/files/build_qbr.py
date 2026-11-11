# -*- coding: utf-8 -*-
"""Q3 2026 QBR deck builder."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import (XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION,
                             XL_TICK_MARK, XL_MARKER_STYLE)
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
from lxml import etree

# ---------- design tokens ----------
NAVY   = RGBColor(0x0E, 0x1C, 0x2B)
INK    = RGBColor(0x1B, 0x27, 0x33)
GRAY   = RGBColor(0x5E, 0x6B, 0x79)
MUTED  = RGBColor(0x8A, 0x95, 0xA1)
LINE   = RGBColor(0xD9, 0xDF, 0xE6)
WASH   = RGBColor(0xF4, 0xF6, 0xF9)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
BLUE   = RGBColor(0x1F, 0x4E, 0x79)
RED    = RGBColor(0xB0, 0x39, 0x2C)
AMBER  = RGBColor(0xC4, 0x7A, 0x20)
TEAL   = RGBColor(0x2A, 0x7A, 0x67)

FONT = "Microsoft YaHei"
W, H = 13.333, 7.5
ML = 0.9                     # left margin
CW = W - 2 * ML              # content width

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]


# ---------- primitives ----------
def _style_run(run, size, bold, color, font=FONT, italic=False):
    f = run.font
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    f.name = font
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", font)


def text(slide, x, y, w, h, s, size=14, bold=False, color=INK,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0,
         space_after=0, font=FONT, italic=False, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = s.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        _style_run(p.add_run(), size, bold, color, font, italic)
        p.runs[0].text = ln
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE, radius=None):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.shadow.inherit = False
    st = sp._element.find(qn('p:style'))
    if st is not None:
        sp._element.remove(st)
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = Pt(lw)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sp.adjustments[0] = radius
    sp.text_frame.text = ""
    return sp


def hline(slide, x, y, w, color=LINE, lw=1.0):
    rect(slide, x, y, w, 0.01, fill=color, line=None).line.width = Pt(lw)


def slide_base(kicker=None, title=None, subtitle=None, dark=False):
    s = prs.slides.add_slide(BLANK)
    bg = rect(s, 0, 0, W, H, fill=NAVY if dark else WHITE)
    bg.shadow.inherit = False
    fg = WHITE if dark else INK
    if kicker:
        text(s, ML, 0.42, CW, 0.22, kicker, size=10.5, bold=True,
             color=AMBER if not dark else AMBER)
    if title:
        text(s, ML, 0.66, CW, 0.52, title, size=25, bold=True, color=fg)
    if subtitle:
        text(s, ML, 1.22, CW, 0.28, subtitle, size=12, color=MUTED if not dark else RGBColor(0xB8, 0xC2, 0xCE))
    if title:
        hline(s, ML, 1.62, CW, LINE if not dark else RGBColor(0x2A, 0x3A, 0x4C))
    return s


def footer(s, n, note=""):
    text(s, ML, H - 0.52, CW - 1.2, 0.22, note, size=9, color=MUTED)
    text(s, W - ML - 0.8, H - 0.52, 0.8, 0.22, f"{n:02d}", size=9, bold=True,
         color=MUTED, align=PP_ALIGN.RIGHT)


# ---------- table helper ----------
def _hex(c):
    return str(c)


def _ln_el(tag, color=None, w=9525):
    """Build an <a:lnX> element."""
    ns = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    if color is None:
        return parse_xml(f'<{tag} {ns} w="{w}" cap="flat"><a:noFill/></{tag}>')
    return parse_xml(f'<{tag} {ns} w="{w}" cap="flat"><a:solidFill><a:srgbClr val="{_hex(color)}"/></a:solidFill></{tag}>')


def _set_borders(cell, bottom=True, bottom_color=None, bottom_w=9525):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        el = tcPr.find(qn(tag))
        if el is not None:
            tcPr.remove(el)
    specs = [("a:lnL", None, 9525), ("a:lnR", None, 9525), ("a:lnT", None, 9525),
             ("a:lnB", bottom_color if bottom else None, bottom_w)]
    for tag, color, width in reversed(specs):
        tcPr.insert(0, _ln_el(tag, color, width))


def table(slide, x, y, w, col_w, rows, header, row_h=0.46, hdr_h=0.42,
          size=11.5, hdr_size=10.5, aligns=None, cell_colors=None, bold_first=True):
    n_r, n_c = len(rows) + 1, len(header)
    gf = slide.shapes.add_table(n_r, n_c, Inches(x), Inches(y), Inches(w), Inches(hdr_h + row_h * len(rows)))
    tbl = gf.table
    tbl.first_row = False
    tbl.horz_banding = False
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    tbl.rows[0].height = Inches(hdr_h)
    for i in range(1, n_r):
        tbl.rows[i].height = Inches(row_h)

    def fill_cell(cell, s, sz, bold, color, align, fill=None, top_line=False):
        cell.text = ""
        cell.margin_left = Inches(0.09)
        cell.margin_right = Inches(0.09)
        cell.margin_top = cell.margin_bottom = 0
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        if fill is None:
            cell.fill.background()
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = fill
        p = cell.text_frame.paragraphs[0]
        p.alignment = align
        _style_run(p.add_run(), sz, bold, color)
        p.runs[0].text = s
        _set_borders(cell, bottom=True, bottom_color=LINE)

    aligns = aligns or ([PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * (n_c - 1))
    for c, h in enumerate(header):
        fill_cell(tbl.cell(0, c), h, hdr_size, True, GRAY, aligns[c])
    # header underline
    for c in range(n_c):
        _set_borders(tbl.cell(0, c), bottom=True, bottom_color=INK, bottom_w=12700)

    for r, row in enumerate(rows, start=1):
        for c, v in enumerate(row):
            col = cell_colors[r - 1][c] if cell_colors else INK
            fill_cell(tbl.cell(r, c), v, size, bold_first and c == 0, col, aligns[c])
    return tbl


def hide_series_labels(ser):
    """Turn off data labels for a single series (plot-level labels stay on)."""
    ns = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
    el = parse_xml(
        f'<c:dLbls xmlns:c="{ns}"><c:showLegendKey val="0"/><c:showVal val="0"/>'
        '<c:showCatName val="0"/><c:showSerName val="0"/><c:showPercent val="0"/>'
        '<c:showBubbleSize val="0"/></c:dLbls>')
    ser_el = ser._element
    cat = ser_el.find(qn('c:cat'))
    idx = list(ser_el).index(cat) if cat is not None else len(ser_el)
    ser_el.insert(idx, el)


# =========================================================
# 1. COVER
# =========================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, fill=NAVY)
rect(s, 0, 0, 0.16, H, fill=AMBER)
text(s, 1.35, 1.78, 8.0, 0.3, "QUARTERLY BUSINESS REVIEW", size=12, bold=True, color=AMBER)
text(s, 1.35, 2.24, 9.5, 0.85, "Q3 2026", size=54, bold=True, color=WHITE)
text(s, 1.35, 3.14, 9.5, 0.85, "业务回顾", size=52, bold=True, color=WHITE)
text(s, 1.35, 4.16, 8.6, 0.9,
     "增长转收缩的一个季度：收入连续三月下滑，\n净新增客户逼近零点。", size=17,
     color=RGBColor(0xC3, 0xCD, 0xD9), spacing=1.35)
hline(s, 1.35, 5.35, 4.2, RGBColor(0x3B, 0x4E, 0x62))
text(s, 1.35, 5.55, 5.0, 0.9,
     "汇报对象：VP\n汇报时间：下周（具体日期待定）\n数据区间：2026-07-01 ~ 2026-09-30",
     size=11, color=RGBColor(0x9A, 0xA8, 0xB8), spacing=1.5)
text(s, W - 3.25, 6.55, 2.35, 0.3, "内部资料 · 勿外传", size=9.5, color=RGBColor(0x7C, 0x8A, 0x99), align=PP_ALIGN.RIGHT)
rect(s, 1.35, 6.95, 10.6, 0.012, fill=RGBColor(0x26, 0x39, 0x4D))

# =========================================================
# 2. EXECUTIVE SUMMARY
# =========================================================
s = slide_base("EXECUTIVE SUMMARY", "执行摘要：问题已定位，但需要本周做决定",
               "一页看清三件事——发生了什么、为什么、下一步要什么")
footer(s, 2)

kpis = [("收入（Q3）", "$529K", "较 7 月 −6.0%", RED),
        ("净新增客户", "+6", "7 月为 +29，降幅 79%", RED),
        ("NPS", "27", "7 月为 38，−11 分", RED)]
x = ML
for label, val, delta, col in kpis:
    rect(s, x, 1.85, 3.66, 1.5, fill=WASH)
    rect(s, x, 1.85, 0.05, 1.5, fill=col)
    text(s, x + 0.28, 2.02, 3.1, 0.24, label, size=10.5, bold=True, color=GRAY)
    text(s, x + 0.28, 2.28, 3.1, 0.6, val, size=33, bold=True, color=INK)
    text(s, x + 0.28, 2.95, 3.1, 0.24, delta, size=10.5, bold=True, color=col)
    x += 3.66 + 0.32

text(s, ML, 3.62, 6.4, 0.26, "三条结论", size=11, bold=True, color=BLUE)
findings = [
    ("这不是波动，是趋势。", "收入、新增、NPS 三项连续三个月同向下滑，流失客户翻倍（12 → 24）。单月波动可以用季节解释，三月同向不能。"),
    ("根因大概率在 8 月 15 日的试用期改动。", "试用从 14 天缩短到 7 天；9 月 8 日起“太难上手”类工单明显增多。链条高度吻合，但尚无按试用时长拆分的转化数据佐证。"),
    ("Q4 的第一优先级是止血，不是增长。", "净新增按当前斜率 10 月转负；此时加大获客投放只会放大漏损。先把转化和留存修回 7 月水平。"),
]
y = 3.96
for i, (h1, body) in enumerate(findings, 1):
    text(s, ML, y + 0.02, 0.3, 0.3, f"{i}", size=13, bold=True,
         color=WHITE if False else BLUE)
    rect(s, ML, y + 0.03, 0.26, 0.26, fill=BLUE)
    text(s, ML, y + 0.04, 0.26, 0.22, str(i), size=10.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, ML + 0.42, y, 6.1, 0.26, h1, size=13, bold=True, color=INK)
    text(s, ML + 0.42, y + 0.29, 6.15, 0.62, body, size=10.3, color=GRAY, spacing=1.28)
    y += 0.96

# right: ask box
box_x = ML + 6.9
rect(s, box_x, 3.62, CW - 6.9, 3.0, fill=NAVY)
text(s, box_x + 0.35, 3.85, CW - 7.6, 0.24, "本次 QBR 唯一需要的决定", size=10.5, bold=True, color=AMBER)
text(s, box_x + 0.35, 4.18, CW - 7.6, 0.7, "将免费试用期\n回调至 14 天", size=19, bold=True, color=WHITE, spacing=1.25)
hline(s, box_x + 0.35, 5.0, CW - 7.8, RGBColor(0x33, 0x47, 0x5C))
text(s, box_x + 0.35, 5.18, CW - 7.7, 1.25,
     "成本：无直接现金成本，仅影响付费转化节奏\n代价：短期转化率口径会波动 1 个季度\n时限：需在本周内拍板，否则 10 月样本已污染",
     size=10, color=RGBColor(0xB9, 0xC4, 0xD1), spacing=1.45)

# =========================================================
# 3. METRICS OVERVIEW
# =========================================================
s = slide_base("01 · 指标总览", "核心指标一览：五项指标，三个月同向恶化",
               "趋势比单点更重要——三个月里每一次读数都比上一次差")
footer(s, 3, "注：Q3 收入为三个月合计；环比列取 9 月对 7 月。")
rows = [
    ["收入（USD）", "182,000", "176,000", "171,000", "−6.0%", "三连降，尚未见底"],
    ["新增客户", "41", "35", "30", "−26.8%", "获客逐月走弱"],
    ["流失客户", "12", "19", "24", "+100%", "翻倍，最需警惕"],
    ["净新增客户", "+29", "+16", "+6", "−79.3%", "逼近零点"],
    ["NPS", "38", "31", "27", "−11 分", "体验同步恶化"],
]
cc = [[INK, INK, INK, INK, RED, RED],
      [INK, INK, INK, INK, RED, AMBER],
      [INK, INK, INK, INK, RED, RED],
      [INK, INK, INK, INK, RED, RED],
      [INK, INK, INK, INK, RED, AMBER]]
table(s, ML, 1.92, CW, [2.9, 1.75, 1.75, 1.75, 1.9, 2.58], rows,
      ["指标", "7 月", "8 月", "9 月", "9 月 vs 7 月", "判读"],
      row_h=0.47, hdr_h=0.44, size=12, cell_colors=cc)

text(s, ML, 5.12, CW, 0.26, "值得注意的两点", size=11, bold=True, color=BLUE)
notes = [
    ("流失的绝对量在放大，而不只是比例。", "24 家/月意味着收入基础在被动收缩，且流失客户通常会带走后续增购。"),
    ("新增下滑与流失上升同时发生，说明是同一个原因。", "市场问题只会打新增；两者同时恶化，指向产品与上手环节，即试用与引导。"),
]
y = 5.44
for h1, body in notes:
    rect(s, ML, y + 0.1, 0.09, 0.09, fill=AMBER)
    text(s, ML + 0.26, y, 6.2, 0.24, h1, size=11.5, bold=True, color=INK)
    text(s, ML + 0.26, y + 0.28, 6.2, 0.5, body, size=10, color=GRAY, spacing=1.3)
    y += 0.82

# =========================================================
# 4. REVENUE CHART
# =========================================================
s = slide_base("02 · 收入", "收入：三个月连续下滑，累计 −6.0%",
               "尚无单月反弹迹象，9 月是季度最低点")
footer(s, 4, "注：纵轴自 150K 起，以放大趋势差异；各点已标注实际值。")

cd = CategoryChartData()
cd.categories = ["7 月", "8 月", "9 月"]
cd.add_series("月度收入（USD）", (182000, 176000, 171000))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(ML), Inches(1.95),
                        Inches(7.5), Inches(4.15), cd)
ch = gf.chart
ch.font.size = Pt(10.5)
ch.font.name = FONT
ch.font.color.rgb = GRAY
ch.has_legend = False
ch.has_title = True
ch.chart_title.text_frame.text = "月度收入（USD）"
_style_run(ch.chart_title.text_frame.paragraphs[0].runs[0], 10.5, True, GRAY)
pl = ch.plots[0]
pl.has_data_labels = True
dl = pl.data_labels
dl.number_format = '$#,##0,"K"'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.ABOVE
dl.font.size = Pt(12)
dl.font.bold = True
dl.font.color.rgb = INK
ser = pl.series[0]
ser.format.line.color.rgb = BLUE
ser.format.line.width = Pt(3.0)
ser.smooth = False
ser.marker.style = XL_MARKER_STYLE.CIRCLE
ser.marker.size = 9
ser.marker.format.fill.solid()
ser.marker.format.fill.fore_color.rgb = BLUE
ser.marker.format.line.color.rgb = WHITE
ser.marker.format.line.width = Pt(2)
va = ch.value_axis
va.minimum_scale = 150000
va.maximum_scale = 190000
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEF, 0xF3)
va.major_gridlines.format.line.width = Pt(0.75)
va.tick_labels.number_format = '$#,##0,"K"'
va.tick_labels.number_format_is_linked = False
va.tick_labels.font.color.rgb = MUTED
va.format.line.fill.background()
va.major_tick_mark = XL_TICK_MARK.NONE
ca = ch.category_axis
ca.tick_labels.font.size = Pt(11.5)
ca.tick_labels.font.color.rgb = INK
ca.format.line.color.rgb = LINE
ca.major_tick_mark = XL_TICK_MARK.NONE

# right panel
px = ML + 7.85
pw = CW - 7.85
text(s, px, 1.98, pw, 0.24, "发生了什么", size=10.5, bold=True, color=BLUE)
text(s, px, 2.28, pw, 1.6,
     "7 月 182K → 9 月 171K，单月降幅 6K 与 5K，\n降速在收窄但方向未变。\n\n按此斜率线性外推，10 月约 165K。",
     size=11, color=GRAY, spacing=1.4)
hline(s, px, 3.95, pw, LINE)
text(s, px, 4.12, pw, 0.24, "为什么不能只看总额", size=10.5, bold=True, color=BLUE)
text(s, px, 4.42, pw, 1.0,
     "收入下滑的构成里，流失客户带走的收入比新增减少的部分更硬——它是永久性的，需要重新销售才能补回。",
     size=10.5, color=GRAY, spacing=1.4)
rect(s, px, 5.62, pw, 0.92, fill=WASH)
text(s, px + 0.26, 5.74, pw - 0.5, 0.7,
     "读法提醒：总额只能判断“变差”，拆分新增 / 留存 / 流失三段才能判断“哪里变差”。",
     size=9.8, color=GRAY, spacing=1.3)

# =========================================================
# 5. ACQUISITION VS CHURN
# =========================================================
s = slide_base("03 · 客户", "获客与流失：两条线正在靠拢",
               "新增 −27%、流失 +100%，净新增从 29 掉到 6")
footer(s, 5, "注：净新增 = 新增 − 流失，按当月计。")

cd = CategoryChartData()
cd.categories = ["7 月", "8 月", "9 月"]
cd.add_series("新增客户", (41, 35, 30))
cd.add_series("流失客户", (12, 19, 24))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(ML), Inches(1.95),
                        Inches(7.6), Inches(3.55), cd)
ch = gf.chart
ch.font.size = Pt(10.5)
ch.font.name = FONT
ch.font.color.rgb = GRAY
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(10.5)
pl = ch.plots[0]
pl.gap_width = 70
pl.overlap = -8
pl.has_data_labels = True
pl.data_labels.font.size = Pt(11)
pl.data_labels.font.bold = True
pl.data_labels.font.color.rgb = INK
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
for i, c in enumerate((BLUE, RED)):
    sr = pl.series[i]
    sr.format.fill.solid()
    sr.format.fill.fore_color.rgb = c
    sr.format.line.fill.background()
va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 50
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEF, 0xF3)
va.format.line.fill.background()
va.major_tick_mark = XL_TICK_MARK.NONE
va.tick_labels.font.color.rgb = MUTED
ca = ch.category_axis
ca.tick_labels.font.size = Pt(11.5)
ca.tick_labels.font.color.rgb = INK
ca.format.line.color.rgb = LINE
ca.major_tick_mark = XL_TICK_MARK.NONE

# net new strip
text(s, ML, 5.62, 1.5, 0.24, "净新增", size=10.5, bold=True, color=GRAY)
x = ML + 1.5
for m, v in (("7 月", "+29"), ("8 月", "+16"), ("9 月", "+6")):
    rect(s, x, 5.55, 1.55, 0.52, fill=WASH)
    text(s, x, 5.62, 0.7, 0.22, m, size=9.5, color=GRAY)
    text(s, x + 0.7, 5.63, 0.75, 0.3, v, size=15, bold=True,
         color=RED if v == "+6" else (AMBER if v == "+16" else INK), align=PP_ALIGN.RIGHT)
    x += 1.55 + 0.14

px = ML + 7.95
pw = CW - 7.95
rect(s, px, 1.95, pw, 2.05, fill=WASH)
rect(s, px, 1.95, 0.05, 2.05, fill=RED)
text(s, px + 0.3, 2.12, pw - 0.5, 0.24, "关键判断", size=10.5, bold=True, color=RED)
text(s, px + 0.3, 2.42, pw - 0.55, 1.45,
     "按 8 → 9 月的斜率（净新增 −10/月），\n10 月净新增将转负，即开始净流失。\n\n留给我们的窗口是一个月。",
     size=11, color=INK, spacing=1.4)
text(s, px, 4.2, pw, 0.24, "对 Q4 的含义", size=10.5, bold=True, color=BLUE)
text(s, px, 4.5, pw, 1.5,
     "在漏损修好之前，提高获客预算的边际回报为负：\n每多买 100 个试用，会有更大比例在 7 天内流失。",
     size=10.5, color=GRAY, spacing=1.4)

# =========================================================
# 6. ROOT CAUSE CHAIN
# =========================================================
s = slide_base("04 · 根因", "根因链条：一次试用期改动，穿透到三项指标",
               "8 月 15 日的改动是唯一同时能解释新增、流失与 NPS 的事件")
footer(s, 6, "说明：链条为证据驱动的推断，尚缺按试用时长拆分的转化数据，见第 8 页。")

steps = [
    ("触发", "试用期 14 天 → 7 天", "8 月 15 日上线，未做灰度，全部新注册用户生效。", AMBER),
    ("机制", "上手时间不够", "原本两周的评估流程被压到一周，客户在见到核心价值前就被切断。", BLUE),
    ("信号", "“太难上手”工单激增", "9 月 8 日起客服工单中该类投诉明显变多，时间点较改动延后约 3 周。", BLUE),
    ("结果", "流失翻倍、NPS −11", "流失 12 → 24，新增 41 → 30，NPS 38 → 27，三项同时恶化。", RED),
]
bw, gap = 2.62, 0.38
x = ML
for i, (tag, head, body, col) in enumerate(steps):
    rect(s, x, 2.0, bw, 2.35, fill=WASH)
    rect(s, x, 2.0, bw, 0.055, fill=col)
    text(s, x + 0.24, 2.18, bw - 0.4, 0.22, tag, size=9.5, bold=True, color=col)
    text(s, x + 0.24, 2.44, bw - 0.42, 0.66, head, size=14, bold=True, color=INK, spacing=1.2)
    text(s, x + 0.24, 3.18, bw - 0.42, 1.0, body, size=10, color=GRAY, spacing=1.32)
    if i < 3:
        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + bw + 0.06), Inches(2.92),
                                Inches(gap - 0.12), Inches(0.19))
        ar.shadow.inherit = False
        ar.fill.solid()
        ar.fill.fore_color.rgb = RGBColor(0xC2, 0xCB, 0xD6)
        ar.line.fill.background()
    x += bw + gap

text(s, ML, 4.62, CW, 0.26, "为什么排除其他解释", size=11, bold=True, color=BLUE)
alts = [("季节性？", "若为季节性，NPS 通常不会同步下挫 11 分。"),
        ("竞争加剧？", "竞争会压低新增，但不会让存量客户在两个月内成倍流失。")]
x = ML
for h1, b in alts:
    rect(s, x, 4.95, 5.75, 0.78, fill=None, line=LINE)
    text(s, x + 0.24, 5.06, 5.3, 0.22, h1, size=10.5, bold=True, color=INK)
    text(s, x + 0.24, 5.3, 5.3, 0.36, b, size=10, color=GRAY, spacing=1.25)
    x += 5.75 + 0.38

rect(s, ML, 5.95, CW, 0.62, fill=NAVY)
text(s, ML + 0.32, 6.1, CW - 0.64, 0.32,
     "结论：把 8 月 15 日的试用期改动撤回，是本季度唯一低成本、可验证、可立即执行的干预点。",
     size=12, bold=True, color=WHITE)

# =========================================================
# 7. NPS
# =========================================================
s = slide_base("05 · 客户体验", "NPS：38 → 27，跌破健康线",
               "净值跌破 30 通常意味着口碑驱动的自然增长同时停滞")
footer(s, 7, "注：NPS 为月末滚动值，样本口径未变更。")

cd = CategoryChartData()
cd.categories = ["7 月", "8 月", "9 月"]
cd.add_series("NPS 净值", (38, 31, 27))
cd.add_series("健康线（30）", (30, 30, 30))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(ML), Inches(2.0),
                        Inches(6.5), Inches(3.85), cd)
ch = gf.chart
ch.font.size = Pt(10.5)
ch.font.name = FONT
ch.font.color.rgb = GRAY
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
ch.legend.include_in_layout = False
ch.legend.font.size = Pt(10)
ch.has_title = True
ch.chart_title.text_frame.text = "NPS 净值（月末滚动）"
_style_run(ch.chart_title.text_frame.paragraphs[0].runs[0], 10.5, True, GRAY)
pl = ch.plots[0]
pl.has_data_labels = True
pl.data_labels.font.size = Pt(12)
pl.data_labels.font.bold = True
pl.data_labels.font.color.rgb = INK
pl.data_labels.position = XL_LABEL_POSITION.ABOVE
sr = pl.series[0]
sr.format.line.color.rgb = BLUE
sr.format.line.width = Pt(3.0)
sr.smooth = False
sr.marker.style = XL_MARKER_STYLE.CIRCLE
sr.marker.size = 9
sr.marker.format.fill.solid()
sr.marker.format.fill.fore_color.rgb = BLUE
sr.marker.format.line.color.rgb = WHITE
sr.marker.format.line.width = Pt(2)
th = pl.series[1]
th.smooth = False
th.marker.style = XL_MARKER_STYLE.NONE
th.format.line.color.rgb = RED
th.format.line.width = Pt(1.5)
th.format.line.dash_style = MSO_LINE.DASH
hide_series_labels(th)
va = ch.value_axis
va.minimum_scale = 0
va.maximum_scale = 45
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEF, 0xF3)
va.format.line.fill.background()
va.major_tick_mark = XL_TICK_MARK.NONE
va.tick_labels.font.color.rgb = MUTED
ca = ch.category_axis
ca.tick_labels.font.size = Pt(11.5)
ca.tick_labels.font.color.rgb = INK
ca.format.line.color.rgb = LINE
ca.major_tick_mark = XL_TICK_MARK.NONE

# threshold band annotation removed (handled by series)
px = ML + 6.9
pw = CW - 6.9
rect(s, px, 2.0, pw, 1.75, fill=WASH)
text(s, px + 0.3, 2.16, pw - 0.6, 0.22, "客户原声（客服工单）", size=10, bold=True, color=GRAY)
text(s, px + 0.3, 2.42, pw - 0.6, 1.2,
     "“太难上手”相关投诉自 9 月 8 日起\n明显增多。", size=15, bold=True, color=INK, spacing=1.3)

text(s, px, 3.98, pw, 0.24, "三条可读的信号", size=10.5, bold=True, color=BLUE)
_sigbox = s.shapes.add_textbox(Inches(px), Inches(4.3), Inches(pw), Inches(2.3))
_stf = _sigbox.text_frame
_stf.word_wrap = True
_stf.margin_left = _stf.margin_right = _stf.margin_top = _stf.margin_bottom = 0
sigs = ["投诉出现的时间点比改动晚约 3 周——符合“先注册、再卡住、最后放弃”的滞后。",
        "工单集中在“上手”而非“价格”或“功能缺失”，指向流程而非产品价值。",
        "贬损者比例上升通常先于流失体现，10 月流失压力可能继续放大。"]
for i, t in enumerate(sigs):
    p = _stf.paragraphs[0] if i == 0 else _stf.add_paragraph()
    p.line_spacing = 1.35
    p.space_after = Pt(15)
    _style_run(p.add_run(), 10, False, GRAY)
    p.runs[0].text = "▪  " + t

# =========================================================
# 8. WHAT'S MISSING / EVIDENCE GAPS
# =========================================================
s = slide_base("06 · 待补证据", "这个结论还不够硬：三组数据本周必须补上",
               "对 VP 汇报最忌讳“猜对了但证明不了”——先把证据补齐再定 Q4 目标")
footer(s, 8, "说明：下一页的外推情景建立在“趋势不变”假设上，不等同于预测。")

gaps = [
    ("按试用天数拆分的转化率", "7 天 vs 14 天 cohorts 的试用→付费率",
     "若 7 天组转化率显著更低，根因即被证实；若持平，需转向引导流程假设。", "产品分析 · 本周三前"),
    ("9 月工单的结构化归因", "按主题给 9 月工单打标并算占比",
     "确认“上手”类占比是否真的上升，排除个别大客户抱怨被放大的可能。", "客服运营 · 本周二前"),
    ("流失客户回访 10 例", "9 月流失客户逐一访谈",
     "直接问“在哪一步卡住”，成本最低、说服力最强的定性证据。", "客户成功 · 本周四前"),
]
y = 2.0
for i, (h1, sub, why, who) in enumerate(gaps, 1):
    rect(s, ML, y, CW, 1.24, fill=None, line=LINE)
    rect(s, ML, y, 0.055, 1.24, fill=BLUE)
    text(s, ML + 0.32, y + 0.16, 0.4, 0.3, f"0{i}", size=15, bold=True, color=RGBColor(0xC2, 0xCB, 0xD6))
    text(s, ML + 0.85, y + 0.15, 4.0, 0.26, h1, size=13, bold=True, color=INK)
    text(s, ML + 0.85, y + 0.48, 4.0, 0.5, sub, size=10, color=MUTED, spacing=1.25)
    text(s, ML + 5.05, y + 0.16, 6.1, 0.26, "为什么必须补", size=9.5, bold=True, color=GRAY)
    text(s, ML + 5.05, y + 0.44, 6.1, 0.6, why, size=10, color=GRAY, spacing=1.25)
    text(s, W - ML - 2.1, y + 0.16, 2.0, 0.26, who, size=9.5, bold=True, color=BLUE, align=PP_ALIGN.RIGHT)
    y += 1.24 + 0.16

rect(s, ML, 6.24, CW, 0.66, fill=WASH)
text(s, ML + 0.3, 6.36, CW - 0.6, 0.42,
     "如果三组证据都指向试用期，则决策无需再等；如果证据相互矛盾，本季度的结论应改为“原因未明，Q4 目标下调”。",
     size=11, color=INK, spacing=1.2)

# =========================================================
# 9. Q4 PLAN
# =========================================================
s = slide_base("07 · 行动计划", "Q4 计划：先止血，再修增长",
               "四条举措按优先级排序，前两条不依赖新增预算")
footer(s, 9, "注：负责人与时间为本稿建议，需在 QBR 会上确认。")

rows = [
    ["P0", "试用期回调至 14 天", "恢复试用转化与上手时长", "产品负责人", "10/01", "试用→付费转化率"],
    ["P0", "新手引导重构（首日关键路径 ≤15 分钟）", "降低上手门槛", "产品 + 客户成功", "10/15", "首周激活率、上手类工单占比"],
    ["P1", "9 月流失客群专项挽回", "挽回 ≥8 家客户", "销售负责人", "11/15", "挽回 ARR"],
    ["P1", "流失与试用转化看板固化", "让同类改动可被提前发现", "数据团队", "10/31", "周度自动预警"],
]
cc = [[RED, INK, GRAY, INK, INK, GRAY], [RED, INK, GRAY, INK, INK, GRAY],
      [AMBER, INK, GRAY, INK, INK, GRAY], [AMBER, INK, GRAY, INK, INK, GRAY]]
table(s, ML, 1.95, CW, [0.7, 3.55, 2.6, 1.85, 0.85, 2.08], rows,
      ["优先级", "举措", "目标", "负责", "完成", "衡量指标"],
      row_h=0.62, hdr_h=0.44, size=10.5, cell_colors=cc,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

text(s, ML, 5.1, CW, 0.24, "Q4 衡量口径（建议）", size=11, bold=True, color=BLUE)
mets = [("止损线", "10–11 月流失 ≤ 18 家/月", RED),
        ("修复线", "12 月净新增转正（≥ +15）", AMBER),
        ("验证线", "试用转化率回到 7 月水平", TEAL)]
x = ML
for h1, v, col in mets:
    rect(s, x, 5.42, 3.7, 0.95, fill=WASH)
    rect(s, x, 5.42, 0.05, 0.95, fill=col)
    text(s, x + 0.28, 5.56, 3.3, 0.22, h1, size=10, bold=True, color=col)
    text(s, x + 0.28, 5.82, 3.3, 0.4, v, size=12.5, bold=True, color=INK)
    x += 3.7 + 0.28

text(s, ML, 6.6, CW, 0.3,
     "口径调整请求：Q4 目标建议由“收入增长 X%”改为“流失率与试用转化率先回到 7 月水平”，否则会激励团队用折扣掩盖漏损。",
     size=10, color=GRAY, italic=True)

# =========================================================
# 10. ASKS
# =========================================================
s = slide_base("08 · 决策请求", "需要 VP 在会上拍板的三件事", None)
footer(s, 10)

asks = [
    ("01", "批准试用期回调至 14 天", "本周内生效", RED,
     "影响：10 月转化率口径会有 1 个月波动\n风险：如果不做，10 月起进入净流失",
     "需要您：会上口头批准，并同步产品与销售"),
    ("02", "追加 2 名 onboarding 资源", "Q4 内到位", AMBER,
     "影响：Q4 增量人力成本\n替代：外包客服可临时承接，但效果打折",
     "需要您：与 HR 对齐 Q4 编制"),
    ("03", "同意 Q4 目标口径重设", "本次会议纪要中明确", BLUE,
     "影响：Q4 收入目标看起来更保守\n理由：先修漏损，再谈增长数字",
     "需要您：认可“先止血”的季度目标"),
]
x = ML
for num, h1, when, col, body, need in asks:
    rect(s, x, 1.95, 3.7, 3.5, fill=None, line=LINE)
    rect(s, x, 1.95, 3.7, 0.055, fill=col)
    text(s, x + 0.32, 2.16, 0.6, 0.4, num, size=20, bold=True, color=RGBColor(0xD5, 0xDB, 0xE3))
    text(s, x + 0.32, 2.62, 3.1, 0.72, h1, size=15, bold=True, color=INK, spacing=1.25)
    text(s, x + 0.32, 3.42, 3.1, 0.22, when, size=10, bold=True, color=col)
    hline(s, x + 0.32, 3.74, 3.06, LINE)
    text(s, x + 0.32, 3.88, 3.08, 1.0, body, size=9.5, color=GRAY, spacing=1.35)
    hline(s, x + 0.32, 4.72, 3.06, LINE)
    text(s, x + 0.32, 4.84, 3.08, 0.5, need, size=9.5, bold=True, color=INK, spacing=1.3)
    x += 3.7 + 0.28

rect(s, ML, 5.78, CW, 0.78, fill=NAVY)
text(s, ML + 0.34, 5.95, CW - 0.68, 0.46,
     "如果只批一件：请批第 1 件。它零成本、可逆、本周可执行，且能直接验证我们对根因的判断。",
     size=12.5, bold=True, color=WHITE, spacing=1.2)

# =========================================================
# 11. APPENDIX
# =========================================================
s = slide_base("APPENDIX", "附录：数据来源与口径说明", None)
footer(s, 11)

text(s, ML, 1.9, 5.6, 0.24, "数据来源", size=10.5, bold=True, color=BLUE)
text(s, ML, 2.2, 5.6, 1.5,
     "· 财务指标：data/q3-metrics.csv（2026-07 ~ 2026-09）\n"
     "· 定性证据：客服工单记录、内部工作日志\n"
     "· 未使用任何外部数据或估算值",
     size=10.5, color=GRAY, spacing=1.45)

text(s, ML, 3.62, 5.6, 0.24, "计算口径", size=10.5, bold=True, color=BLUE)
text(s, ML, 3.92, 5.6, 1.6,
     "· 净新增 = 当月新增 − 当月流失\n"
     "· Q3 收入 = 三个月合计 529,000\n"
     "· 环比 = 9 月 ÷ 7 月 − 1\n"
     "· NPS 取月末滚动值",
     size=10.5, color=GRAY, spacing=1.45)

text(s, ML + 6.15, 1.9, 5.5, 0.24, "已知局限", size=10.5, bold=True, color=RED)
lims = [
    "缺客户基数，无法计算流失率与留存率，只能用绝对量比较。",
    "无按试用时长拆分的转化数据，根因链条目前是“时间吻合 + 机制解释”，非因果证明。",
    "10 月外推为线性示意，未考虑季节性与销售节奏。",
    "客户投诉为定性描述（“明显变多”），尚无结构化占比。",
]
y = 2.2
_lb = s.shapes.add_textbox(Inches(ML + 6.15), Inches(2.18), Inches(5.45), Inches(2.9))
_ltf = _lb.text_frame
_ltf.word_wrap = True
_ltf.margin_left = _ltf.margin_right = _ltf.margin_top = _ltf.margin_bottom = 0
for i, t in enumerate(lims):
    p = _ltf.paragraphs[0] if i == 0 else _ltf.add_paragraph()
    p.line_spacing = 1.35
    p.space_after = Pt(14)
    _style_run(p.add_run(), 10, False, GRAY)
    p.runs[0].text = "▪  " + t

hline(s, ML, 5.5, CW, LINE)
text(s, ML, 5.66, CW, 0.24, "下一版补强", size=10.5, bold=True, color=BLUE)
text(s, ML, 5.95, CW, 0.7,
     "补入 7 天 / 14 天 cohort 转化率对比、9 月工单主题占比、流失客户访谈摘要后，本 deck 第 6 页可由“推断”升级为“结论”。",
     size=10.5, color=GRAY, spacing=1.35)

prs.save("/tmp/pf-17-without_skill-_rif3lst/Q3-2026-QBR.pptx")

# =========================================================
# SPEAKER NOTES
# =========================================================
NOTES = {
1: """开场（30 秒）
· 一句话定调：Q3 不是一次波动，是三个月同向的趋势。
· 先给结论再给数据：收入 -6%、净新增 29→6、NPS 38→27。
· 说明本次只有一个待决策事项：试用期是否回调。

提醒自己：不要在前 2 分钟就开始解释原因，先让对方接受“这是问题”。""",
2: """用法：这一页撑起整场汇报的骨架，后面每页都是它的展开。

· KPI 三块：收入 529K（-6.0%）、净新增 +6（原 +29）、NPS 27（-11）。
· 三条结论按“是什么 → 为什么 → 怎么办”排列。
· 右侧深色框是本次唯一要 VP 点头的事，务必停留 10 秒以上。

预判提问：“为什么现在才提？”
回答：因为 8 月的改动看起来只影响试用体验，直到 9 月工单和 NPS 同步恶化，
      才能把两者连起来——这也是第 8 页要补证据的原因。""",
3: """· 不要逐格念数字，只讲“每一个读数都比上一次差”。
· 重点停在“流失客户 +100%”：这是唯一一个翻倍的指标。
· 主动说明环比口径：9 月对 7 月，因为首月是季度起点。

若被问“流失率是多少”：目前拿不到客户基数，只能给绝对量（见附录局限性）。""",
4: """· 先讲事实：182K → 176K → 171K，降速在收窄但方向没变。
· 明确交代纵轴从 150K 起（已在脚注），避免被质疑夸大趋势。
· 10 月约 165K 是线性示意，不要说成预测。

预判提问：“是不是大客户丢单导致的？”
回答：需要按客户分层拆一次，本周可以补；但从流失家数看是普遍现象，不是单点。""",
5: """本页是全场最关键的一页——两条线在靠拢。

· 新增 41→30（-27%），流失 12→24（+100%）。
· 净新增 29→16→6，按每月 -10 的斜率，10 月转负。
· 明确“留给我们的窗口是一个月”，制造决策紧迫感。

预判提问：“为什么不加大获客投放把数字拉回来？”
回答：漏损没修好之前，每多买 100 个试用，流失比例更高（见右下）。""",
6: """链条讲法：一句一环，不要跳读。
① 触发：8/15 试用 14 天 → 7 天，未灰度。
② 机制：评估周期被压缩，客户在见到核心价值前被切断。
③ 信号：9/8 起“太难上手”工单激增，滞后约 3 周，符合先注册后卡住的节奏。
④ 结果：流失翻倍、新增下滑、NPS -11。

主动交代“这是推断，不是结论”，并指向第 8 页——主动示弱比被问出来好。""",
7: """· NPS 38→27，8 月就已跌破 30，9 月继续下探。
· 引用客户原声时不要加形容词，只念原话。
· 第三条信号最重要：贬损者上升通常领先流失 1-2 个月，意味着 10 月压力更大。""",
8: """这一页是给自己上保险，也是给 VP 的交期承诺。

· 三组证据分别对应产品分析、客服运营、客户成功，本周内可交。
· 关键句：如果证据矛盾，结论要改成“原因未明，Q4 目标下调”——先说出口，后面才不会被逼。
· 明确负责人和时间，现场确认，不要会后补。""",
9: """· P0 两条都不依赖新增预算——强调这一点，因为最容易获批。
· 每条举措都有可衡量的指标，避免“做了但说不清有没有用”。
· 衡量口径三条（止损 / 修复 / 验证）是关键：把“收入增长”换成“先止血”，需要 VP 认可。

预判提问：“10/01 上线是不是太急？”
回答：试用期改动本身就是一次配置变更，可回滚；越晚样本越脏。""",
10: """收口页，只讲三件事，每件 20 秒。

· 01 试用期回调（零成本、可逆、本周可执行）。
· 02 两名 onboarding 资源（唯一需要花钱的）。
· 03 Q4 目标口径重设（需要 VP 在会上背书）。

结束语用底部深色条那句：如果只批一件，请批第 1 件。
然后停下来等答复，不要再补充论证。""",
11: """放在最后，不主动讲；只在被质疑口径或数据时翻到这里。

· 数据来源只用了给定的 CSV 和工作日志，没有任何外部估算。
· 主动承认四条局限，尤其是“无客户基数”和“无 cohort 转化数据”。
· 最后一句话给出升级路径：补齐三组数据后，第 6 页可从“推断”改为“结论”。""",
}

for i, sl in enumerate(prs.slides, start=1):
    if i in NOTES:
        sl.notes_slide.notes_text_frame.text = NOTES[i]

prs.save("/tmp/pf-17-without_skill-_rif3lst/Q3-2026-QBR.pptx")
print("saved", len(prs.slides._sldIdLst), "slides")
