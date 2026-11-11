# -*- coding: utf-8 -*-
"""生成 Q3 2026 业务回顾（QBR）PPT。数据源：data/q3-metrics.csv + notes/worklog.md"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import (XL_CHART_TYPE, XL_TICK_MARK, XL_LEGEND_POSITION,
                            XL_MARKER_STYLE, XL_LABEL_POSITION)
from pptx.chart.data import CategoryChartData
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- 设计系统
FONT = "Microsoft YaHei"

INK    = RGBColor(0x10, 0x18, 0x2B)
SLATE  = RGBColor(0x47, 0x54, 0x67)
MUTED  = RGBColor(0x8A, 0x94, 0xA6)
BLUE   = RGBColor(0x25, 0x4B, 0xD8)
BLUE_T = RGBColor(0xEA, 0xEF, 0xFD)
RED    = RGBColor(0xC0, 0x39, 0x2E)
RED_T  = RGBColor(0xFB, 0xEC, 0xEA)
AMBER  = RGBColor(0xB4, 0x7A, 0x0B)
GREEN  = RGBColor(0x0B, 0x6B, 0x4F)
PANEL  = RGBColor(0xF7, 0xF8, 0xFA)
LINE   = RGBColor(0xE3, 0xE7, 0xEE)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)

W, H = 13.333, 7.5
L, R = 0.9, 12.43          # 内容左右边界
CW = R - L

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------- 工具函数
def set_font(run, size=None, bold=None, color=None, name=FONT):
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    run.font.name = name
    rPr = run._r.get_or_add_rPr()
    latin = rPr.find(qn("a:latin"))
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        if latin is not None:
            latin.addnext(ea)
        else:
            rPr.append(ea)
    ea.set("typeface", name)


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    return tf


def para(tf, text, size=14, bold=False, color=INK, align=PP_ALIGN.LEFT,
         space_before=0, space_after=0, line=1.35, first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if isinstance(text, str):
        text = [(text, {})]
    for chunk, opt in text:
        r = p.add_run()
        r.text = chunk
        set_font(r, opt.get("size", size), opt.get("bold", bold), opt.get("color", color))
    return p


def _strip_style(shape):
    el = shape._element
    style = el.find(qn("p:style"))
    if style is not None:
        el.remove(style)
    spPr = el.spPr
    for old in list(spPr):
        if old.tag == qn("a:effectLst"):
            spPr.remove(old)


def rect(slide, x, y, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE,
         radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    _strip_style(s)
    s.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
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
    s.text_frame.word_wrap = True
    return s


def hline(slide, x, y, w, color=LINE, lw=1.0):
    s = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    _strip_style(s)
    s.shadow.inherit = False
    s.line.color.rgb = color
    s.line.width = Pt(lw)
    return s


PAGE = {"n": 1}


def new_slide(kicker=None, title=None, sub=None, footer=True):
    s = prs.slides.add_slide(BLANK)
    PAGE["n"] += 1
    if kicker:
        tf = textbox(s, L, 0.46, CW, 0.28)
        para(tf, kicker, 10.5, True, BLUE, first=True)
    if title:
        tf = textbox(s, L, 0.72, CW, 0.55)
        para(tf, title, 27, True, INK, first=True, line=1.1)
    if sub:
        tf = textbox(s, L, 1.28, CW, 0.3)
        para(tf, sub, 12.5, False, SLATE, first=True)
    if footer:
        hline(s, L, 6.86, CW)
        tf = textbox(s, L, 6.98, 6, 0.25)
        para(tf, "Q3 2026 业务回顾 · 内部资料", 9, False, MUTED, first=True)
        tf = textbox(s, R - 1.2, 6.98, 1.2, 0.25)
        para(tf, f"{PAGE['n']:02d}", 9, True, MUTED, PP_ALIGN.RIGHT, first=True)
    return s


def style_chart(chart, name=FONT):
    chart.font.name = name
    chart.font.size = Pt(11)
    chart.font.color.rgb = SLATE
    cs = chart._chartSpace
    for latin in cs.iter(qn("a:latin")):
        parent = latin.getparent()
        ea = parent.find(qn("a:ea"))
        if ea is None:
            ea = parent.makeelement(qn("a:ea"), {})
            latin.addnext(ea)
        ea.set("typeface", name)


def chart_frame(chart):
    chart.has_title = False
    cs = chart._chartSpace
    spPr = cs.find(qn("c:spPr"))
    if spPr is None:
        spPr = cs.makeelement(qn("c:spPr"), {})
        cs.find(qn("c:chart")).addnext(spPr)
    for old in list(spPr):
        spPr.remove(old)
    spPr.append(spPr.makeelement(qn("a:noFill"), {}))
    ln = spPr.makeelement(qn("a:ln"), {"w": "0"})
    ln.append(ln.makeelement(qn("a:noFill"), {}))
    spPr.append(ln)


def axis_clean(ax, gridlines=False):
    ax.format.line.fill.background()
    if not gridlines:
        ax.has_major_gridlines = False
    ax.major_tick_mark = XL_TICK_MARK.NONE
    ax.minor_tick_mark = XL_TICK_MARK.NONE


# ================================================================ 1 封面
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, fill=RGBColor(0x0C, 0x14, 0x28))
rect(s, 0, 0, W, 0.12, fill=BLUE)
# 装饰：右侧渐隐色块
rect(s, 9.4, 0, 3.933, H, fill=RGBColor(0x11, 0x1C, 0x38))
rect(s, 9.4, 0, 0.02, H, fill=RGBColor(0x1E, 0x2E, 0x55))

tf = textbox(s, 1.0, 1.55, 8.0, 0.3)
para(tf, "QUARTERLY BUSINESS REVIEW", 11, True, RGBColor(0x7C, 0x9B, 0xFF), first=True)

tf = textbox(s, 1.0, 2.02, 8.4, 1.9)
para(tf, "Q3 2026", 62, True, WHITE, first=True, line=1.0)
para(tf, "业务回顾", 40, True, WHITE, space_before=2, line=1.15)

rect(s, 1.0, 4.36, 1.5, 0.045, fill=BLUE)

tf = textbox(s, 1.0, 4.72, 7.6, 1.2)
para(tf, "增长停滞与留存恶化：问题已从「获客」转移到「上手」", 16, False,
     RGBColor(0xC9, 0xD3, 0xE8), first=True, line=1.5)
para(tf, "汇报对象：VP    ｜    汇报人：业务负责人    ｜    2026 年 10 月", 11.5, False,
     RGBColor(0x8B, 0x99, 0xB5), space_before=14, line=1.4)

# 右侧关键数字
kpis = [("收入（Q3）", "52.9 万美元"), ("净新增客户", "+51"), ("NPS（9 月）", "27")]
y = 2.05
for lab, val in kpis:
    tf = textbox(s, 9.95, y, 2.9, 0.25)
    para(tf, lab, 10, False, RGBColor(0x8B, 0x99, 0xB5), first=True)
    tf = textbox(s, 9.95, y + 0.26, 2.9, 0.5)
    para(tf, val, 23, True, WHITE, first=True, line=1.1)
    y += 1.27

tf = textbox(s, 1.0, 6.62, 6.0, 0.25)
para(tf, "数据来源：内部经营看板（q3-metrics.csv）、客服工单与工作日志", 9, False,
     RGBColor(0x6B, 0x79, 0x95), first=True)

# ================================================================ 2 执行摘要
s = new_slide("EXECUTIVE SUMMARY", "执行摘要",
              "一个季度内，我们从「高速增长」切换到「增长停滞」，且恶化在逐月加速。")

items = [
    ("01", "收入连续两月下滑", BLUE,
     "Q3 收入 52.9 万美元，7→9 月分别为 18.2 / 17.6 / 17.1 万美元，"
     "环比分别下降 3.3% 和 2.8%。跌幅不大，但方向一致且未见拐点。"),
    ("02", "净新增接近归零，是本季最危险的信号", RED,
     "净新增客户 29 → 16 → 6（7/8/9 月）。流失/新增比从 29% 升至 80%，"
     "获客已几乎无法覆盖流失；NPS 同步从 38 跌至 27。"),
    ("03", "首要怀疑：试用期缩短削弱了上手体验", AMBER,
     "8 月中旬试用期由 14 天改为 7 天，9 月 8 日起「太难上手」类工单明显增多。"
     "时间为假设提供了支持，但尚未验证因果。"),
]
y = 1.92
for num, head, col, body in items:
    rect(s, L, y + 0.05, 0.035, 1.16, fill=col)
    tf = textbox(s, L + 0.28, y, 0.6, 0.35)
    para(tf, num, 12, True, col, first=True)
    tf = textbox(s, L + 0.92, y - 0.03, 6.45, 0.4)
    para(tf, head, 16.5, True, INK, first=True)
    tf = textbox(s, L + 0.92, y + 0.38, 6.45, 1.0)
    para(tf, body, 11.5, False, SLATE, first=True, line=1.6)
    y += 1.62

# 右侧结论卡
rect(s, 8.55, 1.92, 3.88, 4.28, fill=PANEL, line=LINE)
rect(s, 8.55, 1.92, 3.88, 0.05, fill=INK)
tf = textbox(s, 8.88, 2.2, 3.3, 0.3)
para(tf, "本季结论", 10.5, True, MUTED, first=True)
tf = textbox(s, 8.88, 2.55, 3.28, 2.3)
para(tf, "增长的重心已经从", 13, False, SLATE, first=True, line=1.6)
para(tf, "“拉新”", 20, True, INK, space_before=4, line=1.2)
para(tf, "转移到", 13, False, SLATE, space_before=4, line=1.6)
para(tf, "“上手与留存”", 20, True, BLUE, space_before=4, line=1.2)
tf = textbox(s, 8.88, 5.0, 3.28, 1.0)
para(tf, "Q4 的胜负手不在增加投放，而在把新用户的第一个 7 天做对。", 11, False,
     SLATE, first=True, line=1.6)
hline(s, 8.88, 5.72, 3.28, LINE)
tf = textbox(s, 8.88, 5.84, 3.3, 0.3)
para(tf, "—— 由此推出 3 项 Q4 举措（见 P7）", 9.5, True, BLUE, first=True)

# ================================================================ 3 核心指标
s = new_slide("SCORECARD", "核心指标看板",
              "四项指标同向恶化：收入下滑、净增归零、流失抬头、体验评分跌破 30。")

cards = [
    ("收入（Q3 合计）", "52.9", "万美元", "环比 -3.3% / -2.8%", RED),
    ("净新增客户", "51", "家", "7 月 29 → 9 月 6", RED),
    ("流失 / 新增", "80", "%", "从 29% 逐月攀升至 80%", RED),
    ("NPS（9 月）", "27", "分", "38 → 31 → 27，跌破警戒线", RED),
]
cw, gap = 2.72, 0.215
for i, (lab, val, unit, sub, col) in enumerate(cards):
    x = L + i * (cw + gap)
    rect(s, x, 1.72, cw, 1.52, fill=PANEL, line=LINE)
    rect(s, x, 1.72, 0.055, 1.52, fill=col)
    tf = textbox(s, x + 0.28, 1.9, cw - 0.5, 0.25)
    para(tf, lab, 10, True, MUTED, first=True)
    tf = textbox(s, x + 0.26, 2.18, cw - 0.45, 0.62)
    para(tf, [(val, {"size": 32, "bold": True, "color": INK}),
              (" " + unit, {"size": 11, "color": SLATE})], first=True, line=1.05)
    tf = textbox(s, x + 0.28, 2.87, cw - 0.5, 0.25)
    para(tf, sub, 9, False, col, first=True)

# 明细表
rows = [
    ("收入（千美元）", "182", "176", "171", "连续两月下滑，累计 -6.0%"),
    ("新增客户", "41", "35", "30", "逐月走低，9 月为季度最低"),
    ("流失客户", "12", "19", "24", "9 月为 7 月的两倍"),
    ("净新增客户", "29", "16", "6", "增长引擎接近停转"),
    ("NPS", "38", "31", "27", "跌破 30 警戒线"),
]
ty = 3.55
colx = [L, L + 3.35, L + 4.95, L + 6.55, L + 8.15]
colw = [3.35, 1.6, 1.6, 1.6, 4.28]
hdr = ["指标", "7 月", "8 月", "9 月", "读数"]
rect(s, L, ty, CW, 0.36, fill=RGBColor(0x1B, 0x24, 0x3A))
for x, w_, t in zip(colx, colw, hdr):
    tf = textbox(s, x + 0.16, ty + 0.085, w_ - 0.2, 0.24)
    para(tf, t, 10, True, WHITE, first=True)
ry = ty + 0.36
for i, r in enumerate(rows):
    if i % 2 == 0:
        rect(s, L, ry, CW, 0.42, fill=RGBColor(0xFA, 0xFB, 0xFC))
    hline(s, L, ry, CW, LINE, 0.75)
    tf = textbox(s, colx[0] + 0.16, ry + 0.11, colw[0] - 0.2, 0.26)
    para(tf, r[0], 10.5, True, INK, first=True)
    for j in range(1, 4):
        tf = textbox(s, colx[j] + 0.16, ry + 0.11, colw[j] - 0.2, 0.26)
        para(tf, r[j], 10.5, False, SLATE, first=True)
    tf = textbox(s, colx[4] + 0.16, ry + 0.115, colw[4] - 0.2, 0.26)
    para(tf, r[4], 10, False, RED if i != 0 else SLATE, first=True)
    ry += 0.44
hline(s, L, ry, CW, RGBColor(0xC9, 0xD0, 0xDC), 1.25)

tf = textbox(s, L, 6.36, CW, 0.3)
para(tf, [("注：", {"bold": True, "color": MUTED, "size": 9}),
          ("「流失/新增」= 月度流失客户数 ÷ 月度新增客户数，用于判断获客是否仍能覆盖流失；"
           "NPS 为月度脉冲调研得分（-100 ~ 100）。本页及后续页数据均取自 data/q3-metrics.csv。",
           {"color": MUTED, "size": 9})], first=True)

# ================================================================ 4 收入与增长
s = new_slide("REVENUE & GROWTH", "收入下滑，净新增接近归零",
              "收入跌幅温和，但净新增的塌陷速度远快于收入——问题在客户结构，而非单价。")

# 图 1：收入
tf = textbox(s, L, 1.72, 5.2, 0.28)
para(tf, "月度收入（千美元）", 11.5, True, INK, first=True)

cd = CategoryChartData()
cd.categories = ["7 月", "8 月", "9 月"]
cd.add_series("收入", (182, 176, 171))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(L - 0.15), Inches(2.0),
                        Inches(5.55), Inches(3.35), cd)
ch = gf.chart
style_chart(ch)
chart_frame(ch)
ch.has_legend = False
pl = ch.plots[0]
pl.has_data_labels = True
dl = pl.data_labels
dl.font.size = Pt(13)
dl.font.bold = True
dl.font.color.rgb = INK
dl.number_format = '0'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.ABOVE
ser = pl.series[0]
ser.format.line.color.rgb = BLUE
ser.format.line.width = Pt(2.75)
ser.smooth = False
ser.marker.style = XL_MARKER_STYLE.CIRCLE
ser.marker.size = 9
ser.marker.format.fill.solid()
ser.marker.format.fill.fore_color.rgb = BLUE
ser.marker.format.line.color.rgb = WHITE
ser.marker.format.line.width = Pt(1.75)

va = ch.value_axis
va.minimum_scale = 160
va.maximum_scale = 190
va.major_unit = 10
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xEE, 0xF1, 0xF5)
va.major_gridlines.format.line.width = Pt(0.75)
va.format.line.fill.background()
va.tick_labels.font.size = Pt(9.5)
va.tick_labels.font.color.rgb = MUTED
va.tick_labels.number_format = '"$"0"k"'
va.tick_labels.number_format_is_linked = False
va.major_tick_mark = XL_TICK_MARK.NONE
va.minor_tick_mark = XL_TICK_MARK.NONE
ca = ch.category_axis
axis_clean(ca)
ca.tick_labels.font.size = Pt(11)
ca.tick_labels.font.color.rgb = SLATE
ca.format.line.color.rgb = LINE

# 图 2：新增 vs 流失
tf = textbox(s, 6.5, 1.72, 5.9, 0.28)
para(tf, "新增客户 vs 流失客户（家）", 11.5, True, INK, first=True)

cd2 = CategoryChartData()
cd2.categories = ["7 月", "8 月", "9 月"]
cd2.add_series("新增客户", (41, 35, 30))
cd2.add_series("流失客户", (12, 19, 24))
gf2 = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(6.35), Inches(2.0),
                         Inches(6.1), Inches(3.35), cd2)
ch2 = gf2.chart
style_chart(ch2)
chart_frame(ch2)
ch2.has_legend = True
ch2.legend.position = XL_LEGEND_POSITION.TOP
ch2.legend.include_in_layout = False
ch2.legend.font.size = Pt(10)
ch2.legend.font.color.rgb = SLATE
pl2 = ch2.plots[0]
pl2.gap_width = 65
pl2.overlap = -12
pl2.has_data_labels = True
dl2 = pl2.data_labels
dl2.font.size = Pt(11)
dl2.font.bold = True
dl2.font.color.rgb = SLATE
dl2.number_format = '0'
dl2.number_format_is_linked = False
dl2.position = XL_LABEL_POSITION.OUTSIDE_END
pl2.series[0].format.fill.solid()
pl2.series[0].format.fill.fore_color.rgb = RGBColor(0x7D, 0x9B, 0xF2)
pl2.series[1].format.fill.solid()
pl2.series[1].format.fill.fore_color.rgb = RGBColor(0xE0, 0x8C, 0x84)
for ser in pl2.series:
    ser.format.line.fill.background()

va2 = ch2.value_axis
va2.minimum_scale = 0
va2.maximum_scale = 45
va2.major_unit = 15
va2.has_major_gridlines = True
va2.major_gridlines.format.line.color.rgb = RGBColor(0xEE, 0xF1, 0xF5)
va2.major_gridlines.format.line.width = Pt(0.75)
va2.format.line.fill.background()
va2.tick_labels.font.size = Pt(9.5)
va2.tick_labels.font.color.rgb = MUTED
va2.major_tick_mark = XL_TICK_MARK.NONE
va2.minor_tick_mark = XL_TICK_MARK.NONE
ca2 = ch2.category_axis
axis_clean(ca2)
ca2.tick_labels.font.size = Pt(11)
ca2.tick_labels.font.color.rgb = SLATE
ca2.format.line.color.rgb = LINE

# 结论条
rect(s, L, 5.62, CW, 1.06, fill=RGBColor(0xFD, 0xF6, 0xF5), line=None)
rect(s, L, 5.62, 0.055, 1.06, fill=RED)
tf = textbox(s, L + 0.32, 5.78, CW - 0.6, 0.75)
para(tf, [("读法：", {"bold": True, "color": RED, "size": 11.5}),
          ("7 月每流失 1 家客户能换来 3.4 家新客，9 月只能换来 1.25 家。",
           {"color": SLATE, "size": 11.5})], first=True, line=1.6)
para(tf, "按此斜率外推，Q4 净新增将转负——收入下滑也会从「结构性」变成「绝对值」。",
     11.5, False, SLATE, space_before=5, line=1.6)

# ================================================================ 5 留存与体验
s = new_slide("RETENTION & EXPERIENCE", "流失与体验同步恶化",
              "NPS 三个月连跌 11 分，与流失率上升、新增下滑发生在同一窗口。")

# 左：NPS 折线
tf = textbox(s, L, 1.72, 5.2, 0.28)
para(tf, "NPS 走势（分）", 11.5, True, INK, first=True)
cd3 = CategoryChartData()
cd3.categories = ["7 月", "8 月", "9 月"]
cd3.add_series("NPS", (38, 31, 27))
gf3 = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(L - 0.15), Inches(2.0),
                         Inches(5.5), Inches(2.85), cd3)
ch3 = gf3.chart
style_chart(ch3)
chart_frame(ch3)
ch3.has_legend = False
pl3 = ch3.plots[0]
pl3.has_data_labels = True
dl3 = pl3.data_labels
dl3.font.size = Pt(13)
dl3.font.bold = True
dl3.font.color.rgb = INK
dl3.number_format = '0'
dl3.number_format_is_linked = False
dl3.position = XL_LABEL_POSITION.ABOVE
ser3 = pl3.series[0]
ser3.format.line.color.rgb = AMBER
ser3.format.line.width = Pt(2.75)
ser3.smooth = False
ser3.marker.style = XL_MARKER_STYLE.CIRCLE
ser3.marker.size = 9
ser3.marker.format.fill.solid()
ser3.marker.format.fill.fore_color.rgb = AMBER
ser3.marker.format.line.color.rgb = WHITE
ser3.marker.format.line.width = Pt(1.75)
va3 = ch3.value_axis
va3.minimum_scale = 20
va3.maximum_scale = 40
va3.major_unit = 10
va3.has_major_gridlines = True
va3.major_gridlines.format.line.color.rgb = RGBColor(0xEE, 0xF1, 0xF5)
va3.major_gridlines.format.line.width = Pt(0.75)
va3.format.line.fill.background()
va3.tick_labels.font.size = Pt(9.5)
va3.tick_labels.font.color.rgb = MUTED
va3.major_tick_mark = XL_TICK_MARK.NONE
va3.minor_tick_mark = XL_TICK_MARK.NONE
ca3 = ch3.category_axis
axis_clean(ca3)
ca3.tick_labels.font.size = Pt(11)
ca3.tick_labels.font.color.rgb = SLATE
ca3.format.line.color.rgb = LINE

# 左下：预警
rect(s, L, 5.2, 5.25, 1.02, fill=PANEL, line=LINE)
tf = textbox(s, L + 0.3, 5.35, 4.7, 0.8)
para(tf, "NPS 27 = 贬损者多于推荐者", 11.5, True, INK, first=True)
para(tf, "低于 30 通常意味着口碑带不动新增，获客成本会随之抬升；"
         "本季新增的下滑部分是这一结果的滞后反映。", 10, False, SLATE,
     space_before=6, line=1.55)

# 右：工单证据卡
rect(s, 6.5, 1.72, 5.93, 2.62, fill=RGBColor(0xFB, 0xF7, 0xEF), line=None)
rect(s, 6.5, 1.72, 0.055, 2.62, fill=AMBER)
tf = textbox(s, 6.85, 1.92, 5.3, 0.3)
para(tf, "来自一线的证据", 10.5, True, AMBER, first=True)
tf = textbox(s, 6.85, 2.26, 5.3, 1.9)
para(tf, "「9 月 8 日起，客服工单里“太难上手”的投诉明显变多。」", 15, True, INK,
     first=True, line=1.5)
para(tf, "—— 客服工作日志，2026-09", 9.5, False, MUTED, space_before=10, line=1.4)
hline(s, 6.85, 3.55, 5.3, RGBColor(0xE7, 0xDD, 0xCA))
tf = textbox(s, 6.85, 3.65, 5.3, 0.6)
para(tf, [("注意：", {"bold": True, "size": 9.5, "color": AMBER}),
          ("这是定性观察，工单量未做结构化统计，Q4 需补上「上手失败原因」标签。",
           {"size": 9.5, "color": SLATE})], first=True, line=1.5)

# 右下：三个同步信号
tf = textbox(s, 6.5, 4.55, 5.9, 0.3)
para(tf, "三个信号在同一个窗口出现", 11.5, True, INK, first=True)
sig = [("新增 ↓", "41 → 35 → 30"), ("流失 ↑", "12 → 19 → 24"), ("NPS ↓", "38 → 31 → 27")]
for i, (a, b) in enumerate(sig):
    x = 6.5 + i * 2.0
    rect(s, x, 4.95, 1.86, 0.85, fill=PANEL, line=LINE)
    tf = textbox(s, x + 0.16, 5.08, 1.6, 0.25)
    para(tf, a, 10, True, RED, first=True)
    tf = textbox(s, x + 0.16, 5.36, 1.6, 0.28)
    para(tf, b, 11.5, True, INK, first=True)
tf = textbox(s, 6.5, 5.98, 5.9, 0.6)
para(tf, "三者在时间上同步，说明更可能来自同一个体验层面的原因，而不是三个独立问题。",
     10.5, False, SLATE, first=True, line=1.55)

# ================================================================ 6 根因
s = new_slide("HYPOTHESIS", "根因假设：试用期 14 天 → 7 天",
              "时间线高度吻合，但我们只有相关性——这一区分必须对 VP 讲清楚。")

# 时间线
ty = 2.72
rect(s, L + 0.3, ty - 0.012, CW - 0.6, 0.024, fill=RGBColor(0xD5, 0xDB, 0xE5))
nodes = [
    (1.55, "7 月", "基线期", "试用 14 天；新增 41、流失 12。", BLUE),
    (4.9, "8 月中旬", "改动发生", "免费试用由 14 天缩短为 7 天。", AMBER),
    (8.05, "9 月 8 日起", "体验投诉", "「太难上手」类工单明显增多。", RED),
    (11.2, "9 月", "结果恶化", "新增 30，流失 24，NPS 27。", RED),
]
for i, (x, date, tag, body, col) in enumerate(nodes):
    cx = x + 0.9
    rect(s, cx - 0.115, ty - 0.115, 0.23, 0.23, fill=col, shape=MSO_SHAPE.OVAL)
    rect(s, cx - 0.045, ty - 0.045, 0.09, 0.09, fill=WHITE, shape=MSO_SHAPE.OVAL)
    tf = textbox(s, x, ty - 0.88, 1.85, 0.3)
    para(tf, date, 12.5, True, col, PP_ALIGN.CENTER, first=True)
    tf = textbox(s, x, ty - 0.57, 1.85, 0.26)
    para(tf, tag, 9.5, False, MUTED, PP_ALIGN.CENTER, first=True)
    tf = textbox(s, x - 0.38, ty + 0.26, 2.6, 0.95)
    para(tf, body, 10, False, SLATE, PP_ALIGN.CENTER, first=True, line=1.55)

# 因果链
tf = textbox(s, L, 4.02, CW, 0.3)
para(tf, "推断的传导链（待验证）", 11.5, True, INK, first=True)
chain = ["试用期缩短", "上手时间不足", "激活率下降", "付费转化降低\n早期流失升高", "净新增归零"]
bx, bw, bg = L, 2.146, 0.20
for i, t in enumerate(chain):
    x = bx + i * (bw + bg)
    last = (i == len(chain) - 1)
    rect(s, x, 4.42, bw, 0.76, fill=RED_T if last else PANEL, line=None if last else LINE)
    tf = textbox(s, x + 0.1, 4.42, bw - 0.2, 0.76, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, t, 10.5, last, RED if last else INK, PP_ALIGN.CENTER, first=True, line=1.45)
    if not last:
        tf = textbox(s, x + bw, 4.42, bg, 0.76, anchor=MSO_ANCHOR.MIDDLE)
        para(tf, "→", 12, True, RGBColor(0x98, 0xA2, 0xB3), PP_ALIGN.CENTER, first=True)

# 诚实声明
rect(s, L, 5.58, CW, 0.86, fill=RGBColor(0xF3, 0xF7, 0xFF), line=None)
rect(s, L, 5.58, 0.055, 0.86, fill=BLUE)
tf = textbox(s, L + 0.32, 5.7, CW - 0.65, 0.64)
para(tf, [("为什么仍以它为首要假设：", {"bold": True, "size": 10.5, "color": BLUE}),
          ("① 时间顺序正确（改动在前，恶化在后）；② 投诉内容直指上手；③ 新增、流失、NPS 三者同步变化。"
           "但它仍是假设——Q4 需用分群对比或 A/B 验证，避免为错误的病因开药。",
           {"size": 10.5, "color": SLATE})], first=True, line=1.55)

# ================================================================ 7 下季计划
s = new_slide("PLAN", "Q4 计划：三件事，对应一个目标",
              "把试用与上手做对，同时抢救已在流失边缘的客户。")

plans = [
    ("举措一", "恢复 14 天试用，并重做激活路径", BLUE,
     ["将试用期恢复至 14 天，同时上线「首个成功动作」引导（三步内到达核心价值）",
      "按 8 周 A/B 验证：缩短试用期是否真的影响转化"],
     "激活率、试用→付费转化率", "产品 + 工程"),
    ("举措二", "对 8–9 月的流失客户做定向挽回", RED,
     ["对 Q3 流失客户做 1v1 回访，区分「上手失败」与「无真实需求」",
      "对上手失败群体：30 天免费延长与一对一陪跑"],
     "挽回率、流失/新增比", "客户成功"),
    ("举措三", "把「太难上手」变成可量化的问题", AMBER,
     ["给工单加上「上手失败」结构化标签，联动产品埋点定位断点",
      "每周复盘 Top3 断点，滚动发布修复"],
     "上手类工单占比、Time-to-Value", "客服 + 产品"),
]
cw3, gap3 = 3.72, 0.185
for i, (tag, title, col, actions, metric, owner) in enumerate(plans):
    x = L + i * (cw3 + gap3)
    rect(s, x, 1.72, cw3, 3.05, fill=PANEL, line=LINE)
    rect(s, x, 1.72, cw3, 0.05, fill=col)
    tf = textbox(s, x + 0.28, 1.92, cw3 - 0.5, 0.25)
    para(tf, tag, 9.5, True, col, first=True)
    tf = textbox(s, x + 0.28, 2.18, cw3 - 0.45, 0.6)
    para(tf, title, 13.5, True, INK, first=True, line=1.4)
    tf = textbox(s, x + 0.28, 2.82, cw3 - 0.45, 1.45)
    for k, a in enumerate(actions):
        para(tf, [("· ", {"color": col, "bold": True}), (a, {})], 9.5, False, SLATE,
             first=(k == 0), line=1.55, space_after=6)
    hline(s, x + 0.28, 4.02, cw3 - 0.56, LINE)
    tf = textbox(s, x + 0.28, 4.12, cw3 - 0.45, 0.6)
    para(tf, [("衡量：", {"bold": True, "size": 9, "color": MUTED}),
              (metric, {"size": 9, "color": SLATE})], first=True, line=1.45)
    para(tf, [("负责：", {"bold": True, "size": 9, "color": MUTED}),
              (owner, {"size": 9, "color": SLATE})], space_before=3, line=1.45)

# Q4 目标
tf = textbox(s, L, 5.02, 5.0, 0.3)
para(tf, "Q4 建议目标（需 VP 认可后锁定）", 11.5, True, INK, first=True)
targets = [("收入", "≥ 54.0 万美元", "Q3 为 52.9"), ("净新增", "≥ 60 家", "Q3 为 51"),
           ("NPS", "≥ 35 分", "9 月为 27"), ("流失/新增", "≤ 40%", "9 月为 80%")]
for i, (lab, val, base) in enumerate(targets):
    x = L + i * 2.95
    rect(s, x, 5.42, 2.8, 0.76, fill=WHITE, line=LINE)
    tf = textbox(s, x + 0.2, 5.51, 2.45, 0.24)
    para(tf, lab, 9, True, MUTED, first=True)
    tf = textbox(s, x + 0.2, 5.74, 2.45, 0.3)
    para(tf, [(val, {"size": 13.5, "bold": True, "color": GREEN}),
              ("  " + base, {"size": 8.5, "color": MUTED})], first=True)
tf = textbox(s, L, 6.40, CW, 0.22)
para(tf, "目标为基于现状的挑战值，非承诺值；若 Q4 第 4 周仍未止跌，将提前启动第二套方案（价格与打包策略）。",
     9, False, MUTED, first=True)

# ================================================================ 8 支持
s = new_slide("ASKS", "需要的支持与决策",
              "三项资源 + 一个需要当场拍板的决策。")

asks = [
    ("决策", "是否同意恢复 14 天试用并做 8 周 A/B？", BLUE,
     "需要你把「短期转化率」的考核口径放宽一个季度，否则团队没有空间做这个实验。", "本周内"),
    ("资源", "2 人周工程 + 1 名客服增援", RED,
     "用于引导流程改造、工单标签体系搭建，以及 Q3 流失客户的 1v1 回访。", "Q4 第 1 周到位"),
    ("预算", "流失挽回成本上限 5 万美元", AMBER,
     "主要用于 30 天免费延长与一对一陪跑，按挽回客户数结算，可控。", "Q4 内弹性使用"),
]
y = 1.82
for tag, head, col, body, when in asks:
    rect(s, L, y, CW, 1.18, fill=PANEL, line=LINE)
    rect(s, L, y, 0.055, 1.18, fill=col)
    tf = textbox(s, L + 0.32, y + 0.2, 1.1, 0.28)
    para(tf, tag, 10, True, col, first=True)
    tf = textbox(s, L + 1.45, y + 0.16, 6.9, 0.36)
    para(tf, head, 14.5, True, INK, first=True)
    tf = textbox(s, L + 1.45, y + 0.6, 6.9, 0.5)
    para(tf, body, 10.5, False, SLATE, first=True, line=1.5)
    tf = textbox(s, L + 8.9, y + 0.24, 2.3, 0.7, anchor=MSO_ANCHOR.MIDDLE)
    para(tf, when, 10.5, True, col, PP_ALIGN.RIGHT, first=True, line=1.4)
    y += 1.34

rect(s, L, 5.88, CW, 0.85, fill=RGBColor(0xF3, 0xF7, 0xFF), line=None)
rect(s, L, 5.88, 0.055, 0.85, fill=BLUE)
tf = textbox(s, L + 0.32, 5.88, CW - 0.65, 0.85, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("如果只能记住一件事：", {"bold": True, "size": 11, "color": BLUE}),
          ("Q3 的问题不是卖得不够多，而是新客户没能在 7 天内用起来。Q4 请把资源从「拉新」挪一部分到「上手」。",
           {"size": 11, "color": SLATE})], first=True, line=1.55)

# ================================================================ 9 附录
s = new_slide("APPENDIX", "附录：数据明细与口径",
              "全部数字均可追溯到原始数据文件，便于交叉核对。")

rows = [
    ("2026-07", "182,000", "41", "12", "38", "29"),
    ("2026-08", "176,000", "35", "19", "31", "16"),
    ("2026-09", "171,000", "30", "24", "27", "6"),
    ("Q3 合计", "529,000", "106", "55", "—", "51"),
]
hdr = ["月份", "收入（美元）", "新增客户", "流失客户", "NPS", "净新增"]
colx2 = [L, L + 1.9, L + 4.3, L + 6.35, L + 8.4, L + 10.0]
colw2 = [1.9, 2.4, 2.05, 2.05, 1.6, 2.43]
ty = 1.82
rect(s, L, ty, CW, 0.4, fill=RGBColor(0x1B, 0x24, 0x3A))
for x, w_, t in zip(colx2, colw2, hdr):
    tf = textbox(s, x + 0.18, ty + 0.11, w_ - 0.2, 0.24)
    para(tf, t, 10.5, True, WHITE, first=True)
ry = ty + 0.4
for i, r in enumerate(rows):
    last = (i == len(rows) - 1)
    if last:
        rect(s, L, ry, CW, 0.42, fill=RGBColor(0xF2, 0xF4, 0xF8))
    elif i % 2 == 0:
        rect(s, L, ry, CW, 0.42, fill=RGBColor(0xFA, 0xFB, 0xFC))
    hline(s, L, ry, CW, LINE, 0.75)
    for j, v in enumerate(r):
        tf = textbox(s, colx2[j] + 0.18, ry + 0.11, colw2[j] - 0.2, 0.26)
        para(tf, v, 10.5, last or j == 0, INK if (last or j == 0) else SLATE, first=True)
    ry += 0.42
hline(s, L, ry, CW, RGBColor(0xC9, 0xD0, 0xDC), 1.25)

defs = [
    ("数据来源", "data/q3-metrics.csv（月度收入、新增/流失客户数、NPS）；定性信息来自 notes/worklog.md。"),
    ("净新增客户", "新增客户数 − 流失客户数，按月计算；季度值 51 = 106 − 55，与各月净新增之和一致。"),
    ("流失/新增比", "月度流失客户数 ÷ 月度新增客户数。Q3 合计 55 ÷ 106 = 52%；9 月单月 24 ÷ 30 = 80%。"),
    ("NPS", "月度脉冲调研得分，范围 -100 ~ 100；本报告未披露样本量，Q4 需补充样本量与置信区间。"),
]
y = 4.46
tf = textbox(s, L, 4.06, CW, 0.28)
para(tf, "口径说明", 11.5, True, INK, first=True)
for k, v in defs:
    tf = textbox(s, L, y, 2.0, 0.6)
    para(tf, k, 10, True, SLATE, first=True, line=1.5)
    tf = textbox(s, L + 2.1, y, CW - 2.2, 0.6)
    para(tf, v, 10, False, SLATE, first=True, line=1.5)
    y += 0.55

tf = textbox(s, L, 6.50, CW, 0.25)
para(tf, "Q3 环比：8 月 -3.3%、9 月 -2.8%；7→9 月累计 -6.0%。上表为未取整原始值。",
     9, False, MUTED, first=True)

NOTES = {
    1: "开场 30 秒：本季度不是营收灾难，是增长引擎熄火。先给结论，再给证据，最后要决策。",
    2: "讲这页时把「净新增 29→16→6」念出来，这是全场最该被记住的一组数字。",
    3: "两张图放在一起看：收入只是缓降，净新增是断崖。结论是问题在客户结构。",
    5: "如果 VP 质疑「证据够不够」，直接承认：我们只有相关性。但三件事同时发生，值得用 8 周实验去验证。",
    7: "这页是全场唯一需要 VP 当场表态的地方：是否接受把转化率考核口径放宽一个季度。",
}
for i, sl in enumerate(prs.slides):
    if i in NOTES:
        sl.notes_slide.notes_text_frame.text = NOTES[i]

prs.save("Q3-2026-QBR.pptx")
print("saved", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
