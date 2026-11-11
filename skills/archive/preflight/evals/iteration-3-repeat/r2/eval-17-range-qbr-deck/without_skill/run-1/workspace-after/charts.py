# -*- coding: utf-8 -*-
"""生成 QBR 所需图表（PNG，透明背景，配色与 PPT 一致）"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
matplotlib.rcParams["axes.unicode_minus"] = False

INK    = "#10233A"
MUTED  = "#6B7C8F"
GRID   = "#E3E8EE"
ACCENT = "#2E6F95"
RED    = "#C0453F"
GREEN  = "#4C8C6B"
GOLD   = "#C99A2E"

ROWS = list(csv.DictReader(open("data/q3-metrics.csv", encoding="utf-8")))
MONTHS = [f"{int(r['month'][5:7])}月" for r in ROWS]
REV    = [int(r["revenue_usd"]) for r in ROWS]
NEW    = [int(r["new_customers"]) for r in ROWS]
CHURN  = [int(r["churned_customers"]) for r in ROWS]
NPS    = [int(r["nps"]) for r in ROWS]


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
        ax.spines[s].set_linewidth(1.2)
    ax.tick_params(colors=MUTED, labelsize=12, length=0)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.xaxis.grid(False)


def save(fig, name):
    fig.savefig(name, dpi=220, transparent=True, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    print("saved", name)


# ---------- 图1：月度收入 ----------
fig, ax = plt.subplots(figsize=(7.2, 3.5))
bars = ax.bar(MONTHS, REV, width=0.46, color=ACCENT, zorder=3)
bars[-1].set_color(RED)
for b, v in zip(bars, REV):
    ax.text(b.get_x() + b.get_width() / 2, v + 5000, f"${v/1000:.1f}k",
            ha="center", va="bottom", fontsize=13, color=INK, fontweight="bold")
mom = ["", "环比 -3.3%", "环比 -2.8%"]
for i, t in enumerate(mom):
    if t:
        ax.text(i, REV[i] + 20000, t, ha="center", va="bottom", fontsize=11.5, color=RED)
style(ax)
ax.set_ylim(0, 232000)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f"{x/1000:.0f}k"))
save(fig, "chart_revenue.png")

# ---------- 图2：新增 vs 流失 ----------
fig, ax = plt.subplots(figsize=(7.2, 3.5))
w = 0.34
x = range(len(MONTHS))
b1 = ax.bar([i - w/2 - 0.02 for i in x], NEW, width=w, color=ACCENT, label="新增客户", zorder=3)
b2 = ax.bar([i + w/2 + 0.02 for i in x], CHURN, width=w, color=RED, label="流失客户", zorder=3)
for bs in (b1, b2):
    for b in bs:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.8, int(b.get_height()),
                ha="center", va="bottom", fontsize=12.5, color=INK, fontweight="bold")
net = [n - c for n, c in zip(NEW, CHURN)]
for i, n in enumerate(net):
    ax.text(i, 47, f"净增 +{n}", ha="center", va="bottom", fontsize=11.5, color=MUTED)
style(ax)
ax.set_xticks(list(x))
ax.set_xticklabels(MONTHS)
ax.set_ylim(0, 56)
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.13),
          fontsize=12, labelcolor=INK, ncol=2, handlelength=1.2)
save(fig, "chart_customers.png")

# ---------- 图3：NPS ----------
fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.plot(MONTHS, NPS, color=ACCENT, linewidth=3, marker="o", markersize=9,
        markerfacecolor="white", markeredgewidth=2.5, zorder=3)
for i, v in enumerate(NPS):
    dx = -0.16 if i == len(NPS) - 1 else 0
    ax.text(i + dx, v + 2.0, str(v), ha="right" if dx else "center", va="bottom",
            fontsize=13, color=RED if i == len(NPS) - 1 else INK, fontweight="bold")
ax.axhspan(0, 30, color=RED, alpha=0.06, zorder=1)
ax.text(-0.32, 30.7, "预警线 30", fontsize=11, color=RED, ha="left", va="bottom")
style(ax)
ax.set_ylim(20, 46)
ax.set_xlim(-0.35, 2.45)
save(fig, "chart_nps.png")
