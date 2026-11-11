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
                              XL_MARKER_STYLE, XL_LEGEND_POSITION)
from pptx.oxml.ns import qn

# ---------------------------------------------------------------- palette
INK      = RGBColor(0x0F, 0x21, 0x37)
NAVY2    = RGBColor(0x17, 0x2C, 0x45)
SLATE    = RGBColor(0x5B, 0x6B, 0x7C)
MUTED    = RGBColor(0x8A, 0x98, 0xA6)
LINE     = RGBColor(0xDD, 0xE4, 0xEB)
LIGHT    = RGBColor(0xF2, 0xF5, 0xF8)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT   = RGBColor(0x1F, 0x6F, 0x8B)
ACCENT_L = RGBColor(0x9A, 0xC4, 0xD4)
AMBER    = RGBColor(0xD8, 0x93, 0x2F)
RED      = RGBColor(0xB8, 0x46, 0x3C)
GREEN    = RGBColor(0x2E, 0x7A, 0x5A)
SKY      = RGBColor(0x7F, 0xA6, 0xC9)

FONT = "Microsoft YaHei"
W, H = 13.333, 7.5
ML = 0.78                      # left margin
CW = W - 2 * ML                # content width
TOTAL_SLIDES = 11

# ---------------------------------------------------------------- data
months, revenue, new_c, churn, nps = [], [], [], [], []
with open("data/q3-metrics.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        months.append(row["month"])
        revenue.append(int(row["revenue_usd"]))
        new_c.append(int(row["new_customers"]))
        churn.append(int(row["churned_customers"]))
        nps.append(int(row["nps"]))

labels = [f"{m.split('-')[1]} 月" for m in months]
rev_k = [r / 1000 for r in revenue]
net = [n - c for n, c in zip(new_c, churn)]
rev_total = sum(revenue)
mom = [(revenue[i] - revenue[i - 1]) / revenue[i - 1] * 100 for i in range(1, len(revenue))]

# ---------------------------------------------------------------- helpers
def _font(run, size=None, color=None, bold=None, name=FONT):
    run.font.name = name
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if bold is not None:
        run.font.bold = bold
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", name)


def tf_box(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True, margins=0):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = Inches(margins)
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tf


def par(tf, parts, first=False, size=12, color=INK, bold=False,
        align=PP_ALIGN.LEFT, space_before=0, space_after=0, line=1.25, spc=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if isinstance(parts, str):
        parts = [parts]
    for part in parts:
        if isinstance(part, str):
            spec = {}
            txt = part
        else:
            txt = part[0]
            spec = part[1] if len(part) > 1 else {}
        r = p.add_run()
        r.text = txt
        _font(r, spec.get("size", size), spec.get("color", color),
              spec.get("bold", bold), spec.get("font", FONT))
        if spec.get("spc", spc):
            r._r.get_or_add_rPr().set("spc", str(int(spec.get("spc", spc))))
    return p


def text(slide, x, y, w, h, content, **kw):
    anchor = kw.pop("anchor", MSO_ANCHOR.TOP)
    tf = tf_box(slide, x, y, w, h, anchor=anchor)
    allowed = {k: kw.pop(k) for k in ("size", "color", "bold", "align", "space_before",
                                      "space_after", "line", "spc") if k in kw}
    items = content if isinstance(content, list) else [content]
    for i, item in enumerate(items):
        par(tf, item, first=(i == 0), **allowed)
    return tf


def rect(slide, x, y, w, h, fill=None, line_color=None, shape=MSO_SHAPE.RECTANGLE,
         line_w=0.75, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    style_el = s._element.find(qn("p:style"))
    if style_el is not None:
        s._element.remove(style_el)
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line_color is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_color
        s.line.width = Pt(line_w)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.text_frame.word_wrap = True
    return s


def header(slide, kicker, title, subtitle=None, dark=False):
    c_kick = SKY if dark else ACCENT
    c_title = WHITE if dark else INK
    c_sub = ACCENT_L if dark else SLATE
    text(slide, ML, 0.52, CW, 0.3, kicker, size=10.5, color=c_kick, bold=True, spc=150)
    text(slide, ML, 0.86, CW, 0.55, title, size=25, color=c_title, bold=True, line=1.05)
    if subtitle:
        text(slide, ML, 1.44, CW, 0.3, subtitle, size=11.5, color=c_sub)


def footer(slide, page, label="Q3 2026 QBR · 内部资料"):
    rect(slide, ML, 6.94, CW, 0.012, fill=LINE)
    text(slide, ML, 7.06, CW * 0.7, 0.24, label, size=8.5, color=MUTED)
    text(slide, W - ML - 1.2, 7.06, 1.2, 0.24, f"{page:02d} / {TOTAL_SLIDES}",
         size=8.5, color=MUTED, align=PP_ALIGN.RIGHT)


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def chart_frame(gf):
    chart = gf.chart
    chart.has_title = False
    return chart


def axis_light(chart, cat_size=11):
    try:
        va = chart.value_axis
        va.has_major_gridlines = False
        va.visible = False
        va.format.line.fill.background()
    except Exception:
        pass
    ca = chart.category_axis
    ca.has_major_gridlines = False
    ca.format.line.color.rgb = LINE
    ca.format.line.width = Pt(1)
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.minor_tick_mark = XL_TICK_MARK.NONE
    ca.tick_labels.font.size = Pt(cat_size)
    ca.tick_labels.font.color.rgb = SLATE
    ca.tick_labels.font.name = FONT


def kpi_cell(table_rows, r, c, txt, **style):
    cell = table_rows[r][c]
    cell["text"] = txt
    cell.update(style)


def add_table(slide, x, y, col_w, row_h, rows, sep_after=None):
    sep_after = sep_after if sep_after is not None else range(len(rows) - 1)
    nrows, ncols = len(rows), len(col_w)
    shape = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y),
                                   Inches(sum(col_w)), Inches(sum(row_h)))
    table = shape.table
    table.first_row = False
    table.horz_banding = False
    # strip theme style -> no borders, no banding
    tblPr = table._tbl.tblPr
    for attr in ("firstRow", "bandRow"):
        tblPr.set(attr, "0")
    style_id = tblPr.find(qn("a:tableStyleId"))
    if style_id is None:
        style_id = tblPr.makeelement(qn("a:tableStyleId"), {})
        tblPr.append(style_id)
    style_id.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"
    for i, wd in enumerate(col_w):
        table.columns[i].width = Inches(wd)
    for i, ht in enumerate(row_h):
        table.rows[i].height = Inches(ht)

    for r, row in enumerate(rows):
        for c, spec in enumerate(row):
            cell = table.cell(r, c)
            cell.margin_left = Inches(0.14)
            cell.margin_right = Inches(0.1)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            fill = spec.get("fill")
            if fill is None:
                cell.fill.background()
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = fill
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = spec.get("align", PP_ALIGN.LEFT)
            p.line_spacing = 1.0
            parts = spec["text"] if isinstance(spec["text"], list) else [spec["text"]]
            for part in parts:
                if isinstance(part, str):
                    piece, st = part, {}
                else:
                    piece, st = part[0], part[1]
                run = p.add_run()
                run.text = piece
                _font(run, st.get("size", spec.get("size", 11)),
                      st.get("color", spec.get("color", INK)),
                      st.get("bold", spec.get("bold", False)))
    # separators
    y_cur = y
    for r in range(nrows - 1):
        y_cur += row_h[r]
        if r in sep_after:
            rect(slide, x, y_cur - 0.006, sum(col_w), 0.009, fill=LINE)
    return table


# ---------------------------------------------------------------- deck
prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
prs.core_properties.title = "Q3 2026 业务回顾（QBR）"
prs.core_properties.author = "{{汇报人}}"

# ============================================================ 1. cover
s = blank(prs)
rect(s, 0, 0, W, H, fill=INK)
rect(s, 0, 0, 0.22, H, fill=ACCENT)
text(s, 1.05, 1.62, 8.6, 0.3, "QUARTERLY BUSINESS REVIEW  ·  Q3 2026",
     size=11.5, color=SKY, bold=True, spc=180)
rect(s, 1.05, 2.16, 0.86, 0.05, fill=AMBER)
text(s, 1.05, 2.45, 9.0, 1.1, "Q3 业务回顾", size=54, color=WHITE, bold=True, line=1.0)
text(s, 1.05, 3.72, 9.4, 0.9,
     ["收入下滑、流失抬头、体验转弱", ["本季的三个信号，以及 Q4 的应对方案"]],
     size=17, color=ACCENT_L, line=1.35, space_before=8)

rect(s, 1.05, 5.55, 4.4, 0.012, fill=NAVY2)
text(s, 1.05, 5.8, 4.6, 1.0, [
    [("汇报人：", {"color": MUTED, "size": 11}), ("{{汇报人}}", {"color": WHITE, "size": 11})],
    [("2026 年 10 月  ·  面向 VP 的业务评审", {"color": MUTED, "size": 11})],
], line=1.7)
text(s, 7.6, 5.8, 4.7, 1.0, [
    [("数据口径：2026-07 ~ 2026-09", {"color": MUTED, "size": 10})],
    [("数据来源：月度经营看板 / 客服工单 / NPS 调研", {"color": MUTED, "size": 10})],
], line=1.7)
text(s, 10.2, 1.45, 2.6, 0.9, "Q3", size=72, color=NAVY2, bold=True, align=PP_ALIGN.RIGHT)

# ============================================================ 2. exec summary
s = blank(prs)
header(s, "EXECUTIVE SUMMARY", "执行摘要：增长动能减弱，问题在留存与上手，不在获客",
       "三个判断，一页看完本季经营状况")

cards = [
    ("收入", f"${rev_total/1000:.0f}K", "7→9 月连续两月下滑，累计 -6.0%", RED),
    ("净新增客户", f"{sum(net)}", "7 月 29 → 9 月 6，流失翻倍", RED),
    ("NPS", f"{nps[-1]}", "较 7 月 -11 分，9 月为季度最低", RED),
]
cw_card, gap = 3.78, 0.24
for i, (lab, val, sub, col) in enumerate(cards):
    x = ML + i * (cw_card + gap)
    rect(s, x, 1.9, cw_card, 1.62, fill=LIGHT)
    rect(s, x, 1.9, 0.05, 1.62, fill=col)
    text(s, x + 0.28, 2.06, cw_card - 0.45, 0.24, lab, size=10.5, color=SLATE, bold=True)
    text(s, x + 0.28, 2.34, cw_card - 0.45, 0.55, val, size=30, color=INK, bold=True, line=1.0)
    text(s, x + 0.28, 3.0, cw_card - 0.45, 0.4, sub, size=10, color=SLATE)

findings = [
    ("1", "收入：三个月一路走低",
     "Q3 合计 $529K，9 月 $171K 为季度低点；新增客户数（106）并未塌陷，收入下滑更多来自存量流失。"),
    ("2", "客户：流失增速超过新增",
     "流失 12 → 19 → 24 家，净新增 29 → 16 → 6；9 月流失量已达新增的 80%。"),
    ("3", "体验：NPS 与工单同步恶化",
     "NPS 38 → 31 → 27；9 月 8 日起“太难上手”类工单明显增加，指向 onboarding 而非价格。"),
]
y = 3.78
for num, t, d in findings:
    text(s, ML, y, 0.34, 0.3, num, size=12, color=ACCENT, bold=True)
    text(s, ML + 0.42, y - 0.02, 3.05, 0.3, t, size=12.5, color=INK, bold=True)
    text(s, ML + 3.5, y - 0.02, CW - 3.5, 0.5, d, size=11, color=SLATE, line=1.3)
    y += 0.83

rect(s, ML, 6.32, CW, 0.46, fill=RGBColor(0xF6, 0xEE, 0xE9))
text(s, ML + 0.22, 6.4, CW - 0.4, 0.3,
     [[("结论  ", {"bold": True, "color": RED}),
       ("Q4 的首要动作是修复 onboarding、压住流失；在留存修复前加大获客投入，只会放大漏水。", {"color": INK})]],
     size=11.5)
footer(s, 2)

# ============================================================ 3. KPI table
s = blank(prs)
header(s, "01  KEY METRICS", "Q3 关键指标：每一项都在变差，且下滑在加速",
       "月度经营看板 · 2026-07 至 2026-09")

hdr = ["指标", "7 月", "8 月", "9 月", "Q3 合计 / 期末", "趋势"]
rows = [[{"text": h, "size": 10, "color": SLATE, "bold": True,
          "align": PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER} for i, h in enumerate(hdr)]]

def trend(txt, col):
    return {"text": txt, "size": 10, "color": col, "bold": True, "align": PP_ALIGN.CENTER}

body = [
    ("收入（USD）", f"${revenue[0]/1000:.0f}K", f"${revenue[1]/1000:.0f}K", f"${revenue[2]/1000:.0f}K",
     f"${rev_total/1000:.0f}K", "▼ -6.0%"),
    ("新增客户", str(new_c[0]), str(new_c[1]), str(new_c[2]), str(sum(new_c)), "▼ -27%"),
    ("流失客户", str(churn[0]), str(churn[1]), str(churn[2]), str(sum(churn)), "▲ +100%"),
    ("净新增客户", f"+{net[0]}", f"+{net[1]}", f"+{net[2]}", f"+{sum(net)}", "▼ -79%"),
    ("NPS", str(nps[0]), str(nps[1]), str(nps[2]), f"{nps[-1]}（期末）", "▼ -11 分"),
]
for i, r in enumerate(body):
    hl = i % 2 == 1
    cells = [{"text": r[0], "size": 11.5, "bold": True, "color": INK,
              "fill": LIGHT if hl else None}]
    for v in r[1:5]:
        cells.append({"text": v, "size": 11.5, "color": INK, "align": PP_ALIGN.CENTER,
                      "fill": LIGHT if hl else None})
    col = RED if r[5].startswith("▼") or r[5].startswith("▲") else SLATE
    cells.append({"text": r[5], "size": 10, "color": col, "bold": True,
                  "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None})
    rows.append(cells)

add_table(s, ML, 1.92, [3.1, 1.55, 1.55, 1.55, 2.2, 1.82], [0.42] + [0.56] * 5, rows)

text(s, ML, 5.42, CW, 0.26, "三个必须解释的异常", size=11, color=ACCENT, bold=True, spc=60)
notes = [
    ("流失翻倍", "12 → 24 家", "9 月单月流失已达新增客户的 80%，获客几乎被流失抵消。"),
    ("净新增塌陷", "29 → 6 家", "新增连续两月下降，同时流失上升，双向挤压。"),
    ("NPS 快速下滑", "38 → 27", "口碑与流失同向变化，说明问题集中在新客户早期体验。"),
]
for i, (t, big, d) in enumerate(notes):
    x = ML + i * (CW / 3)
    text(s, x, 5.75, 1.45, 0.28, t, size=10.5, color=INK, bold=True)
    text(s, x + 1.42, 5.72, 1.5, 0.3, big, size=13, color=RED, bold=True)
    text(s, x, 6.08, CW / 3 - 0.4, 0.65, d, size=9.5, color=SLATE, line=1.3)
footer(s, 3)

# ============================================================ 4. revenue
s = blank(prs)
header(s, "02  REVENUE", "收入：连续两个月环比下降，9 月为季度低点",
       "月度确认收入（USD）")

cd = CategoryChartData()
cd.categories = labels
cd.add_series("收入", tuple(rev_k))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(ML - 0.12), Inches(1.86),
                        Inches(7.5), Inches(4.35), cd)
chart = chart_frame(gf)
plot = chart.plots[0]
plot.gap_width = 78
plot.vary_by_categories = False
ser = plot.series[0]
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = ACCENT
ser.format.line.fill.background()
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '0"K"'
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(13)
dl.font.bold = True
dl.font.color.rgb = INK
dl.font.name = FONT
chart.value_axis.maximum_scale = 215
chart.value_axis.minimum_scale = 0
axis_light(chart, 12)

# right panel
px = ML + 7.75
rect(s, px, 1.9, W - ML - px, 4.35, fill=LIGHT)
text(s, px + 0.34, 2.1, 3.4, 0.26, "本季读数", size=10, color=ACCENT, bold=True, spc=80)
stats = [
    ("Q3 合计", f"${rev_total:,.0f}", "月均 $176K"),
    ("9 月环比", f"{mom[-1]:+.1f}%", f"8 月环比 {mom[0]:+.1f}%"),
    ("9 月 vs 7 月", f"{(revenue[-1]-revenue[0])/revenue[0]*100:+.1f}%", "累计减少 $11K"),
]
yy = 2.48
for lab, val, sub in stats:
    text(s, px + 0.34, yy, 1.5, 0.22, lab, size=9.5, color=SLATE)
    text(s, px + 0.34, yy + 0.22, 3.3, 0.4, val, size=22, color=RED if "-" in val else INK, bold=True, line=1.0)
    text(s, px + 0.34, yy + 0.64, 3.3, 0.22, sub, size=9.5, color=MUTED)
    yy += 1.02
text(s, px + 0.34, 5.62, 3.3, 0.5, "收入降幅小于流失增幅，\n差额需用客户级 ARR 解释。",
     size=9, color=SLATE, line=1.35)

text(s, ML, 6.38, CW, 0.42,
     [[("待补数据  ", {"bold": True, "color": AMBER}),
       ("收入下滑的来源拆解需要存量客户明细（降级 / 扩容 / 流失 ARR），当前看板只能提供总数。建议 Q4 前补齐该口径。",
        {"color": SLATE})]],
     size=9.5, line=1.3)
footer(s, 4)

# ============================================================ 5. customers
s = blank(prs)
header(s, "03  CUSTOMERS", "客户：流失增速超过新增，9 月净新增仅 6 家",
       "新增 / 流失客户数（家）与净新增")

cd = CategoryChartData()
cd.categories = labels
cd.add_series("新增客户", tuple(new_c))
cd.add_series("流失客户", tuple(churn))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(ML - 0.12), Inches(1.88),
                        Inches(7.5), Inches(4.3), cd)
chart = chart_frame(gf)
plot = chart.plots[0]
plot.gap_width = 55
plot.overlap = -8
colors = [ACCENT, RED]
for i, sr in enumerate(plot.series):
    sr.format.fill.solid()
    sr.format.fill.fore_color.rgb = colors[i]
    sr.format.line.fill.background()
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = "0"
dl.number_format_is_linked = False
dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(11)
dl.font.bold = True
dl.font.color.rgb = INK
dl.font.name = FONT
chart.value_axis.maximum_scale = 50
chart.value_axis.minimum_scale = 0
axis_light(chart, 12)
chart.has_legend = True
chart.legend.position = XL_LEGEND_POSITION.TOP
chart.legend.include_in_layout = False
chart.legend.font.size = Pt(10.5)
chart.legend.font.color.rgb = SLATE
chart.legend.font.name = FONT

# net adds panel
px = ML + 7.75
pw = W - ML - px
rect(s, px, 1.9, pw, 4.3, fill=LIGHT)
text(s, px + 0.32, 2.08, pw - 0.6, 0.26, "净新增客户", size=10, color=ACCENT, bold=True, spc=80)
bar_max = 2.05
for i, (lab, v) in enumerate(zip(labels, net)):
    yy = 2.5 + i * 0.92
    text(s, px + 0.32, yy, 0.9, 0.26, lab, size=10, color=SLATE)
    wbar = max(bar_max * v / max(net), 0.16)
    rect(s, px + 1.22, yy + 0.03, wbar, 0.2, fill=ACCENT if i == 0 else (SKY if i == 1 else RED))
    text(s, px + 1.3 + wbar, yy - 0.01, 0.8, 0.3, f"+{v}", size=11.5, color=INK, bold=True)
text(s, px + 0.32, 5.32, pw - 0.6, 0.7,
     "净新增三个月累计 +51，\n但 9 月只有 6 家。", size=10, color=SLATE, line=1.35)

text(s, ML, 6.4, CW, 0.42,
     [[("读法  ", {"bold": True, "color": ACCENT}),
       ("新增下降 27%、流失上升 100%，两条曲线在 9 月接近交叉；若趋势延续，Q4 净新增可能转负。",
        {"color": SLATE})]],
     size=9.5, line=1.3)
footer(s, 5)

# ============================================================ 6. NPS
s = blank(prs)
header(s, "04  EXPERIENCE", "体验：NPS 三个月下滑 11 分，9 月跌至 27",
       "月度 NPS（0–100）与客户反馈信号")

cd = CategoryChartData()
cd.categories = labels
cd.add_series("NPS", tuple(nps))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(ML - 0.1), Inches(1.9),
                        Inches(7.35), Inches(4.3), cd)
chart = chart_frame(gf)
plot = chart.plots[0]
sr = plot.series[0]
sr.smooth = False
sr.format.line.color.rgb = ACCENT
sr.format.line.width = Pt(2.5)
sr.marker.style = XL_MARKER_STYLE.CIRCLE
sr.marker.size = 9
sr.marker.format.fill.solid()
sr.marker.format.fill.fore_color.rgb = WHITE
sr.marker.format.line.color.rgb = ACCENT
sr.marker.format.line.width = Pt(2)
plot.has_data_labels = True
dl = plot.data_labels
dl.position = XL_LABEL_POSITION.ABOVE
dl.font.size = Pt(13)
dl.font.bold = True
dl.font.color.rgb = INK
dl.font.name = FONT
chart.value_axis.maximum_scale = 50
chart.value_axis.minimum_scale = 20
chart.has_legend = False
axis_light(chart, 12)

px = ML + 7.6
pw = W - ML - px
rect(s, px, 1.9, pw, 1.9, fill=INK)
text(s, px + 0.3, 2.06, pw - 0.6, 0.24, "9 月流失客户", size=9.5, color=ACCENT_L, bold=True, spc=80)
text(s, px + 0.3, 2.32, pw - 0.6, 0.7, "24 家", size=30, color=WHITE, bold=True, line=1.0)
text(s, px + 0.3, 3.06, pw - 0.6, 0.55, "季度最高，为 7 月的 2 倍；\n同期 NPS 由 38 降至 27。",
     size=9.5, color=ACCENT_L, line=1.35)

quotes = [
    ("9 月 8 日起", "客服工单中“太难上手”类投诉明显增多（工作日志）。"),
    ("8 月中旬", "免费试用由 14 天缩短为 7 天，客户在价值验证前即面临到期。"),
]
yy = 4.0
for t, d in quotes:
    rect(s, px, yy, pw, 1.04, fill=LIGHT)
    rect(s, px, yy, 0.045, 1.04, fill=AMBER)
    text(s, px + 0.24, yy + 0.12, pw - 0.45, 0.22, t, size=9.5, color=AMBER, bold=True)
    text(s, px + 0.24, yy + 0.38, pw - 0.45, 0.6, d, size=9.5, color=INK, line=1.3)
    yy += 1.18

text(s, ML, 6.42, CW, 0.4,
     [[("注意  ", {"bold": True, "color": RED}),
       ("NPS 为月度抽样，样本量较小；结论方向可靠，但具体分值不宜做精确比较。",
        {"color": SLATE})]],
     size=9.5)
footer(s, 6)

# ============================================================ 7. root cause
s = blank(prs)
header(s, "05  DIAGNOSIS", "根因假设：试用期缩短 → 上手失败 → 流失与口碑双降",
       "时间线对齐：体验变化与指标恶化出现在同一窗口")

# timeline
ty = 2.62
rect(s, ML + 0.2, ty, CW - 0.4, 0.02, fill=LINE)
nodes = [
    ("8 月中旬", "试用期 14 天 → 7 天", "价值验证窗口被砍半，新客尚未完成首次成功体验即到期。", AMBER),
    ("8 月", "流失 19 家（+58%）", "流失首次明显抬头，NPS 由 38 降至 31。", RED),
    ("9 月 8 日", "“太难上手”工单激增", "客服工单主题集中爆发，指向 onboarding 而非价格。", AMBER),
    ("9 月", "流失 24 家 · NPS 27", "净新增降至 6 家，季度最差点。", RED),
]
seg = (CW - 0.6) / (len(nodes) - 1)
for i, (date, title_, desc, col) in enumerate(nodes):
    cx = ML + 0.3 + i * seg
    rect(s, cx - 0.075, ty - 0.065, 0.15, 0.15, fill=col, shape=MSO_SHAPE.OVAL)
    bw = 2.52
    bx = cx - bw / 2
    if i == 0:
        bx = ML
    if i == len(nodes) - 1:
        bx = W - ML - bw
    text(s, bx, ty - 0.52, bw, 0.26, date, size=10, color=col, bold=True, align=PP_ALIGN.CENTER)
    text(s, bx, ty + 0.26, bw, 0.3, title_, size=10.5, color=INK, bold=True, align=PP_ALIGN.CENTER, line=1.2)
    text(s, bx, ty + 0.62, bw, 0.85, desc, size=8.8, color=SLATE, align=PP_ALIGN.CENTER, line=1.3)

# causal chain
text(s, ML, 4.24, CW, 0.26, "因果链（假设）", size=10, color=ACCENT, bold=True, spc=80)
chain = ["试用期缩短至 7 天", "新客来不及完成首次价值验证", "上手困难 / 放弃", "流失上升 + NPS 下降"]
cw_chain, gap = 2.62, 0.34
cy = 4.6
for i, c in enumerate(chain):
    x = ML + i * (cw_chain + gap)
    fill = RGBColor(0xE8, 0xEE, 0xF3) if i < 3 else RGBColor(0xF6, 0xE7, 0xE4)
    rect(s, x, cy, cw_chain, 0.78, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    text(s, x + 0.14, cy + 0.11, cw_chain - 0.28, 0.56, c, size=9.6,
         color=INK, bold=(i == 3), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, line=1.25)
    if i < 3:
        text(s, x + cw_chain + 0.02, cy + 0.2, gap - 0.04, 0.35, "›", size=18,
             color=MUTED, bold=True, align=PP_ALIGN.CENTER)

# caveat + validation
rect(s, ML, 5.62, CW, 1.12, fill=LIGHT)
text(s, ML + 0.28, 5.74, 5.4, 0.26, "需要承认的不确定性", size=10, color=SLATE, bold=True, spc=60)
text(s, ML + 0.28, 6.0, 5.5, 0.66,
     "以上为相关性判断，非因果证明；产品复杂度提升、竞品动作、销售结构变化均可能是叠加因素。",
     size=9.3, color=SLATE, line=1.35)
text(s, ML + 6.2, 5.74, 5.2, 0.26, "Q4 如何验证", size=10, color=ACCENT, bold=True, spc=60)
text(s, ML + 6.2, 6.0, 5.2, 0.66,
     "按获客批次 / 试用期长度分群对比转化与 90 天留存；条件允许时做小流量 A/B（14 天 vs 7 天）。",
     size=9.3, color=INK, line=1.35)
footer(s, 7)

# ============================================================ 8. Q4 targets
s = blank(prs)
header(s, "06  Q4 TARGETS", "Q4 目标：先止跌，再修复；净新增回到 30 家/月",
       "建议目标值，待 VP 评审确认")

rows = [[{"text": h, "size": 10, "color": SLATE, "bold": True,
          "align": PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER}
         for i, h in enumerate(["指标", "Q3 实际", "Q4 目标", "变化"])]]
targets = [
    ("季度收入", f"${rev_total/1000:.0f}K", "$540K", "+2.1%"),
    ("月度收入（9 月）", f"${revenue[-1]/1000:.0f}K", "≥ $180K", "+5.3%"),
    ("净新增客户", f"+{sum(net)}", "≥ +90", "约 30 家/月"),
    ("流失客户", f"{sum(churn)}", "≤ 45", "≤ 15 家/月"),
    ("NPS（期末）", f"{nps[-1]}", "≥ 35", "+8 分"),
]
for i, (a, b, c, d) in enumerate(targets):
    hl = i % 2 == 1
    rows.append([
        {"text": a, "size": 11.5, "bold": True, "fill": LIGHT if hl else None},
        {"text": b, "size": 11.5, "align": PP_ALIGN.CENTER, "color": SLATE, "fill": LIGHT if hl else None},
        {"text": c, "size": 11.5, "align": PP_ALIGN.CENTER, "color": GREEN, "bold": True, "fill": LIGHT if hl else None},
        {"text": d, "size": 9.5, "align": PP_ALIGN.CENTER, "color": SLATE, "fill": LIGHT if hl else None},
    ])
add_table(s, ML, 1.92, [3.05, 1.72, 1.72, 1.55], [0.42] + [0.56] * 5, rows)

px = ML + 8.15
pw = W - ML - px
rect(s, px, 1.92, pw, 3.5, fill=LIGHT)
text(s, px + 0.3, 2.08, pw - 0.6, 0.26, "目标怎么来的", size=10, color=ACCENT, bold=True, spc=80)
for i, b in enumerate([
    "收入以 9 月为基数逐月回升，不假设一次性反弹。",
    "净新增 30 家/月：需同时做到流失 ≤15 且新增回到 45+。",
    "NPS 修复优先级高于获客，先修漏再加大投放。",
    "里程碑按月检查；若 10 月未达标，11 月中复盘时同步下调收入预期。",
]):
    text(s, px + 0.3, 2.44 + i * 0.74, pw - 0.6, 0.7,
         [[("· ", {"color": ACCENT, "bold": True}), (b, {})]],
         size=9.5, color=INK, line=1.32)

text(s, ML, 5.62, CW, 0.26, "里程碑", size=10, color=ACCENT, bold=True, spc=80)
ms = [("10 月", "试用期回滚上线\n流失 ≤18"), ("11 月", "onboarding v2 上线\n净新增 ≥20"), ("12 月", "净新增 ≥30\nNPS ≥35")]
for i, (m, d) in enumerate(ms):
    x = ML + i * (CW / 3)
    rect(s, x, 5.94, CW / 3 - 0.28, 0.72, fill=None, line_color=LINE)
    text(s, x + 0.18, 6.0, 1.2, 0.24, m, size=10, color=INK, bold=True)
    text(s, x + 0.18, 6.24, CW / 3 - 0.6, 0.42, d, size=9, color=SLATE, line=1.25)
footer(s, 8)

# ============================================================ 9. action plan
s = blank(prs)
header(s, "07  ACTION PLAN", "Q4 行动计划：五件事，围绕“让新客用起来”",
       "负责人与时间待团队确认后锁定")

rows = [[{"text": h, "size": 9.5, "color": SLATE, "bold": True}
         for h in ["举措", "关键动作", "负责人", "时间", "衡量指标"]]]
actions = [
    ("① 试用期回滚", "恢复 14 天试用；按获客渠道分群对比 7 天/14 天的转化与 90 天留存", "产品 {{TBD}}", "10/15 前", "试用→付费转化率\n首周激活率"),
    ("② Onboarding 重构", "新手 checklist + 行业模板库 + 首周 CSM 主动触达（第 1/3/7 天）", "产品 / 客户成功", "11 月底", "7 日激活率\n上手工单量"),
    ("③ 流失预警", "整合 NPS、工单主题、登录频次，建流失风险分与干预 SOP", "数据 / 客户成功", "11 月", "预警覆盖率\n干预后留存率"),
    ("④ Win-back", "对 Q3 流失 55 家做回访，定位流失原因，推出回归方案", "客户成功", "10–12 月", "赢回 ≥15 家\n挽回 ARR"),
    ("⑤ 体验周报", "工单主题 Top3 + 闭环跟踪，每周同步产品与支持", "客服", "10 月起每周", "主题闭环率\n复发率"),
]
for i, a in enumerate(actions):
    hl = i % 2 == 1
    rows.append([
        {"text": a[0], "size": 9.8, "bold": True, "fill": LIGHT if hl else None},
        {"text": a[1], "size": 9.2, "color": SLATE, "fill": LIGHT if hl else None},
        {"text": a[2], "size": 9.2, "color": SLATE, "fill": LIGHT if hl else None},
        {"text": a[3], "size": 9.2, "color": SLATE, "fill": LIGHT if hl else None},
        {"text": a[4], "size": 9.2, "color": SLATE, "fill": LIGHT if hl else None},
    ])
add_table(s, ML, 1.9, [2.28, 4.94, 1.72, 1.24, 1.98], [0.4] + [0.78] * 5, rows)

text(s, ML, 6.42, CW, 0.4,
     [[("不做 ② 的后果  ", {"bold": True, "color": AMBER}),
       ("仅回滚试用期只能延长窗口，若首次成功体验仍未解决，Q4 流失难以回到 15 家/月以内。",
        {"color": SLATE})]],
     size=9.3)
footer(s, 9)

# ============================================================ 10. asks
s = blank(prs)
header(s, "08  DECISIONS", "需要 VP 拍板的三件事",
       "每一项都直接决定 Q4 目标能否达成")

asks = [
    ("01", "批准试用期回滚至 14 天",
     "影响：所有新客转化路径，需产品 + 市场同步调整话术与页面。",
     "时间：10 月 15 日前上线，才能影响 11 月转化。",
     "不做的代价：新客继续在价值验证前到期，流失难以下降。"),
    ("02", "增配 1 名 Onboarding 专员",
     "影响：首周触达覆盖率由抽样改为全覆盖，直接作用于 7 日激活率。",
     "时间：Q4 内到岗，11 月 onboarding v2 需要人力承接。",
     "不做的代价：方案落地依赖现有 CSM，覆盖率只能维持约 40%。"),
    ("03", "批准 $30K Win-back 预算",
     "影响：覆盖 Q3 流失的 55 家客户回访与回归激励。",
     "时间：10 月启动，按赢回 15 家测算，回收 ARR 约为投入的 4 倍。",
     "不做的代价：流失客户冷却后赢回成本显著上升。"),
]
cw_card, gap = 3.78, 0.24
for i, (num, title_, impact, timing, cost) in enumerate(asks):
    x = ML + i * (cw_card + gap)
    rect(s, x, 1.92, cw_card, 3.66, fill=LIGHT)
    text(s, x + 0.26, 2.08, 0.9, 0.4, num, size=16, color=ACCENT_L, bold=True)
    text(s, x + 0.26, 2.48, cw_card - 0.5, 0.62, title_, size=12.5, color=INK, bold=True, line=1.25)
    text(s, x + 0.26, 3.18, cw_card - 0.5, 0.72, impact, size=9.4, color=SLATE, line=1.4)
    text(s, x + 0.26, 4.02, cw_card - 0.5, 0.75, timing, size=9.4, color=SLATE, line=1.4)
    rect(s, x + 0.26, 4.94, cw_card - 0.52, 0.012, fill=LINE)
    text(s, x + 0.26, 5.04, cw_card - 0.5, 0.46, cost, size=9, color=RED, line=1.35)

rect(s, ML, 5.88, CW, 0.62, fill=INK)
text(s, ML + 0.3, 6.02, CW - 0.6, 0.4,
     [[("风险提示  ", {"bold": True, "color": AMBER}),
       ("若 10 月底流失仍未回到 18 家以内，Q4 收入目标需下调；建议 11 月中做一次中期复盘，按实际数据决定是否调整获客投入。",
        {"color": WHITE})]],
     size=10, line=1.35)
footer(s, 10)

# ============================================================ 11. appendix
s = blank(prs)
header(s, "APPENDIX", "附录：数据明细与口径说明",
       "原始数据见 data/q3-metrics.csv")

rows = [[{"text": h, "size": 10, "color": SLATE, "bold": True,
          "align": PP_ALIGN.LEFT if i == 0 else PP_ALIGN.CENTER}
         for i, h in enumerate(["月份", "收入（USD）", "新增客户", "流失客户", "净新增", "NPS"])]]
for i in range(len(months)):
    hl = i % 2 == 1
    rows.append([
        {"text": months[i], "size": 10.5, "bold": True, "fill": LIGHT if hl else None},
        {"text": f"{revenue[i]:,}", "size": 10.5, "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None},
        {"text": str(new_c[i]), "size": 10.5, "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None},
        {"text": str(churn[i]), "size": 10.5, "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None},
        {"text": f"+{net[i]}", "size": 10.5, "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None},
        {"text": str(nps[i]), "size": 10.5, "align": PP_ALIGN.CENTER, "fill": LIGHT if hl else None},
    ])
rows.append([
    {"text": "Q3 合计 / 期末", "size": 10.5, "bold": True},
    {"text": f"{rev_total:,}", "size": 10.5, "bold": True, "align": PP_ALIGN.CENTER},
    {"text": str(sum(new_c)), "size": 10.5, "bold": True, "align": PP_ALIGN.CENTER},
    {"text": str(sum(churn)), "size": 10.5, "bold": True, "align": PP_ALIGN.CENTER},
    {"text": f"+{sum(net)}", "size": 10.5, "bold": True, "align": PP_ALIGN.CENTER},
    {"text": "—", "size": 10.5, "align": PP_ALIGN.CENTER},
])
add_table(s, ML, 1.92, [2.3, 2.3, 1.9, 1.9, 1.7, 1.5], [0.4] + [0.44] * 4, rows)

text(s, ML, 4.32, 6.2, 0.26, "口径说明", size=10, color=ACCENT, bold=True, spc=80)
text(s, ML, 4.62, 6.4, 1.9, [
    "收入：当月确认收入（USD），不含未生效合同。",
    "流失：当月取消订阅的付费客户数，不含降级客户。",
    "净新增 = 新增客户 − 流失客户。",
    "NPS：月度抽样调研，9 月样本量偏小，分值仅供趋势参考。",
], size=9.3, color=SLATE, line=1.5)

px = 7.55
text(s, px, 4.32, W - ML - px, 0.26, "待补充数据", size=10, color=AMBER, bold=True, spc=80)
text(s, px, 4.62, W - ML - px, 1.9, [
    "存量客户 ARR 与降级/扩容明细（拆解收入下滑来源）",
    "试用期 7 天 / 14 天分群的转化与留存对比",
    "工单主题分类明细（“太难上手”占比与趋势）",
    "流失客户的流失原因打标结果",
], size=9.3, color=SLATE, line=1.5)

text(s, ML, 6.52, CW, 0.34,
     "来源：data/q3-metrics.csv；notes/worklog.md（工单与试用期变更记录）。",
     size=8.5, color=MUTED)
footer(s, 11)


# ---------------------------------------------------------------- speaker notes
NOTES = [
    "开场：本季不是需求端塌陷，而是留存与上手出了问题。先给结论，再用数据支撑，最后要三个决策。\n"
    "提醒听众：所有数字来自月度看板，口径见附录。",

    "三个判断按“收入—客户—体验”顺序讲，每条只给一组数字，避免堆砌。\n"
    "落点是：在留存修复前加大获客投入，等于放大漏水。",

    "先看整体，再看结构。这张表的作用是让 VP 一眼看到“每一项都在变差、且下滑在加速”。\n"
    "若被问到为什么收入只跌 6% 而流失翻倍，回答：客单价与客户结构在部分抵消，需要客户级 ARR 明细验证（见下一页）。",

    "收入连续两月环比下降，9 月是季度低点。\n"
    "强调缺口：目前看板没有存量客户 ARR 明细，无法把收入下滑精确拆到降级/扩容/流失，这是 Q4 要补的口径。",

    "新增从 41 降到 30，流失从 12 升到 24，两条线在 9 月接近交叉。\n"
    "净新增 29→16→6，若趋势延续，Q4 可能出现净流失。",

    "NPS 与工单同步恶化是本次 QBR 最关键的发现：问题集中在早期体验，而不是价格。\n"
    "说明 NPS 为抽样、样本量偏小，所以只看方向，不纠结具体分值。",

    "这一页回答“为什么”。时间线对齐：8 月中改试用期 → 8 月流失抬头 → 9/8 工单激增 → 9 月最差。\n"
    "必须主动说明这是相关性假设、非因果证明，并给出 Q4 的验证方法（分群对比 + 小流量 A/B）。",

    "目标逻辑：先止跌再修复。收入以 9 月为基数回升，净新增 30/月需要流失 ≤15 且新增回到 45+。\n"
    "明确说明这是建议值，等 VP 确认后锁定。",

    "五件事都围绕“让新客用起来”。优先级：① 和 ② 是主攻，③④⑤ 是保障与兜底。\n"
    "负责人与时间待团队确认，会后一天内锁定并公示。",

    "只提三个决策，每个都给出时间与不做的代价，方便 VP 当场拍板。\n"
    "留一个风险出口：10 月底流失未回到 18 家以内，则 11 月中复盘时下调 Q4 收入预期。",

    "附录用于答疑：原始数据、口径定义、以及我们承认还缺哪些数据。\n"
    "如果被追问细节，直接翻到这里，不要在主线上展开。",
]

for slide, note in zip(prs.slides, NOTES):
    slide.notes_slide.notes_text_frame.text = note


out = "Q3-2026-QBR.pptx"
prs.save(out)
print("saved", out)
