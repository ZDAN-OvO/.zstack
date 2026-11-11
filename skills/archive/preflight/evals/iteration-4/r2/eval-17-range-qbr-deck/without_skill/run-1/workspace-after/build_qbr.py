# -*- coding: utf-8 -*-
"""Q3 2026 QBR deck builder."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION, XL_MARKER_STYLE,
                             XL_TICK_MARK, XL_LEGEND_POSITION)

# ---------- tokens ----------
FONT = "Noto Sans CJK SC"
INK    = "0F1B2A"
SLATE  = "5A6B7C"
MUTED  = "8A97A6"
LINE   = "DCE3EA"
PANEL  = "F4F7FA"
WHITE  = "FFFFFF"
BLUE   = "2F6FEB"
AMBER  = "C2410C"
GREEN  = "0E7C6B"
COVER_SUB = "9FB0C3"

W, H = 13.333, 7.5
M = 0.85
CW = W - 2 * M   # 11.633

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]

MONTHS = ["7 月", "8 月", "9 月"]
REV = [182000, 176000, 171000]
NEW = [41, 35, 30]
CHURN = [12, 19, 24]
NPS = [38, 31, 27]


def hexc(h):
    return RGBColor.from_string(h)


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = hexc(fill)
    s.line.fill.background()
    s.shadow.inherit = False
    for st in s._element.findall(qn('p:style')):
        s._element.remove(st)
    return s


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def para(tf, first, runs, size, color, line=1.35, before=0, align=PP_ALIGN.LEFT):
    """runs: str or list of (text, dict(overrides))"""
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line
    p.space_before = Pt(before)
    p.space_after = Pt(0)
    if isinstance(runs, str):
        runs = [(runs, {})]
    for text, ov in runs:
        r = p.add_run()
        r.text = text
        f = r.font
        f.name = ov.get("font", FONT)
        f.size = Pt(ov.get("size", size))
        f.bold = ov.get("bold", False)
        f.color.rgb = hexc(ov.get("color", color))
    return p


def simple(slide, x, y, w, h, text, size, color, bold=False,
           line=1.35, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = textbox(slide, x, y, w, h, anchor)
    para(tf, True, [(text, {"bold": bold})], size, color, line, align=align)
    return tf


def slide_head(slide, kicker, title, sub=None):
    simple(slide, M, 0.52, CW, 0.24, kicker, 9.5, BLUE, bold=True)
    simple(slide, M, 0.78, CW, 0.52, title, 26, INK, bold=True, line=1.1)
    rect(slide, M, 1.42, 0.62, 0.035, BLUE)
    if sub:
        simple(slide, M, 1.62, 10.6, 0.4, sub, 12.5, SLATE, line=1.4)


def footer(slide, idx, total):
    simple(slide, M, 7.02, 6.0, 0.25, "Q3 2026 业务回顾  ·  内部资料", 9, MUTED)
    simple(slide, W - M - 1.2, 7.02, 1.2, 0.25, f"{idx:02d} / {total:02d}", 9, MUTED, align=PP_ALIGN.RIGHT)


def style_chart(chart):
    chart.font.name = FONT
    chart.font.size = Pt(10)
    chart.font.color.rgb = hexc(SLATE)


def axis_chrome(chart, ymin=None, ymax=None, fmt='0'):
    va = chart.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = hexc(LINE)
    va.major_gridlines.format.line.width = Pt(0.75)
    va.format.line.fill.background()
    va.major_tick_mark = XL_TICK_MARK.NONE
    va.minor_tick_mark = XL_TICK_MARK.NONE
    if ymin is not None:
        va.minimum_scale = ymin
    if ymax is not None:
        va.maximum_scale = ymax
    va.tick_labels.font.size = Pt(9.5)
    va.tick_labels.font.color.rgb = hexc(MUTED)
    va.tick_labels.font.name = FONT
    va.tick_labels.number_format = fmt
    va.tick_labels.number_format_is_linked = False

    ca = chart.category_axis
    ca.format.line.color.rgb = hexc(LINE)
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.minor_tick_mark = XL_TICK_MARK.NONE
    ca.tick_labels.font.size = Pt(10)
    ca.tick_labels.font.color.rgb = hexc(SLATE)
    ca.tick_labels.font.name = FONT


def kpi_card(slide, x, y, w, label, value, delta, delta_color):
    rect(slide, x, y, w, 1.22, PANEL)
    simple(slide, x + 0.26, y + 0.18, w - 0.5, 0.22, label, 9.5, SLATE, bold=True)
    simple(slide, x + 0.26, y + 0.44, w - 0.5, 0.42, value, 26, INK, bold=True, line=1.0)
    simple(slide, x + 0.26, y + 0.9, w - 0.5, 0.2, delta, 9, delta_color)


def callout(slide, x, y, w, h, content, size=12, pad=0.3, fill=PANEL, accent=BLUE, blocks=False):
    rect(slide, x, y, w, h, fill)
    rect(slide, x, y, 0.045, h, accent)
    tf = textbox(slide, x + pad, y + 0.14, w - 2 * pad, h - 0.28, MSO_ANCHOR.MIDDLE)
    # content = list of runs (single paragraph), or list of (runs, opts) when blocks=True
    specs = content if blocks else [(content, {})]
    for i, (runs, ov) in enumerate(specs):
        para(tf, i == 0, runs, ov.get("size", size), ov.get("color", INK),
             line=ov.get("line", 1.45), before=ov.get("before", 10 if i else 0))


TOTAL_SLIDES = 8

# ============================== 1. COVER ==============================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, INK)
simple(s, 9.05, 0.6, 3.6, 2.4, "Q3", 145, "1A2A3D", bold=True, align=PP_ALIGN.RIGHT)
simple(s, M, 1.95, 9.0, 0.3, "季度业务回顾  /  QUARTERLY BUSINESS REVIEW", 10, COVER_SUB, bold=True)
rect(s, M, 2.42, 0.7, 0.04, BLUE)
simple(s, M, 2.7, 9.0, 0.9, "Q3 业务回顾", 46, WHITE, bold=True, line=1.1)
simple(s, M, 3.72, 9.0, 0.4, "2026 年 7–9 月  ·  收入、客户与体验", 16, COVER_SUB)
rect(s, M, 5.35, CW, 0.012, "2A3A4E")
simple(s, M, 5.62, 5.2, 0.3, "汇报对象：VP      汇报日期：2026 年 10 月", 10.5, COVER_SUB)
simple(s, M, 5.98, 5.2, 0.3, "数据口径：月度经营看板（data/q3-metrics.csv）", 10.5, "6E7F92")
simple(s, M, 6.62, 8.0, 0.3, "本期核心问题：收入连续三月下滑，原因是什么、下季怎么止住。", 11, "6E7F92")
s.notes_slide.notes_text_frame.text = (
    "开场 30 秒：Q3 收入 $529K，但 7 月到 9 月连续两个月下滑，累计 -6.0%。"
    "今天不只汇报结果，重点讲清一个判断和一个决策请求。"
)

# ============================== 2. EXEC SUMMARY ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "EXECUTIVE SUMMARY", "执行摘要",
           "Q3 收入 $529K，客户与体验指标连续三月走弱；8 月中旬试用期由 14 天缩短至 7 天，是与拐点时间最吻合的变量。")

cw4 = (CW - 3 * 0.24) / 4
cards = [
    ("Q3 收入", "$529K", "较 7 月 −6.0%", AMBER),
    ("净新增客户", "+51", "月度 +29 → +6", AMBER),
    ("流失客户", "55", "月度 12 → 24（+100%）", AMBER),
    ("NPS", "27", "较 7 月 −11 分", AMBER),
]
for i, (lab, val, d, c) in enumerate(cards):
    kpi_card(s, M + i * (cw4 + 0.24), 2.2, cw4, lab, val, d, c)

simple(s, M, 3.78, 3.0, 0.25, "关键结论", 10, SLATE, bold=True)
concl = [
    ("增长在减速",
     "新增客户 41 → 35 → 30，净新增从 +29 降至 +6，Q3 净增仅 51 家。"),
    ("流失在翻倍",
     "月度流失 12 → 24，9 月流失/新增比达 80%，流失规模正接近吞掉全部新增。"),
    ("体验先恶化",
     "NPS 38 → 27；9 月 8 日起「太难上手」类工单明显增多，Q4 流失仍有上行压力。"),
]
yy = 4.18
for i, (lead, body) in enumerate(concl):
    simple(s, M, yy, 0.45, 0.3, f"0{i+1}", 13, BLUE, bold=True)
    tf = textbox(s, M + 0.55, yy - 0.02, CW - 0.6, 0.72)
    para(tf, True, [(lead + " — ", {"bold": True, "color": INK}), (body, {"color": SLATE})],
         13, INK, line=1.4)
    yy += 0.78
footer(s, 2, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "四个指标全部转负，不是单点波动。强调第 3 条：NPS 是先行指标，流失通常滞后 1 个月，"
    "所以 Q4 的流失压力还没释放完。"
)

# ============================== 3. REVENUE ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "01  收入", "收入连续两月环比下滑，降幅没有收窄",
           "Q3 合计 $529K；8 月 −3.3%、9 月 −2.8%，仍在同一斜率上。")

cd = CategoryChartData()
cd.categories = MONTHS
cd.add_series("收入", tuple(REV))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(M - 0.12), Inches(2.05),
                        Inches(7.1), Inches(4.35), cd)
chart = gf.chart
style_chart(chart)
chart.has_title = False
chart.has_legend = False
axis_chrome(chart, ymin=160000, ymax=190000, fmt='$#,##0,"K"')
plot = chart.plots[0]
ser = plot.series[0]
ser.format.line.color.rgb = hexc(BLUE)
ser.format.line.width = Pt(2.5)
ser.marker.style = XL_MARKER_STYLE.CIRCLE
ser.marker.size = 9
ser.marker.format.fill.solid()
ser.marker.format.fill.fore_color.rgb = hexc(WHITE)
ser.marker.format.line.color.rgb = hexc(BLUE)
ser.marker.format.line.width = Pt(2.5)
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '$#,##0,"K"'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.ABOVE
dl.font.size = Pt(12)
dl.font.bold = True
dl.font.color.rgb = hexc(INK)
dl.font.name = FONT

simple(s, M - 0.05, 6.45, 6.9, 0.25, "纵轴自 $160K 起，用于放大趋势；绝对数值见数据标签。",
       8.5, MUTED)

X = 8.15
simple(s, X, 2.15, 4.3, 0.25, "发生了什么", 10, SLATE, bold=True)
tf = textbox(s, X, 2.5, 4.3, 1.9)
para(tf, True, [("7→9 月收入累计 ", {}), ("−6.0%", {"bold": True, "color": AMBER}),
                ("，三个月减少约 $11K/月。", {})], 12.5, INK, line=1.45)
para(tf, False, [("环比降幅 3.3% → 2.8%，说明不是一次性冲击，而是", {}),
                 ("持续性流失", {"bold": True, "color": INK}), ("。", {})], 12.5, INK, before=8, line=1.45)

callout(s, X, 4.5, 4.35, 1.3,
        [("口径缺口：", {"bold": True, "color": AMBER}),
         ("本次数据不含 ARPU / 折扣率，因此还不能排除单价因素。建议 Q4 看板补齐后再做归因定论。", {})],
        size=11, accent=AMBER)
simple(s, X, 5.98, 4.35, 0.5, "行动指向：先把「量」的问题（新增↓、流失↑）解决，再谈「价」。",
       11, SLATE, line=1.4)
footer(s, 3, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "如果被问「是不是降价导致的」，直接答：现有口径回答不了，这是我们要补的第一个数据缺口，"
    "不要凭感觉下结论。"
)

# ============================== 4. CUSTOMERS ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "02  客户", "流失翻倍，净新增从 +29 掉到 +6",
           "Q3 新增 106 家、流失 55 家；漏斗的两端同时反向运动。")

cd = CategoryChartData()
cd.categories = MONTHS
cd.add_series("新增客户", tuple(NEW))
cd.add_series("流失客户", tuple(CHURN))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(M - 0.12), Inches(2.05),
                        Inches(7.1), Inches(4.3), cd)
chart = gf.chart
style_chart(chart)
chart.has_title = False
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.TOP
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(10)
chart.legend.font.color.rgb = hexc(SLATE)
chart.legend.font.name = FONT
axis_chrome(chart, ymin=0, ymax=48, fmt='0')
plot = chart.plots[0]
plot.gap_width = 70
plot.overlap = -12
for ser, col in zip(plot.series, [BLUE, AMBER]):
    ser.format.fill.solid()
    ser.format.fill.fore_color.rgb = hexc(col)
    ser.format.line.fill.background()
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '0'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(10.5)
dl.font.bold = True
dl.font.color.rgb = hexc(SLATE)
dl.font.name = FONT

X = 8.15
simple(s, X, 2.15, 4.3, 0.25, "失衡程度", 10, SLATE, bold=True)
rows = [("流失 / 新增", "29%  →  80%", AMBER),
        ("净新增（月）", "+29  →  +6", AMBER),
        ("Q3 净增合计", "+51 家", INK)]
yy = 2.5
for lab, val, col in rows:
    simple(s, X, yy, 2.0, 0.25, lab, 10.5, SLATE)
    simple(s, X + 2.0, yy - 0.03, 2.35, 0.3, val, 13, col, bold=True, align=PP_ALIGN.RIGHT)
    rect(s, X, yy + 0.33, 4.35, 0.012, LINE)
    yy += 0.52

callout(s, X, 4.55, 4.35, 1.15,
        [("为什么危险：", {"bold": True, "color": INK}),
         ("9 月每新增 5 家就有 4 家老客户离开，增长几乎全靠「补漏」。", {})],
        size=11)
simple(s, X, 5.95, 4.35, 0.5, "注：因缺少期初客户基数，本期未计算流失率。", 9, MUTED)
footer(s, 4, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "80% 这个比例是全场最有冲击力的数字，务必让 VP 记住。净增 51 家意味着毛增长被流失吃掉了三分之一以上。"
)

# ============================== 5. NPS ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "03  体验", "NPS 掉了 11 分，投诉指向「上手难」",
           "指标与工单两条线在同一时间窗口内同向恶化。")

cd = CategoryChartData()
cd.categories = MONTHS
cd.add_series("NPS", tuple(NPS))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(M - 0.12), Inches(2.05),
                        Inches(7.1), Inches(4.1), cd)
chart = gf.chart
style_chart(chart)
chart.has_title = False
chart.has_legend = False
axis_chrome(chart, ymin=20, ymax=42, fmt='0')
plot = chart.plots[0]
ser = plot.series[0]
ser.format.line.color.rgb = hexc(AMBER)
ser.format.line.width = Pt(2.5)
ser.marker.style = XL_MARKER_STYLE.CIRCLE
ser.marker.size = 9
ser.marker.format.fill.solid()
ser.marker.format.fill.fore_color.rgb = hexc(WHITE)
ser.marker.format.line.color.rgb = hexc(AMBER)
ser.marker.format.line.width = Pt(2.5)
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '0'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.ABOVE
dl.font.size = Pt(12)
dl.font.bold = True
dl.font.color.rgb = hexc(INK)
dl.font.name = FONT
simple(s, M - 0.05, 6.25, 6.9, 0.25, "NPS（净推荐值），范围 −100 ～ 100；纵轴自 20 起。", 8.5, MUTED)

X = 8.15
simple(s, X, 2.15, 4.3, 0.25, "来自一线的信号", 10, SLATE, bold=True)
callout(s, X, 2.5, 4.35, 1.05, [
    ([("「太难上手」", {"bold": True, "size": 13})], {"size": 13}),
    ([("9 月 8 日起，客服工单中该类投诉明显变多。", {})], {"size": 10.5, "before": 6}),
], fill="FBF3EF", accent=AMBER, blocks=True)

simple(s, X, 3.85, 4.35, 0.25, "这意味着", 10, SLATE, bold=True)
tf = textbox(s, X, 4.2, 4.35, 1.5)
para(tf, True, [("NPS 是流失的领先指标。", {"bold": True, "color": INK}),
                ("9 月的体验下滑，大概率会在 Q4 的续费/留存上体现。", {})], 12, INK, line=1.45)
para(tf, False, [("留给我们的窗口是 ", {}), ("一个季度", {"bold": True, "color": AMBER}),
                 ("，不是一个月。", {})], 12, INK, before=8, line=1.45)

callout(s, X, 5.75, 4.35, 0.95,
        [("待验证：", {"bold": True, "color": BLUE}),
         ("NPS 下滑是否集中在新注册 30 天内的用户？需按用户账龄拆分样本。", {})],
        size=10.5)
footer(s, 5, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "工单是定性证据，NPS 是定量证据，两者时间吻合。主动说出「按账龄拆分」这个待验证点，"
    "比硬下结论更可信。"
)

# ============================== 6. DIAGNOSIS ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "04  归因", "时间线高度吻合，但相关性不等于因果",
           "8 月中旬试用期 14 天 → 7 天，之后四个指标依次转向。")

# timeline
ty = 3.02
rect(s, 1.55, ty, 10.05, 0.02, LINE)
nodes = [
    ("8 月中", "试用期由 14 天缩短至 7 天", BLUE),
    ("8 月", "新增首次下滑，流失 12→19", AMBER),
    ("9 月 8 日", "「太难上手」工单明显增多", AMBER),
    ("9 月", "NPS 31→27，流失 19→24", AMBER),
]
xs = [1.9, 4.35, 6.8, 9.25]
for (date, label, col), nx in zip(nodes, xs):
    rect(s, nx - 0.055, ty - 0.045, 0.11, 0.11, col, MSO_SHAPE.OVAL)
    simple(s, nx - 0.45, ty - 0.38, 1.4, 0.24, date, 10.5, col, bold=True, align=PP_ALIGN.CENTER)
    simple(s, nx - 0.62, ty + 0.24, 2.15, 0.7, label, 11, SLATE, line=1.4, align=PP_ALIGN.CENTER)

simple(s, M, 4.35, 5.0, 0.25, "三个待验证假设", 10, SLATE, bold=True)
hyps = [
    ("H1  试用期过短", "用户在感知到价值前就已到期，转化被截断。"),
    ("H2  上手门槛偏高", "新手引导未覆盖关键动作，试用期内完不成「aha」。"),
    ("H3  外部变量", "季节性 / 竞品动作 / 渠道质量，需做同期对比。"),
]
yy = 4.72
for lead, body in hyps:
    tf = textbox(s, M, yy, 7.25, 0.55)
    para(tf, True, [(lead + "　", {"bold": True, "color": INK}), (body, {"color": SLATE})], 11.5, INK, line=1.35)
    yy += 0.6

callout(s, 8.55, 4.55, 3.95, 2.05, [
    ([("下一步：用 2 周做实验，", {"bold": True}), ("\n而不是再用 1 个季度做猜测。", {"bold": True})], {"size": 12}),
    ([("恢复 14 天试用并 A/B 对照，同时给流失客户打原因标签。", {"color": SLATE})],
     {"size": 10.5, "before": 10}),
], blocks=True)
footer(s, 6, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "关键一句话：我说的是「最吻合的变量」，不是「原因」。H3 必须保留，否则会被质疑归因过度。"
    "但无论 H1/H2 哪个成立，行动都是同一个方向——把上手路径修好。"
)

# ============================== 7. PLAN ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "05  下季计划", "Q4 目标：先止跌，再修复",
           "三条并行工作流，全部围绕「让用户更快上手、让流失可见」。")

cols = [
    ("A", "体验与上手", "10 月", BLUE, [
        "试用期恢复 14 天，做 A/B 对照实验",
        "新手引导埋点：3 个关键动作完成率",
        "按用户账龄拆分 NPS 与工单",
    ], "指标：「太难上手」工单 −50%"),
    ("B", "留存与流失", "10–11 月", AMBER, [
        "流失客户 100% 打原因标签",
        "Top 20 高风险客户 1v1 回访",
        "建立续费前 30 天预警名单",
    ], "指标：月度流失回到 ≤15 家"),
    ("C", "增长与数据", "11–12 月", GREEN, [
        "看板补齐 ARPU / 渠道 / 同期对比",
        "新增回到 40+ / 月",
        "以「净新增」而非「新增」考核",
    ], "指标：Q4 收入环比 ≥ 0%"),
]
cw3 = (CW - 2 * 0.28) / 3
for i, (tag, title, when, col, items, metric) in enumerate(cols):
    x = M + i * (cw3 + 0.28)
    rect(s, x, 2.15, cw3, 3.3, PANEL)
    rect(s, x, 2.15, cw3, 0.05, col)
    simple(s, x + 0.28, 2.38, 0.4, 0.25, tag, 11, col, bold=True)
    simple(s, x + 0.62, 2.36, cw3 - 0.9, 0.3, title, 14, INK, bold=True)
    simple(s, x + 0.28, 2.72, cw3 - 0.5, 0.25, when, 9.5, MUTED)
    tf = textbox(s, x + 0.28, 3.08, cw3 - 0.56, 1.9)
    for j, it in enumerate(items):
        para(tf, j == 0, [("· ", {"color": col, "bold": True}), (it, {})], 10.5, SLATE, line=1.4,
             before=0 if j == 0 else 7)
    rect(s, x + 0.28, 4.72, cw3 - 0.56, 0.014, "C9D4DF")
    simple(s, x + 0.28, 4.82, cw3 - 0.56, 0.25, metric, 10, INK, bold=True)

rect(s, M, 5.72, CW, 1.05, INK)
simple(s, M + 0.3, 5.86, 2.2, 0.25, "需要 VP 决策", 9.5, "8FA3BA", bold=True)
asks = "① 批准试用期 A/B 实验（占用 2 周流量）　② onboarding 方向增配 1 名人力　③ 同意 Q4 收入目标按「止跌」而非「增长」设定"
simple(s, M + 0.3, 6.14, CW - 0.6, 0.5, asks, 11.5, WHITE, line=1.4)
footer(s, 7, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "三个 ask 要一个一个提，第 3 个最容易引起争论——提前准备好「为什么止跌就是好结果」的口径："
    "流失不刹住，增长目标只是数字游戏。"
)

# ============================== 8. APPENDIX ==============================
s = prs.slides.add_slide(BLANK)
slide_head(s, "APPENDIX", "数据附录",
           "来源：data/q3-metrics.csv，月度经营看板。")

rows = [("月份", "收入 (USD)", "新增", "流失", "净新增", "NPS")]
for i, m in enumerate(MONTHS):
    rows.append((f"2026-{7+i:02d}  {m}", f"{REV[i]:,}", str(NEW[i]), str(CHURN[i]),
                 f"{NEW[i]-CHURN[i]:+d}", str(NPS[i])))
rows.append(("Q3 合计", f"{sum(REV):,}", str(sum(NEW)), str(sum(CHURN)),
             f"{sum(NEW)-sum(CHURN):+d}", "—"))

tw, th = 8.4, 0.52
gf = s.shapes.add_table(len(rows), 6, Inches(M), Inches(2.1), Inches(tw), Inches(th * len(rows)))
tbl = gf.table
tbl.first_row = True
tbl.horz_banding = False
widths = [2.5, 1.9, 1.0, 1.0, 1.1, 0.9]
for i, wd in enumerate(widths):
    tbl.columns[i].width = Inches(wd)
for r in range(len(rows)):
    tbl.rows[r].height = Inches(th)

for r, row in enumerate(rows):
    for c, val in enumerate(row):
        cell = tbl.cell(r, c)
        cell.margin_left = Inches(0.18)
        cell.margin_right = Inches(0.12)
        cell.margin_top = Inches(0.05)
        cell.margin_bottom = Inches(0.05)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        if r == 0:
            cell.fill.fore_color.rgb = hexc(INK)
        elif r == len(rows) - 1:
            cell.fill.fore_color.rgb = hexc("E8EDF3")
        else:
            cell.fill.fore_color.rgb = hexc(WHITE if r % 2 else PANEL)
        tf = cell.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = val
        run.font.name = FONT
        run.font.size = Pt(11)
        run.font.bold = (r == 0 or r == len(rows) - 1)
        if r == 0:
            run.font.color.rgb = hexc(WHITE)
        elif r == len(rows) - 1:
            run.font.color.rgb = hexc(INK)
        elif c in (3, 4):
            run.font.color.rgb = hexc(AMBER)
        else:
            run.font.color.rgb = hexc(INK)

callout(s, M, 5.52, 8.4, 0.9, [
    ([("读法：", {"bold": True, "color": INK}), ("收入、新增、NPS 连续三个月下行，流失连续三个月上行，", {})], {"size": 11}),
    ([("方向一致且不反复 → 属于结构性问题，需要流程修复，而不是促销式短期拉动。", {"color": SLATE})],
     {"size": 11, "before": 5}),
], blocks=True)

X = 9.75
simple(s, X, 2.15, 3.0, 0.25, "口径说明", 10, SLATE, bold=True)
notes = [
    ("流失率", "缺期初客户基数，本期未计算，Q4 补齐。"),
    ("ARPU / 折扣", "数据未覆盖，收入归因暂不能排除价格因素。"),
    ("试用期变更", "8 月中旬生效，未单独标记，需产品侧确认具体日期。"),
    ("样本口径", "NPS 为月度汇总值，未按用户账龄拆分。"),
]
yy = 2.5
for k, v in notes:
    simple(s, X, yy, 3.3, 0.22, k, 9.5, BLUE, bold=True)
    simple(s, X, yy + 0.22, 3.3, 0.5, v, 9.5, SLATE, line=1.35)
    yy += 0.82
footer(s, 8, TOTAL_SLIDES)
s.notes_slide.notes_text_frame.text = (
    "附录是防守用的。四个口径缺口主动列出来，比被 VP 问出来好。"
)

prs.save("Q3-2026-QBR.pptx")
print("saved")
