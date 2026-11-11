# -*- coding: utf-8 -*-
"""Q3 2026 QBR deck builder."""
import csv
from pptx import Presentation
from pptx.util import Inches as In, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------------- palette ----------------
INK    = RGBColor(0x0F, 0x1B, 0x2D)
NAVY   = RGBColor(0x0E, 0x1B, 0x33)
BODY   = RGBColor(0x4A, 0x55, 0x68)
MUTED  = RGBColor(0x8A, 0x95, 0xA8)
BLUE   = RGBColor(0x2F, 0x6F, 0xED)
RED    = RGBColor(0xD6, 0x45, 0x45)
GREEN  = RGBColor(0x2E, 0x9E, 0x6B)
AMBER  = RGBColor(0xE8, 0xA3, 0x3D)
RULE   = RGBColor(0xE2, 0xE7, 0xF0)
HAIR   = RGBColor(0xEC, 0xEF, 0xF5)
CARD   = RGBColor(0xF7, 0xF9, 0xFC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
SUB    = RGBColor(0xA8, 0xB6, 0xC9)
PALE   = RGBColor(0xD7, 0xDF, 0xEC)

FONT = "Microsoft YaHei"
SW, SH = 13.333, 7.5
ML = 0.85
CW = SW - 2 * ML


def q(s):
    return "\u201c" + s + "\u201d"


# ---------------- data ----------------
rows = list(csv.DictReader(open("data/q3-metrics.csv")))
rev   = [int(r["revenue_usd"]) for r in rows]
new   = [int(r["new_customers"]) for r in rows]
churn = [int(r["churned_customers"]) for r in rows]
nps   = [int(r["nps"]) for r in rows]

REV_Q3   = sum(rev)
EXIT_ARR = rev[-1] * 12
ARR_GAP  = EXIT_ARR - rev[0] * 12
RATE     = rev[2] / rev[1] - 1
PROJ, v = [], rev[-1]
for _ in range(3):
    v *= (1 + RATE)
    PROJ.append(v)
Q4_PROJ  = sum(PROJ)
Q4_DELTA = (Q4_PROJ - REV_Q3) / REV_Q3 * 100
RET_Q3   = Q4_PROJ and sum(churn)  # Q3 churned total

prs = Presentation()
prs.slide_width, prs.slide_height = In(SW), In(SH)
BLANK = prs.slide_layouts[6]


# ---------------- primitives ----------------
def nostyle(sh):
    """Remove theme <p:style> so no inherited shadow / line / fill."""
    sp = sh._element
    st = sp.find(qn("p:style"))
    if st is not None:
        sp.remove(st)
    return sh


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE):
    sh = nostyle(slide.shapes.add_shape(shape, In(x), In(y), In(w), In(h)))
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def line(slide, x, y, w, color=RULE, width=1.0):
    sh = nostyle(slide.shapes.add_connector(1, In(x), In(y), In(x + w), In(y)))
    sh.line.color.rgb = color
    sh.line.width = Pt(width)
    return sh


class T:
    """Tiny text helper: T(slide, x, y, w, h).p([(text, bold, color)], size=...)"""

    def __init__(self, slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
        self.box = slide.shapes.add_textbox(In(x), In(y), In(w), In(h))
        self.tf = self.box.text_frame
        self.tf.word_wrap = wrap
        self.tf.vertical_anchor = anchor
        self.tf.margin_left = self.tf.margin_right = 0
        self.tf.margin_top = self.tf.margin_bottom = 0
        self.n = 0

    def p(self, runs, size=12, color=BODY, line_sp=1.3, before=0, after=0,
          align=PP_ALIGN.LEFT, hang=False, bold=False):
        if isinstance(runs, str):
            runs = [(runs, bold, color)]
        para = self.tf.paragraphs[0] if self.n == 0 else self.tf.add_paragraph()
        self.n += 1
        para.alignment = align
        para.space_before = Pt(before)
        para.space_after = Pt(after)
        para.line_spacing = line_sp
        if hang:
            pPr = para._p.get_or_add_pPr()
            pPr.set("marL", "171450")
            pPr.set("indent", "-171450")
        for item in runs:
            text = item[0]
            b = item[1] if len(item) > 1 else bold
            c = item[2] if len(item) > 2 else (INK if b else color)
            self._run(para, text, size, b, c)
        return para

    @staticmethod
    def _run(para, text, size, bold, color):
        r = para.add_run()
        r.text = text
        f = r.font
        f.name, f.size, f.bold = FONT, Pt(size), bold
        f.color.rgb = color
        rPr = r._r.get_or_add_rPr()
        ea = rPr.find(qn("a:ea"))
        if ea is None:
            ea = rPr.makeelement(qn("a:ea"), {})
            rPr.append(ea)
        ea.set("typeface", FONT)


def header(slide, kicker, title, sub=None):
    T(slide, ML, 0.62, CW, 0.28).p(kicker, 9.5, BLUE, bold=True)
    T(slide, ML, 0.92, CW, 0.62).p(title, 26, INK, bold=True)
    if sub:
        T(slide, ML, 1.58, CW, 0.28).p(sub, 11, BODY)
        line(slide, ML, 2.0, CW)
    else:
        line(slide, ML, 1.64, CW)


def footer(slide, page, source="来源：data/q3-metrics.csv（2026-07 ~ 09）· notes/worklog.md"):
    T(slide, ML, 6.92, CW - 1.0, 0.24).p(source, 8.5, MUTED)
    T(slide, SW - ML - 0.7, 6.92, 0.7, 0.24).p(f"{page:02d}", 9, MUTED,
                                               bold=True, align=PP_ALIGN.RIGHT)


def bullets(slide, x, y, w, items, size=11.5, gap=12, mark_color=BLUE, mark=True):
    t = T(slide, x, y, w, 0.4)
    for i, item in enumerate(items):
        runs = ([(chr(0x25AA) + "  ", True, mark_color)] if mark else []) + item
        t.p(runs, size, line_sp=1.38, before=0 if i == 0 else gap, hang=mark)
    return t


def kicker(slide, x, y, w, text, color=BLUE):
    T(slide, x, y, w, 0.24).p(text, 9.5, color, bold=True)


def draw_table(slide, x, y, fracs, head, data, row_h=0.5, size=12,
               aligns=None, colors=None, bold_col0=True):
    total = sum(fracs)
    xs, acc = [], x
    for f in fracs:
        xs.append(acc)
        acc += f / total * CW
    widths = [f / total * CW for f in fracs]
    aligns = aligns or [PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * (len(fracs) - 1)
    for j, h in enumerate(head):
        T(slide, xs[j], y, widths[j] - 0.12, 0.3).p(h, 9.5, MUTED, align=aligns[j])
    line(slide, x, y + 0.32, CW, RGBColor(0xC9, 0xD2, 0xE0), 1.0)
    for i, rowv in enumerate(data):
        ry = y + 0.4 + i * row_h
        for j, cell in enumerate(rowv):
            col = (colors or {}).get((i, j), INK)
            T(slide, xs[j], ry, widths[j] - 0.12, row_h, anchor=MSO_ANCHOR.MIDDLE).p(
                cell, size, col, bold=(bold_col0 and j == 0), align=aligns[j])
        if i < len(data) - 1:
            line(slide, x, ry + row_h, CW, HAIR, 0.75)
    return y + 0.4 + len(data) * row_h


# =======================================================================
# 01 cover
# =======================================================================
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SW, SH, NAVY)
rect(s, ML, 2.2, 0.85, 0.045, RGBColor(0x4C, 0x7D, 0xF0))

T(s, ML, 2.44, 8.0, 0.28).p("QUARTERLY BUSINESS REVIEW", 10.5,
                            RGBColor(0x7E, 0x8F, 0xA8), bold=True)
T(s, ML - 0.05, 2.8, 9.6, 1.0).p("Q3 2026 业务回顾", 50, WHITE, bold=True)
T(s, ML, 3.94, 9.0, 0.4).p("收入、客户与体验的季度回看，以及 Q4 的止跌方案", 15, SUB)
line(s, ML, 4.72, 5.0, RGBColor(0x2A, 0x3A, 0x55), 1.0)

meta = [("汇报对象", "VP, 业务线"), ("汇报人", "（待填）"), ("数据区间", "2026 年 7—9 月")]
for i, (k, val) in enumerate(meta):
    x = ML + i * 3.0
    T(s, x, 4.94, 2.7, 0.22).p(k, 9, RGBColor(0x6C, 0x7D, 0x96))
    T(s, x, 5.18, 2.7, 0.3).p(val, 12.5, RGBColor(0xE4, 0xEA, 0xF2))
T(s, ML, 6.92, 6.0, 0.24).p("内部资料 · 请勿外传", 8.5, RGBColor(0x5A, 0x6C, 0x88))

# =======================================================================
# 02 executive summary
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "EXECUTIVE SUMMARY", "结论：增长失速与流失加速发生在同一季度")

T(s, ML, 1.82, CW - 0.6, 0.9).p([
    ("本季的问题不在获客前端不够猛，而在", False, BODY),
    ("新客上手环节正在漏人", True, INK),
    ("：收入、新签、NPS 三条曲线同时向下，流失单独向上。", False, BODY),
], 15, line_sp=1.45)

cards = [
    ("收入 · 连续两月下滑", "182K → 171K", "季度内 −6.0%　|　Q3 合计 $529K",
     "9 月退出年化 $2.05M，低于 7 月 $132K。", BLUE),
    ("流失 · 季度内翻倍", "12 → 24", "+100%　|　流失/新签比 29% → 80%",
     "净增客户 29 → 16 → 6，9 月已逼近零增长。", RED),
    ("体验 · NPS 转差", "38 → 27", "−11 分　|　连续两月下滑",
     "9 月 8 日起，投诉集中在" + q("太难上手") + "。", AMBER),
]
cw, gap = 3.69, 0.24
for i, (lab, big, sub, body, color) in enumerate(cards):
    x = ML + i * (cw + gap)
    rect(s, x, 3.0, cw, 2.0, CARD)
    rect(s, x, 3.0, 0.05, 2.0, color)
    T(s, x + 0.32, 3.2, cw - 0.6, 0.24).p(lab, 10, color, bold=True)
    T(s, x + 0.32, 3.46, cw - 0.6, 0.5).p(big, 25, INK, bold=True)
    T(s, x + 0.32, 4.02, cw - 0.55, 0.24).p(sub, 9.5, BODY, bold=True)
    T(s, x + 0.32, 4.36, cw - 0.62, 0.55).p(body, 10.5, BODY, line_sp=1.35)

rect(s, ML, 5.26, CW, 1.3, NAVY)
rect(s, ML, 5.26, 0.05, 1.3, AMBER)
T(s, ML + 0.36, 5.42, CW - 0.7, 0.22).p("核心判断", 9.5, AMBER, bold=True)
T(s, ML + 0.36, 5.66, CW - 0.75, 0.8).p([
    ("三条曲线均在 8 月中旬（试用期由 14 天缩短为 7 天）之后同步转向。本期把它列为", False, PALE),
    ("待验证的主假设", True, WHITE),
    ("，而不是已证结论 —— 验证方法与缺口数据见 P7、P10。", False, PALE),
], 11.5, line_sp=1.4)
footer(s, 2)

# =======================================================================
# 03 metrics overview
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "KEY METRICS", "季度内各项指标全线转差",
       "变化口径为季度内 7 → 9 月；Q2 基线缺失，无法给出环比，详见 P10")

metric_rows = [
    ["收入（USD）", "182K", "176K", "171K", "−6.0%"],
    ["新签客户", "41", "35", "30", "−26.8%"],
    ["流失客户", "12", "19", "24", "+100.0%"],
    ["净增客户", "+29", "+16", "+6", "−79.3%"],
    ["NPS", "38", "31", "27", "−11 分"],
]
colors = {(i, 4): RED for i in range(5)}
colors.update({(2, 2): RED, (2, 3): RED, (2, 1): BODY,
               (3, 2): AMBER, (3, 3): RED,
               (4, 2): AMBER, (4, 3): RED})
end = draw_table(s, ML, 2.28, [2.0, 1.0, 1.0, 1.0, 1.3],
                 ["指标", "7 月", "8 月", "9 月", "季度内变化"],
                 metric_rows, row_h=0.48, size=13, colors=colors)

notes = [
    ("收入", "连续两个月环比下滑（−3.3%、−2.8%），是趋势性变化而不是单月波动。"),
    ("客户", "流失增速（+100%）远快于新签降幅（−26.8%），收入池两端同时收缩。"),
    ("体验", "NPS 两个月累计 −11 分，9 月为季度最低点。"),
]
for i, (k, txt) in enumerate(notes):
    T(s, ML, 5.42 + i * 0.44, CW, 0.3).p(
        [(k + "　", True, BLUE), (txt, False, BODY)], 11, line_sp=1.3)
footer(s, 3)

# =======================================================================
# 04 revenue
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "REVENUE", "收入：连续两月下滑，季度内累计 −6.0%")
s.shapes.add_picture("assets/chart_revenue.png", In(ML - 0.14), In(2.12), width=In(7.32))

kicker(s, 8.6, 2.26, 3.8, "WHAT IT MEANS")
bullets(s, 8.6, 2.58, 3.88, [
    [("月度环比 −3.3%、−2.8%，", True), ("两个月合计 −6.0%；降幅稳定说明趋势仍在延续。", False)],
    [("Q3 合计 $529K", True), ("，月均 $176K，三个月里没有一个月持平或回升。", False)],
    [("9 月退出年化 $2.05M", True), ("，较 7 月的 $2.18M 低 $132K。", False)],
    [("缺 Q2 对比", True), ("：无法判断这是高位回落还是低于全年趋势，这是本页最大的口径缺口。", False)],
], size=11.5, gap=13)
footer(s, 4)

# =======================================================================
# 05 customers
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "CUSTOMER MOMENTUM", "客户：流失翻倍，净增从 29 掉到 6")
s.shapes.add_picture("assets/chart_customers.png", In(ML - 0.14), In(2.12), width=In(7.32))

kicker(s, 8.6, 2.26, 3.8, "WHAT IT MEANS")
bullets(s, 8.6, 2.58, 3.88, [
    [("两端同时恶化", True), ("：新签 41 → 30（−26.8%），流失 12 → 24（+100%）。", False)],
    [("每签 10 个客户，9 月只净留下 2 个", True), (" —— 流失/新签比 29% → 54% → 80%。", False)],
    [("净增 29 → 16 → 6", True), ("，按此斜率 10 月即接近零增长。", False)],
    [("口径限制", True), ("：缺客户基数与 ARPU，无法算流失率% 与 NRR；此处用流失/新签比替代，不可当作标准留存率外推。", False)],
], size=11.5, gap=13)
footer(s, 5)

# =======================================================================
# 06 experience
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "EXPERIENCE", "体验：NPS 两个月 −11 分，投诉指向" + q("上手"))
s.shapes.add_picture("assets/chart_nps.png", In(ML - 0.14), In(2.12), width=In(7.32))

kicker(s, 8.6, 2.26, 3.8, "WHAT IT MEANS")
bullets(s, 8.6, 2.58, 3.88, [
    [("NPS 38 → 31 → 27", True), ("，两个月 −11 分，9 月为季度最低。", False)],
    [("投诉主题高度一致", True), ("：9 月 8 日起 " + q("太难上手") + " 类工单明显变多 —— 指向产品激活，而非价格或功能缺失。", False)],
    [("注意时滞", True), ("：NPS 与流失都是滞后指标，9 月的差评对应的是 8 月入组客户的体验。", False)],
    [("交叉印证", True, AMBER), ("：NPS 下滑的月份（8、9 月）与流失抬升的月份完全重合，定性反馈与定量数据指向同一环节。", False)],
], size=11.5, gap=13)
footer(s, 6)

# =======================================================================
# 07 root-cause hypothesis
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "ROOT CAUSE", "主假设：试用期缩短压缩了" + q("首次价值") + "的窗口",
       "按时间线排列的假设，尚未做因果验证 —— 结论强度取决于 P10 所列数据")

ty = 2.72
line(s, ML, ty, CW, RGBColor(0xD5, 0xDD, 0xEA), 1.5)
events = [
    ("8 / 15", "试用期 14 天 → 7 天", "改动上线（8 月中旬）", BLUE),
    ("9 / 8 起", q("太难上手") + "工单上升", "客服侧定性信号（工作日志）", AMBER),
    ("9 / 24", "流失达 24，季度峰值", "较 7 月的 12 家翻倍", RED),
]
xs = [ML + 0.5, ML + 4.55, ML + 8.6]
for (date, title, sub, color), x in zip(events, xs):
    rect(s, x, ty - 0.075, 0.15, 0.15, color, MSO_SHAPE.OVAL)
    T(s, x, ty - 0.6, 3.0, 0.26).p(date, 11, color, bold=True)
    T(s, x, ty + 0.24, 3.0, 0.3).p(title, 12, INK, bold=True)
    T(s, x, ty + 0.58, 3.0, 0.26).p(sub, 10, MUTED)

hy = 3.9
rect(s, ML, hy, 6.0, 1.95, CARD)
kicker(s, ML + 0.32, hy + 0.2, 5.3, "假设成立的话，应能观察到")
bullets(s, ML + 0.32, hy + 0.56, 5.4, [
    [("时间顺序吻合", True), ("：改期后约 3—4 周出现上手类投诉，随后才是流失高峰。", False)],
    [("投诉主题与假设一致", True), ("：不是价格、不是缺功能，而是太难上手。", False)],
    [("流失增幅 > 新签降幅", True), ("：问题更可能出在接客之后，而不是获客之前。", False)],
], size=11, gap=11)

gx = ML + 6.28
kicker(s, gx, hy + 0.2, 5.2, "但在下结论前必须排除", RED)
bullets(s, gx, hy + 0.56, 5.2, [
    [("渠道质量变化", True), ("：8—9 月是否引入了更高流失率的渠道组合。", False)],
    [("季节性", True), ("：去年 9 月是否同样下滑（需去年数据）。", False)],
    [("价格 / 竞品动作", True), ("：同期是否有调价或竞品事件（工作日志未记录）。", False)],
], size=11, gap=11)

T(s, ML, 6.5, CW, 0.35).p([
    ("验证方式（1 周内）：", True, INK),
    ("按 trial_start_date 分组，对比 7 天组与 14 天组的首周激活率、30 日留存、90 日流失率；若无对照组，改用改期前后入组的准实验对比。",
     False, BODY),
], 10.5, line_sp=1.3)
footer(s, 7)

# =======================================================================
# 08 cost of inaction
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "COST OF INACTION", f"若不干预：Q4 收入量级约 ${Q4_PROJ/1000:.0f}K，较 Q3 再降 {abs(Q4_DELTA):.1f}%",
       "线性外推：假设 9 月 −2.8% 的环比降幅延续。这是量级说明，不是预测，也不作为预算依据")

labels = ["10 月（外推）", "11 月（外推）", "12 月（外推）"]
for i, (lab, val) in enumerate(zip(labels, PROJ)):
    x = ML + i * 3.95
    T(s, x, 2.36, 3.5, 0.24).p(lab, 10, MUTED)
    T(s, x, 2.62, 3.5, 0.55).p(f"${val/1000:.0f}K", 34, INK, bold=True)
    line(s, x, 3.26, 3.5, HAIR, 1.0)

stats = [
    ("Q4 合计（外推）", f"${Q4_PROJ/1000:.0f}K", f"较 Q3 的 $529K 下降 {abs(Q4_DELTA):.1f}%"),
    ("Q4 末退出年化", f"${PROJ[-1]*12/1_000_000:.2f}M", "低于 9 月水平的 $2.05M"),
    ("Q4 流失家数（外推）", "约 70 家", "按 9 月 24 家/月水平延续"),
]
for i, (k, val, sub) in enumerate(stats):
    x = ML + i * 3.95
    T(s, x, 3.62, 3.5, 0.24).p(k, 10, MUTED)
    T(s, x, 3.88, 3.5, 0.42).p(val, 20, RED, bold=True)
    T(s, x, 4.36, 3.6, 0.24).p(sub, 10, BODY)

rect(s, ML, 5.0, CW, 1.55, CARD)
kicker(s, ML + 0.32, 5.16, 6.0, "这个数字意味着什么")
bullets(s, ML + 0.32, 5.48, CW - 0.75, [
    [("不是少赚，是结构性收缩", True), ("：收入下滑主因是客户数在减少，而不是单价或汇率，修复代价高于增长放缓。", False)],
    [("窗口期很短", True), ("：8—9 月入组的客户仍在流失临界期，Q4 前两周是挽回这批客户的可及窗口。", False)],
    [("因此 Q4 目标应按止跌设定", True), ("，而不是在既有增长假设上做叠加。", False)],
], size=11, gap=9)
footer(s, 8, "来源：data/q3-metrics.csv · 外推为简单线性假设，属量级说明，不作为预算依据")

# =======================================================================
# 09 Q4 plan
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "Q4 PLAN", "Q4 行动：先止漏，再修增长",
       "五项动作按 验证 → 修复 → 常态化 排序；具体负责人待本周确认")

acts = [
    ["1　试用策略回调 / 分级", "10 / 10", "10 / 15 上线 A/B", "7 日激活率（建议 ≥ 55%，待对齐）", "增长"],
    ["2　新客首周上手动线（3 步引导 + 人工触达）", "10 / 10", "10 月底全量", "首周 " + q("上手") + " 类工单 −50%", "客户成功"],
    ["3　流失 cohort 归因（按入组日期分层）", "10 / 03", "10 / 10 交付", "产出留存曲线，锁定主因", "数据"],
    ["4　渠道质量复核（各渠道 90 日留存）", "10 / 03", "10 月底", "下线 90 日留存 < 40% 的渠道", "市场"],
    ["5　流失预警看板 + 周会机制", "10 / 13", "10 / 20 上线", "流失信号提前 30 天可见", "数据 / CS"],
]
draw_table(s, ML, 2.16, [4.15, 0.95, 1.35, 4.0, 1.15],
           ["动作", "启动", "截止", "成功指标", "负责"],
           acts, row_h=0.58, size=11,
           aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

rect(s, ML, 5.62, CW, 1.0, CARD)
kicker(s, ML + 0.3, 5.76, 5.0, "如果只做一件事")
T(s, ML + 0.3, 6.0, CW - 0.6, 0.55).p([
    ("做 3 号（cohort 归因）。", True, INK),
    ("在拿到分渠道、按入组日期分层的留存数据之前，1、2 号动作都是在赌方向；它一周内可交付，并决定后面所有投入是否用对地方。",
     False, BODY),
], 11.5, line_sp=1.35)
footer(s, 9, "来源：data/q3-metrics.csv · notes/worklog.md　|　目标值为建议值，需与 VP 对齐后定稿")

# =======================================================================
# 10 asks & gaps
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "ASKS & GAPS", "需要 VP 决策的三件事，以及本期结论的强度边界")

kicker(s, ML, 1.9, 5.5, "需要支持")
bullets(s, ML, 2.22, 5.5, [
    [("1　批准试用期分级实验", True), ("（保留 14 天对照组），10 / 15 前上线；没有对照组，这个实验无法证明因果。", False)],
    [("2　Q4 临时增配 1 名 onboarding 人力", True), ("，仅覆盖 Q4，2 号动线上线后再评估。", False)],
    [("3　同意 Q4 收入目标按止跌设定", True), ("，并把流失率（而非只有新签数）纳入季度考核。", False)],
], size=11.5, gap=15)

kicker(s, ML + 6.2, 1.9, 5.4, "数据缺口（影响结论强度）", RED)
bullets(s, ML + 6.2, 2.22, 5.35, [
    [("无 Q2 基线", True), (" → 只能说季度内在下滑，无法判断是否低于全年趋势。", False)],
    [("无客户基数 / ARPU", True), (" → 算不出流失率% 与 NRR，只能用流失/新签比近似。", False)],
    [("无渠道与 cohort 拆分", True), (" → 根因只能停在假设级，无法排除替代解释。", False)],
    [("无去年 9 月数据", True), (" → 无法排除季节性。", False)],
], size=11.5, gap=13)

rect(s, ML, 5.05, CW, 0.98, NAVY)
T(s, ML + 0.36, 5.2, 6.0, 0.22).p("建议动作", 9.5, AMBER, bold=True)
T(s, ML + 0.36, 5.46, CW - 0.7, 0.6).p([
    ("从 Q4 起固定 QBR 数据包", True, WHITE),
    ("（收入 / 客户数 / 流失率 / NRR / 分渠道 cohort），口径清单见 P11。", False, PALE),
], 11.5, line_sp=1.35)
footer(s, 10)

# =======================================================================
# 11 appendix
# =======================================================================
s = prs.slides.add_slide(BLANK)
header(s, "APPENDIX", "口径、计算方式与素材来源")

kicker(s, ML, 1.9, 5.5, "指标口径")
defs = [
    ("收入", "月度 revenue_usd 合计；季度内变化 =（9 月 − 7 月）/ 7 月。"),
    ("净增客户", "新签 − 流失，是流量口径，不是存量客户数。"),
    ("流失 / 新签比", "流失客户 ÷ 新签客户。非流失率，不能替代 NRR。"),
    ("退出年化", "当月收入 × 12，仅用于量级比较。"),
    ("外推（P8）", "以 9 月环比 −2.8% 逐月连乘，非预测值。"),
]
yy = 2.22
for k, txt in defs:
    T(s, ML, yy, 5.5, 0.24).p(k, 10.5, INK, bold=True)
    T(s, ML, yy + 0.25, 5.5, 0.26).p(txt, 10, BODY)
    yy += 0.68

kicker(s, ML + 6.2, 1.9, 5.4, "数据与素材")
src = [
    ("定量", "data/q3-metrics.csv（2026-07 ~ 09 月度：收入 / 新签 / 流失 / NPS）"),
    ("定性", "notes/worklog.md（试用期改期、9/8 起上手类投诉、QBR 时间）"),
    ("图表", "由上述 CSV 直接生成（matplotlib），未做人工修饰"),
    ("结构", "template.md 的章节（收入 / 客户 / 下季计划）已映射到 P4—P9"),
]
yy = 2.22
for k, txt in src:
    T(s, ML + 6.2, yy, 5.4, 0.24).p(k, 10.5, INK, bold=True)
    T(s, ML + 6.2, yy + 0.25, 5.35, 0.3).p(txt, 10, BODY, line_sp=1.3)
    yy += 0.72

line(s, ML, 5.9, CW, HAIR, 0.75)
T(s, ML, 6.04, CW, 0.5).p(
    "本稿中所有未获证据支持的推断均已显式标注为假设（P7）或外推（P8）；"
    "如需把假设升级为结论，请先补齐 P10 所列四项数据。", 10, MUTED, line_sp=1.35)
footer(s, 11)

prs.save("Q3-2026-QBR.pptx")
print("saved")
