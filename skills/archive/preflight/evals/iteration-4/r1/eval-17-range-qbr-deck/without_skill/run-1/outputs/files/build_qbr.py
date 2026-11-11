#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Q3 2026 QBR deck from data/q3-metrics.csv + notes/worklog.md."""

import csv
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_MARK,
                             XL_LEGEND_POSITION)
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- data
rows = list(csv.DictReader(open("data/q3-metrics.csv")))
M = [r["month"][-2:] + "月" for r in rows]
REV = [int(r["revenue_usd"]) for r in rows]
NEW = [int(r["new_customers"]) for r in rows]
CHU = [int(r["churned_customers"]) for r in rows]
NPS = [int(r["nps"]) for r in rows]
NET = [n - c for n, c in zip(NEW, CHU)]
REV_T = sum(REV) / 1000
NEW_T, CHU_T, NET_T = sum(NEW), sum(CHU), sum(NET)
REV_DELTA = (REV[-1] - REV[0]) / REV[0] * 100
CHURN_RATIO = CHU_T / NEW_T * 100

# ---------------------------------------------------------------- style
FONT = "Noto Sans CJK SC"
INK = RGBColor(0x18, 0x20, 0x2E)
MUTED = RGBColor(0x6A, 0x75, 0x85)
FAINT = RGBColor(0x9A, 0xA4, 0xB2)
LINE = RGBColor(0xE2, 0xE6, 0xEC)
PANEL = RGBColor(0xF5, 0xF7, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLUE = RGBColor(0x2B, 0x5C, 0xE0)
RED = RGBColor(0xC4, 0x43, 0x2C)
DARK = RGBColor(0x12, 0x19, 0x27)
AMBER = RGBColor(0xB9, 0x7A, 0x14)

W, H = 13.333, 7.5
L, R = 0.75, 12.583
CW = R - L

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
BLANK = prs.slide_layouts[6]


def _ea(run, name=FONT):
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {})
            rPr.append(e)
        e.set("typeface", name)


def style(run, size, color=INK, bold=False, spacing=None):
    f = run.font
    f.name, f.size, f.bold = FONT, Pt(size), bold
    f.color.rgb = color
    _ea(run)
    if spacing:
        run._r.get_or_add_rPr().set("spc", str(int(spacing * 100)))


def text(slide, x, y, w, h, runs, size=13, color=INK, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.32,
         space_after=0, wrap=True):
    """runs: str | list of str (paragraphs) | list of list-of-(txt, kwargs)"""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_l = tf.margin_r = tf.margin_t = tf.margin_b = 0
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        chunks = [(para, {})] if isinstance(para, str) else para
        for txt, kw in chunks:
            r = p.add_run()
            r.text = txt
            style(r, kw.get("size", size), kw.get("color", color),
                  kw.get("bold", bold), kw.get("spacing", 0))
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, lw=1, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp = s._element
    st = sp.find(qn("p:style"))
    if st is not None:
        sp.remove(st)
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


def head(slide, kicker, title, sub=None):
    text(slide, L, 0.52, CW, 0.24, kicker, 9.5, FAINT, True, spacing=1.0)
    text(slide, L, 0.80, CW, 0.52, title, 25, INK, True, spacing=1.0)
    y = 1.45
    if sub:
        text(slide, L, 1.42, CW, 0.3, sub, 12, MUTED, spacing=1.0)
        y = 1.80
    rect(slide, L, y, CW, 0.012, LINE)
    return y + 0.05


def foot(slide, n):
    text(slide, L, 7.02, 6.0, 0.2, "Q3 2026 QBR · 内部资料", 8.5, FAINT, spacing=1.0)
    text(slide, R - 1.0, 7.02, 1.0, 0.2, f"{n:02d}", 8.5, FAINT,
         align=PP_ALIGN.RIGHT, spacing=1.0)


def chart_font(chart, size=11):
    chart.font.name, chart.font.size = FONT, Pt(size)
    chart.font.color.rgb = MUTED


def clean_chart(chart, valfmt='#,##0', gridlines=True, labels=True):
    chart_font(chart)
    chart.has_legend = False
    va = chart.value_axis
    va.has_major_gridlines = gridlines
    if gridlines:
        va.major_gridlines.format.line.color.rgb = LINE
        va.major_gridlines.format.line.width = Pt(0.75)
    va.format.line.fill.background()
    va.major_tick_mark = XL_TICK_MARK.NONE
    va.minor_tick_mark = XL_TICK_MARK.NONE
    va.tick_labels.font.size = Pt(10)
    va.tick_labels.font.color.rgb = FAINT
    va.tick_labels.number_format = valfmt
    va.tick_labels.number_format_is_linked = False
    ca = chart.category_axis
    ca.format.line.color.rgb = LINE
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.tick_labels.font.size = Pt(11)
    ca.tick_labels.font.color.rgb = MUTED
    return va


# ================================================================ 1 cover
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, DARK)
rect(s, 0, 0, 0.14, H, BLUE)
text(s, 1.15, 1.55, 9.0, 0.3, "QUARTERLY BUSINESS REVIEW", 11,
     RGBColor(0x8E, 0x9A, 0xAD), True, spacing=2.6)
text(s, 1.15, 2.05, 10.0, 1.1, "Q3 2026 业务回顾", 52, WHITE, True, spacing=1.05)
rect(s, 1.18, 3.30, 1.5, 0.035, BLUE)
text(s, 1.15, 3.62, 9.6, 0.9,
     "收入、留存与增长引擎：一个季度里的三个转折点", 18,
     RGBColor(0xD4, 0xDB, 0xE6), spacing=1.4)
text(s, 1.15, 5.55, 5.6, 0.28,
     [[("汇报对象：商务 VP", {}), ("　|　", {"color": RGBColor(0x5C, 0x66, 0x78)}),
       ("2026 年 10 月", {})]], 11, RGBColor(0x9A, 0xA5, 0xB6), spacing=1.0)
text(s, 1.15, 5.95, 5.6, 0.28,
     "数据来源：BI 月度指标导出（2026-07 至 2026-09）", 9.5,
     RGBColor(0x6E, 0x79, 0x8B), spacing=1.0)
text(s, 9.55, 5.5, 2.6, 0.7,
     [[("Q3 汇总", {"size": 9, "color": RGBColor(0x6E, 0x79, 0x8B), "bold": True})],
      [(f"${REV_T:.0f}K 收入　·　{NET_T} 净新增", {"size": 12, "color": RGBColor(0xB9, 0xC2, 0xD0)})]],
     11, align=PP_ALIGN.RIGHT, spacing=1.5)

# ================================================================ 2 exec summary
s = prs.slides.add_slide(BLANK)
top = head(s, "01 / 执行摘要", "增长引擎在下半年失速：收入连续三个月下滑，流失已吃掉一半新增")

items = [
    (f"${REV_T:.0f}K", "季度收入，连续三个月下滑",
     ["182K → 176K → 171K", f"9 月较 7 月 {REV_DELTA:+.1f}%"], RED),
    (f"{NET_T}", "季度净新增，9 月几乎停滞",
     ["月度净新增 29 → 16 → 6", "曲线比季度总数更值得看"], RED),
    (f"{CHURN_RATIO:.0f}%", "流失占同期新增的比例",
     ["55 家流失 / 106 家新增", "逐月加速：12 → 19 → 24"], RED),
    (f"{NPS[0]}→{NPS[-1]}", "NPS 三个月下降 11 点",
     ["与收入、留存同向下滑", "方向一致，构成同一组信号"], AMBER),
]
x, gap = L, 0.26
bw = (CW - gap * 3) / 4
for i, (big, lab, note, col) in enumerate(items):
    bx = x + i * (bw + gap)
    rect(s, bx, 1.95, bw, 1.95, PANEL)
    rect(s, bx, 1.95, bw, 0.045, col)
    text(s, bx + 0.24, 2.14, bw - 0.48, 0.55, big, 30, col, True, spacing=1.0)
    text(s, bx + 0.24, 2.72, bw - 0.42, 0.5, lab, 11.5, INK, True, spacing=1.2)
    text(s, bx + 0.24, 3.22, bw - 0.44, 0.55, note, 9.5, MUTED, spacing=1.32)

rect(s, L, 4.28, CW, 1.62, None, LINE)
rect(s, L, 4.28, 0.05, 1.62, AMBER)
text(s, L + 0.34, 4.50, CW - 0.7, 1.2,
     [[("我们目前的判断（假设，尚未验证）", {"size": 11, "color": AMBER, "bold": True})],
      [("8 月中旬把免费试用从 14 天缩短到 7 天，可能是这一轮流失和 NPS 下滑的共同原因 —— "
        "9 月起客服工单中「太难上手」的投诉明显增多，时间点吻合。",
        {"size": 13.5, "color": INK})],
      [("但这个相关性还没有被队列数据证实。Q4 的第一件事是证实或证伪它，而不是先上动作。",
        {"size": 11, "color": MUTED})]],
     spacing=1.35, space_after=6)

text(s, L, 6.16, CW, 0.3,
     [[("一句话结论：", {"bold": True, "color": INK}),
       ("这不是需求问题，是我们把「新客户活下来」这件事弄坏了。修好留存，收入曲线自然回来。",
        {"color": MUTED})]], 12, spacing=1.0)
foot(s, 2)

# ================================================================ 3 KPI board
s = prs.slides.add_slide(BLANK)
top = head(s, "02 / 季度记分卡", "Q3 全貌：结构性指标全线走弱",
            "口径：月度活跃订阅客户；收入为确认收入（USD）；NPS 为月末滚动值")
tiles = [
    (f"${REV_T:.0f}K", "季度收入", f"{REV_DELTA:+.1f}%", ["9 月 vs 7 月", "无目标值，无法算达成率"], RED),
    (f"{NEW_T}", "新增客户", "41 → 35 → 30", ["环比 -27%", "连续三个月下降"], RED),
    (f"{CHU_T}", "流失客户", "12 → 19 → 24", ["环比 +26%", "季度内翻倍"], RED),
    (f"{NET_T}", "净新增", "29 → 16 → 6", ["9 月接近零增长", "按斜率 10 月转负"], RED),
    (f"{NPS[-1]}", "NPS（9 月末）", f"{NPS[0]} → {NPS[1]} → {NPS[2]}", ["-11 点", "跌破 30"], AMBER),
]
x, gap = L, 0.24
bw = (CW - gap * 4) / 5
for i, (big, lab, delta, note, col) in enumerate(tiles):
    bx = x + i * (bw + gap)
    rect(s, bx, 2.08, bw, 2.30, None, LINE)
    text(s, bx + 0.22, 2.24, bw - 0.44, 0.28, lab, 10.5, MUTED, True, spacing=1.0)
    text(s, bx + 0.22, 2.58, bw - 0.4, 0.62, big, 34, INK, True, spacing=1.0)
    text(s, bx + 0.22, 3.24, bw - 0.4, 0.26, delta, 10, col, True, spacing=1.0)
    text(s, bx + 0.22, 3.56, bw - 0.4, 0.5, note, 9.5, MUTED, spacing=1.3)

rect(s, L, 4.66, CW, 1.32, PANEL)
text(s, L + 0.3, 4.86, 5.4, 0.9,
     [[("读数", {"size": 10, "color": MUTED, "bold": True})],
      [("五个指标同向、同月拐头，说明这不是单点波动，而是同一件事在漏斗不同位置的表现。",
        {"size": 12, "color": INK})]], spacing=1.35, space_after=5)
text(s, 7.0, 4.86, 5.3, 0.9,
     [[("数据缺口", {"size": 10, "color": RED, "bold": True})],
      [("缺少期初客户总数与收入目标，算不出流失率（%）与达成率；两项均需财务 / BI 补数。",
        {"size": 12, "color": INK})]], spacing=1.35, space_after=5)
text(s, L, 6.24, CW, 0.3,
     [[("口径备注：", {"bold": True, "color": MUTED}),
       ("流失按「当期取消订阅」计；NPS 为样本量未披露的月末值，环比方向可信、绝对值仅作参考。",
        {"color": MUTED})]], 10.5, spacing=1.0)
foot(s, 3)

# ================================================================ 4 revenue
s = prs.slides.add_slide(BLANK)
top = head(s, "03 / 收入", "收入连续三个月下滑，9 月为季度最低点",
            "单位：千美元；确认收入口径")
cd = CategoryChartData()
cd.categories = M
cd.add_series("收入", [v / 1000 for v in REV])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(L), Inches(2.28),
                        Inches(7.55), Inches(4.0), cd)
ch = gf.chart
ch.has_title = False
clean_chart(ch, '"$"#,##0"K"')
ch.plots[0].gap_width = 62
ser = ch.plots[0].series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = BLUE
ser.format.line.fill.background()
ch.plots[0].has_data_labels = True
dl = ch.plots[0].data_labels
dl.font.size, dl.font.bold, dl.font.color.rgb = Pt(14), True, INK
dl.number_format, dl.number_format_is_linked = '"$"#,##0"K"', False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
ch.value_axis.maximum_scale, ch.value_axis.minimum_scale = 200, 0

px = 8.62
rect(s, px, 2.28, R - px, 4.0, None, LINE)
text(s, px + 0.3, 2.48, R - px - 0.6, 0.28, "三个月里发生了什么", 10, MUTED, True, spacing=1.0)
notes = [
    ("-6.0%", "9 月对比 7 月，共减少约 $11K"),
    ("-3.3%", "8 月单月环比，跌幅在 9 月继续扩大"),
    ("$171K", "9 月为季度低点，且无回升迹象"),
]
yy = 2.86
for big, t in notes:
    text(s, px + 0.3, yy, 1.5, 0.32, big, 19, INK, True, spacing=1.0)
    text(s, px + 0.3, yy + 0.34, R - px - 0.6, 0.5, t, 10.5, MUTED, spacing=1.25)
    yy += 0.86
text(s, px + 0.3, yy + 0.02, R - px - 0.6, 0.6,
     [[("缺口", {"size": 9.5, "color": RED, "bold": True})],
      [("没有季度收入目标，本页只能看趋势，无法回答「是否达标」。",
        {"size": 10, "color": MUTED})]], spacing=1.25, space_after=3)
text(s, L, 6.44, CW, 0.3,
     [[("解读：", {"bold": True, "color": INK}),
       ("收入下滑幅度小于流失幅度，说明单品客单价或存量扩张在部分抵消流失 —— "
        "这缓冲了短期数字，也掩盖了客户结构的恶化。", {"color": MUTED})]], 11.5, spacing=1.0)
foot(s, 4)

# ================================================================ 5 growth engine
s = prs.slides.add_slide(BLANK)
top = head(s, "04 / 增长引擎", "新增在降、流失在涨，两条曲线正在交叉")
cd = CategoryChartData()
cd.categories = M
cd.add_series("新增", NEW)
cd.add_series("流失", CHU)
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(L), Inches(2.30),
                        Inches(7.3), Inches(3.85), cd)
ch = gf.chart
clean_chart(ch, '0')
ch.plots[0].gap_width = 90
ch.plots[0].overlap = -12
for srs, col in zip(ch.plots[0].series, (BLUE, RED)):
    srs.format.fill.solid()
    srs.format.fill.fore_color.rgb = col
    srs.format.line.fill.background()
ch.has_legend = True
ch.legend.position = XL_LEGEND_POSITION.TOP
ch.legend.include_in_layout = False
ch.legend.font.size, ch.legend.font.color.rgb = Pt(11), MUTED
ch.plots[0].has_data_labels = True
dl = ch.plots[0].data_labels
dl.font.size, dl.font.bold, dl.font.color.rgb = Pt(11), True, INK
dl.number_format, dl.number_format_is_linked = '0', False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
ch.value_axis.maximum_scale = 50
ch.value_axis.minimum_scale = 0
ch.value_axis.major_unit = 10

px = 8.45
text(s, px, 2.32, R - px, 0.28, "净新增（新增 − 流失）", 10, MUTED, True, spacing=1.0)
yy = 2.66
for i in range(3):
    text(s, px, yy, 1.05, 0.28, M[i], 10, FAINT, spacing=1.0)
    text(s, px + 1.05, yy - 0.06, 1.05, 0.36, f"{NET[i]:+d}", 20,
         RED if NET[i] < 20 else INK, True, spacing=1.0)
    # bar
    bw = 2.55 * NET[i] / max(NET)
    rect(s, px + 2.15, yy + 0.03, max(bw, 0.06), 0.2, RED if NET[i] < 20 else BLUE)
    yy += 0.62
rect(s, px, yy + 0.04, R - px, 0.012, LINE)

text(s, px, yy + 0.24, R - px, 0.28, "为什么这一页最重要", 10, MUTED, True, spacing=1.0)
text(s, px, yy + 0.54, R - px, 1.9,
     [[("净新增从 29 掉到 6（-79%），同期新增只跌了 27%。",
        {"color": INK})],
      [("绝大部分恶化来自流失，不是获客。",
        {"color": INK, "bold": True})],
      [("按当前斜率，10 月净新增会转负。",
        {"color": MUTED, "size": 10.5})]],
     11.5, spacing=1.4, space_after=7)
text(s, L, 6.44, CW, 0.3,
     [[("判断：", {"bold": True, "color": INK}),
       ("把预算继续压在获客上，等于往漏桶里倒水。Q4 的重心应放在留存侧的修复与验证。",
        {"color": MUTED})]], 11.5, spacing=1.0)
foot(s, 5)

# ================================================================ 6 signals
s = prs.slides.add_slide(BLANK)
top = head(s, "05 / 客户之声", "时间线指向同一个窗口：8 月中旬的试用期变更")
text(s, L, 2.05, 6.3, 0.3, "我们从日志与工单里看到的信号", 10.5, MUTED, True, spacing=1.0)

ev = [
    ("8 月中旬", "免费试用从 14 天缩短为 7 天", "当季唯一一次影响全量新客的产品变更。", AMBER),
    ("9 月 8 日起", "客服工单中「太难上手」类投诉明显变多", "定性观察，来自客服工单标题；尚未做主题计数与占比统计。", RED),
    ("同期", "流失从 12 升到 24，NPS 从 38 降到 27", "两个指标同月、同向拐头，与工单上升落在同一时间段。", RED),
]
yy = 2.45
for when, what, note, col in ev:
    rect(s, L, yy, 0.035, 1.02, col)
    text(s, L + 0.26, yy + 0.02, 1.35, 0.26, when, 10, col, True, spacing=1.0)
    text(s, L + 1.62, yy + 0.0, 4.5, 0.3, what, 12.5, INK, True, spacing=1.2)
    text(s, L + 1.62, yy + 0.34, 4.55, 0.6, note, 9.5, MUTED, spacing=1.3)
    yy += 1.18

rect(s, 6.95, 2.05, R - 6.95, 3.98, PANEL)
text(s, 7.25, 2.28, R - 7.55, 0.28, "工单主题（非逐字原文）", 10, MUTED, True, spacing=1.0)
text(s, 7.25, 2.66, R - 7.55, 1.3,
     [[("「太难上手」", {"size": 30, "color": INK, "bold": True})],
      [("9 月工单中反复出现的主题标签", {"size": 10, "color": MUTED})]],
     spacing=1.2, space_after=4)
rect(s, 7.25, 4.14, R - 7.85, 0.012, LINE)
text(s, 7.25, 4.42, R - 7.6, 1.6,
     [[("注意证据强度", {"size": 10, "color": AMBER, "bold": True})],
      [("以上是三条弱证据的叠加：一次产品变更、一类工单主题、两个指标的方向。",
        {"size": 10.5, "color": INK})],
      [("它们足以支持「去验证」，但不足以支持「已定论」。本页不做因果宣称。",
        {"size": 10.5, "color": MUTED})]],
     spacing=1.35, space_after=6)
text(s, L, 6.44, CW, 0.3,
     [[("我们还不知道的：", {"bold": True, "color": INK}),
       ("7 天试用用户的 30/60 天留存 vs 14 天用户 —— 这个对比能一次性决定上面这条假设成立与否。",
        {"color": MUTED})]], 11.5, spacing=1.0)
foot(s, 6)

# ================================================================ 7 diagnosis
s = prs.slides.add_slide(BLANK)
top = head(s, "06 / 归因", "假设：上手时间被砍掉一半，价值还没被感知就流失了",
            "这是当前最简洁、也最可被证伪的解释")

chain = [("试用期\n14 → 7 天", "可用上手时间减半", BLUE),
         ("上手流程\n跑不完", "多数用户只完成前 2 步", BLUE),
         ("价值未感知", "「太难上手」成为主要抱怨", AMBER),
         ("早期流失\nNPS 下降", "流失 12→19→24，NPS 38→27", RED)]
bwid, bgap = 2.72, 0.36
for i, (t, d, col) in enumerate(chain):
    bx = L + i * (bwid + bgap)
    rect(s, bx, 2.18, bwid, 1.28, None, LINE)
    rect(s, bx, 2.18, bwid, 0.04, col)
    text(s, bx + 0.2, 2.36, bwid - 0.4, 0.68,
         [[(ln, {"size": 12.5, "color": INK, "bold": True})] for ln in t.split("\n")],
         spacing=1.25, space_after=1)
    text(s, bx + 0.2, 3.10, bwid - 0.4, 0.3, d, 9.5, MUTED, spacing=1.2)
    if i < 3:
        text(s, bx + bwid + 0.06, 2.66, 0.3, 0.3, "→", 15, FAINT, spacing=1.0)

text(s, L, 3.72, 6.2, 0.28, "怎么证实或证伪（Q4 第 1–2 周即可完成）", 10.5, MUTED, True, spacing=1.0)
tests = [
    ("队列对比", "7 天 vs 14 天注册队列的 30/60 天留存与首次价值达成时间"),
    ("工单量化", "把「太难上手」主题做成计数，看它占流失客户工单的比例"),
    ("流失访谈", "抽 10 家 8–9 月流失客户，问「卡在哪一步」"),
]
yy = 4.08
for name, d in tests:
    text(s, L, yy, 1.5, 0.26, name, 10.5, BLUE, True, spacing=1.0)
    text(s, L + 1.55, yy, 4.6, 0.5, d, 10.5, INK, spacing=1.3)
    yy += 0.62

rect(s, 7.0, 3.72, R - 7.0, 2.28, PANEL)
text(s, 7.28, 3.92, R - 7.56, 0.28, "如果假设成立", 10, MUTED, True, spacing=1.0)
text(s, 7.28, 4.24, R - 7.56, 1.65,
     [[("恢复 14 天试用 + 上手引导，应能在 4–6 周内看到早期流失回落，",
        {"size": 11, "color": INK})],
      [("这是低成本、可逆的一步，不需要等完整论证。",
        {"size": 11, "color": INK, "bold": True})],
      [("如果假设不成立，说明问题在定价或交付质量 —— 那会是另一个量级的投入，"
        "需要在下一次评审前重新排优先级。",
        {"size": 10, "color": MUTED})]],
     spacing=1.35, space_after=6)
text(s, L, 6.44, CW, 0.3,
     [[("所以先做的是：", {"bold": True, "color": INK}),
       ("两周内出归因结论；在此之前不承诺预算，也不对外宣布「问题已解决」。",
        {"color": MUTED})]], 11.5, spacing=1.0)
foot(s, 7)

# ================================================================ 8 plan
s = prs.slides.add_slide(BLANK)
top = head(s, "07 / Q4 计划", "五件事，按「先验证、再修复、后扩张」排序",
            "目标是止住净新增下滑：10 月回正，12 月恢复增长")
data = [
    ("P0", "试用期回滚 14 天 + A/B 对照", "产品增长", "早期流失率", "10 月中"),
    ("P0", "队列归因分析，出结论", "BI / 增长", "结论文档", "10 月第 2 周"),
    ("P1", "上手流程改造（引导 + 检查清单）", "产品", "首次价值达成时间", "11 月底"),
    ("P1", "流失预警与主动成功干预", "客户成功", "月流失 ≤ 15", "持续"),
    ("P2", "存量客户扩张（升级 / 增购）", "销售", "净收入留存率", "12 月底"),
]
cols = [0.85, 5.30, 1.85, 2.55, 1.28]
hdr = ["优先级", "行动", "负责人", "衡量指标", "截止"]
tw = sum(cols)
tbl_shape = s.shapes.add_table(len(data) + 1, 5, Inches(L), Inches(2.20),
                               Inches(tw), Inches(0.36 + 0.44 * len(data)))
tbl = tbl_shape.table
for i, cwid in enumerate(cols):
    tbl.columns[i].width = Inches(cwid)
tbl.rows[0].height = Inches(0.36)
for r in range(1, len(data) + 1):
    tbl.rows[r].height = Inches(0.44)


def cell(r, c, txt, size=11, bold=False, color=INK, align=PP_ALIGN.LEFT):
    cl = tbl.cell(r, c)
    cl.margin_left, cl.margin_right = Inches(0.14), Inches(0.08)
    cl.margin_top, cl.margin_bottom = Inches(0.05), Inches(0.05)
    cl.vertical_anchor = MSO_ANCHOR.MIDDLE
    cl.fill.solid()
    cl.fill.fore_color.rgb = PANEL if r == 0 else (WHITE if r % 2 else RGBColor(0xFA, 0xFB, 0xFD))
    tf = cl.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = 1.15
    run = p.add_run()
    run.text = txt
    style(run, size, color, bold)
    # borders
    tcPr = cl._tc.get_or_add_tcPr()
    for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = tcPr.makeelement(qn(tag), {"w": "6350", "cap": "flat"})
        fill = ln.makeelement(qn("a:solidFill"), {})
        clr = fill.makeelement(qn("a:srgbClr"), {"val": "E2E6EC"})
        fill.append(clr)
        ln.append(fill)
        tcPr.insert(i, ln)


for i, h in enumerate(hdr):
    cell(0, i, h, 10, True, MUTED)
for r, row in enumerate(data, start=1):
    col = RED if row[0] == "P0" else (AMBER if row[0] == "P1" else FAINT)
    cell(r, 0, row[0], 10.5, True, col)
    cell(r, 1, row[1], 11, r <= 2)
    cell(r, 2, row[2], 10.5, False, MUTED)
    cell(r, 3, row[3], 10.5, False, MUTED)
    cell(r, 4, row[4], 10.5, False, MUTED)

rect(s, L, 5.16, CW, 1.14, None, LINE)
rect(s, L, 5.16, 0.05, 1.14, BLUE)
text(s, L + 0.34, 5.36, 5.55, 0.8,
     [[("建议目标（待与 VP 对齐）", {"size": 10, "color": MUTED, "bold": True})],
      [("10 月净新增 ≥ 20；11 月起月流失 ≤ 15；12 月 NPS 回到 31 以上。",
        {"size": 11.5, "color": INK})]], spacing=1.35, space_after=5)
text(s, 7.18, 5.36, R - 7.18, 0.8,
     [[("关于负责人", {"size": 10, "color": RED, "bold": True})],
      [("以上为建议承接方，需在评审会上确认到人；没有名字的计划不会发生。",
        {"size": 11.5, "color": INK})]], spacing=1.35, space_after=5)
text(s, L, 6.6, CW, 0.3,
     [[("排序理由：", {"bold": True, "color": INK}),
       ("P0 是验证与止血，两周内出结论；P1 是修复，需要产品排期；P2 只有在前两项见效后才值得投预算。",
        {"color": MUTED})]], 11, spacing=1.0)
foot(s, 8)

# ================================================================ 9 asks
s = prs.slides.add_slide(BLANK)
top = head(s, "08 / 需要的支持", "三个决策，和三个我们已经预判的风险")
text(s, L, 2.05, 5.6, 0.28, "请在会上决定", 10.5, MUTED, True, spacing=1.0)
asks = [
    ("01", "同意试用期回滚 14 天", "低成本、可逆，10 月中上线；不占用额外预算。"),
    ("02", "给 P1 排一个产品 sprint", "上手引导改造需要产品资源，否则 11 月底的节点守不住。"),
    ("03", "确认 Q4 目标是「净新增回正」", "而非「收入达标」—— 先修漏斗，再谈规模。"),
]
yy = 2.42
for num, t, d in asks:
    text(s, L, yy, 0.5, 0.3, num, 12, BLUE, True, spacing=1.0)
    text(s, L + 0.55, yy - 0.02, 4.9, 0.3, t, 13, INK, True, spacing=1.15)
    text(s, L + 0.55, yy + 0.32, 4.95, 0.6, d, 10.5, MUTED, spacing=1.3)
    yy += 1.02

text(s, 6.55, 2.05, R - 6.55, 0.28, "风险与缓解", 10.5, MUTED, True, spacing=1.0)
risks = [
    ("回滚试用期会拉低当期新增数", "预计短期新增 -10% 左右；用净新增而非新增数考核，避免被单指标带偏。"),
    ("归因结论 10 月出不来", "先做回滚（低风险），同时并行访谈；两者不互斥。"),
    ("修留存见效慢，Q4 收不回来", "同步启动 P2 存量扩张，守住 Q4 收入下限。"),
]
yy = 2.42
for t, d in risks:
    rect(s, 6.55, yy, R - 6.55, 0.98, PANEL)
    text(s, 6.78, yy + 0.13, R - 6.98, 0.28, t, 11, INK, True, spacing=1.15)
    text(s, 6.78, yy + 0.45, R - 6.98, 0.45, d, 9.5, MUTED, spacing=1.25)
    yy += 1.13
text(s, L, 6.5, CW, 0.3,
     [[("如果只记一件事：", {"bold": True, "color": INK}),
       ("Q3 的核心损失不是收入，是「新客户活不过第一个月」这件事被我们忽略了三个月。",
        {"color": MUTED})]], 11.5, spacing=1.0)
foot(s, 9)

# ================================================================ 10 appendix
s = prs.slides.add_slide(BLANK)
top = head(s, "附录", "数据口径与已知局限")
left = [
    ("数据来源", "BI 月度指标导出 q3-metrics.csv，覆盖 2026-07 / 08 / 09 三个月；"
                 "定性信息来自团队工作日志与客服工单。"),
    ("指标定义", "收入＝当月确认收入（USD）；新增＝当月首次付费客户数；流失＝当月取消订阅客户数；"
                 "净新增＝新增 − 流失；NPS＝月末滚动值。"),
    ("缺失项", "① 期初客户总数（无法计算流失率 %）；② 季度收入目标（无法计算达成率）；"
               "③ NPS 样本量；④ 试用队列的留存分层数据。"),
]
yy = 2.1
for t, d in left:
    text(s, L, yy, 5.4, 0.26, t, 10, MUTED, True, spacing=1.0)
    text(s, L, yy + 0.28, 5.45, 1.2, d, 10.5, INK, spacing=1.4)
    yy += 1.42

right = [
    ("不要把相关性当因果", "8 月试用期变更与流失上升时间吻合，但同期也可能有定价、竞品、季节性因素。"
                           "证据强度：中等偏弱。"),
    ("绝对值谨慎引用", "NPS 27 的绝对值受样本与调研方式影响，建议只引用其环比方向。"),
    ("下季度需要补的三件事", "给每个指标配目标值；把流失按队列拆分；给工单打可统计的主题标签。"),
]
yy = 2.1
for t, d in right:
    rect(s, 6.9, yy - 0.04, R - 6.9, 1.18, PANEL)
    text(s, 7.14, yy + 0.12, R - 7.36, 0.26, t, 10.5, INK, True, spacing=1.0)
    text(s, 7.14, yy + 0.44, R - 7.36, 0.7, d, 10, MUTED, spacing=1.35)
    yy += 1.34
foot(s, 10)

NOTES = [
    "开场：Q3 不是收入问题，是留存问题。先给结论，再走证据。",
    "三条同时发生：收入下滑、净新增接近零、流失超过新增一半。停在这一页问一句："
    "我们是不是把增长当成获客的同义词了。",
    "五个指标同月同向拐头——这是同一个原因在不同位置的投影。"
    "如果有人问流失率，如实说缺期初客户数，算不出来，不要现场估。",
    "收入只跌 6%，但流失翻了倍——差额靠客单价和存量扩张撑着。这层缓冲会掩盖结构恶化，值得提醒。",
    "本页是全场最重要的：净新增跌幅（-79%）远大于新增跌幅（-27%），"
    "所以止血点在留存侧，不在投放侧。",
    "三条弱证据叠加。注意措辞：说『时间吻合』，不说『因为』。"
    "如果 VP 追问因果，直接说『还没验证，10 月出结论』。",
    "把假设摊开，同时给证伪路径——这样即使结论被推翻，团队的公信力不受损。",
    "排序逻辑要讲清楚：P0 是两周内能出结论、可逆的动作；P2 是等前两项见效才投的预算。"
    "负责人一栏是建议，会上必须落到人。",
    "三个 ask 尽量在会上拿到明确答复，尤其是 03（考核口径）。",
    "附录留给追问：口径、缺失项、下一步要补的数据。",
]
for sl, note in zip(prs.slides, NOTES):
    sl.notes_slide.notes_text_frame.text = note

prs.save("Q3-2026-QBR.pptx")
print("saved Q3-2026-QBR.pptx ·", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
