import csv, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

INK   = "#0F1B2D"
BODY  = "#4A5568"
MUTED = "#98A2B3"
BLUE  = "#2F6FED"
RED   = "#D64545"
GREEN = "#2E9E6B"
AMBER = "#E8A33D"
RULE  = "#E2E7F0"

plt.rcParams.update({
    "font.family": "Noto Sans CJK SC",
    "font.size": 11,
    "axes.edgecolor": RULE,
    "axes.labelcolor": BODY,
    "text.color": INK,
    "xtick.color": BODY,
    "ytick.color": MUTED,
    "axes.grid": False,
    "figure.dpi": 200,
})

rows = list(csv.DictReader(open("data/q3-metrics.csv")))
months = ["7月", "8月", "9月"]
rev  = [int(r["revenue_usd"]) for r in rows]
new  = [int(r["new_customers"]) for r in rows]
churn= [int(r["churned_customers"]) for r in rows]
nps  = [int(r["nps"]) for r in rows]


def clean(ax, keep_left=False, keep_bottom=True):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(keep_left)
    ax.spines["bottom"].set_visible(keep_bottom)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(length=0)


# ---------- 1. revenue ----------
fig, ax = plt.subplots(figsize=(7.1, 3.82))
ax.plot(months, rev, color=BLUE, lw=2.6, marker="o", ms=9, mfc="white",
        mew=2.6, zorder=3, clip_on=False)
ax.fill_between(months, rev, min(rev) - 14000, color=BLUE, alpha=0.08, zorder=1)
ax.plot([months[-1]], [rev[-1]], "o", ms=11, mfc=BLUE, mec=BLUE, zorder=4)

for i, v in enumerate(rev):
    ax.annotate(f"{v/1000:.0f}K", (i, v), textcoords="offset points",
                xytext=(0, 16), ha="center", fontsize=13, fontweight="bold", color=INK)
for i in (1, 2):
    pct = (rev[i] - rev[i-1]) / rev[i-1] * 100
    ax.annotate(f"{pct:+.1f}%", ((i-1+ i)/2, (rev[i]+rev[i-1])/2), textcoords="offset points",
                xytext=(0, -18), ha="center", fontsize=10.5, color=RED, fontweight="bold")

ax.set_ylim(min(rev) - 13000, max(rev) + 11000)
ax.set_xlim(-0.28, 2.28)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v/1000:.0f}K"))
ax.set_yticks([170000, 175000, 180000, 185000])
ax.grid(axis="y", color=RULE, lw=1)
ax.set_axisbelow(True)
clean(ax)
ax.tick_params(axis="x", labelsize=12, pad=6)
ax.set_xlabel("")
fig.tight_layout(pad=0.4)
fig.savefig("assets/chart_revenue.png", transparent=True)
plt.close(fig)

# ---------- 2. new vs churn ----------
fig, ax = plt.subplots(figsize=(7.1, 3.82))
w = 0.30
xs = range(3)
b1 = ax.bar([x - w/2 - 0.02 for x in xs], new, w, color=BLUE, zorder=3)
b2 = ax.bar([x + w/2 + 0.02 for x in xs], churn, w, color=RED, alpha=0.92, zorder=3)
for b in list(b1) + list(b2):
    h = b.get_height()
    ax.annotate(f"{h}", (b.get_x() + b.get_width()/2, h), textcoords="offset points",
                xytext=(0, 4), ha="center", fontsize=12, fontweight="bold", color=INK)
# in-bar labels on first group
ax.annotate("新签", (-w/2 - 0.02, 3.2), ha="center", fontsize=10, color="white", fontweight="bold")
ax.annotate("流失", (w/2 + 0.02, 3.2), ha="center", fontsize=10, color="white", fontweight="bold")
# net adds on top
net_cols = [GREEN, AMBER, RED]
for i in xs:
    net = new[i] - churn[i]
    ax.annotate(f"net  +{net}" if False else f"净增 +{net}", (i, 47.5), ha="center",
                fontsize=11.5, color=net_cols[i], fontweight="bold")
ax.axhline(0, color=RULE, lw=1)
ax.set_ylim(0, 51)
ax.set_xticks(list(xs))
ax.set_xticklabels(months, fontsize=12)
ax.tick_params(axis="x", pad=8)
ax.set_yticks([0, 10, 20, 30, 40])
clean(ax)
fig.tight_layout(pad=0.4)
fig.savefig("assets/chart_customers.png", transparent=True)
plt.close(fig)

# ---------- 3. nps ----------
fig, ax = plt.subplots(figsize=(7.1, 3.82))
cols = [BLUE, "#6E8FCB", RED]
bars = ax.bar(months, nps, 0.42, color=cols, zorder=3)
for b, v in zip(bars, nps):
    ax.annotate(f"{v}", (b.get_x() + b.get_width()/2, v), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=14, fontweight="bold", color=INK)
for x, d in ((0.5, "−7 pts"), (1.5, "−4 pts")):
    ax.annotate(d, (x, 45.5), ha="center", fontsize=11.5, color=RED, fontweight="bold")
ax.set_ylim(0, 50)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_xticks(range(3))
ax.set_xticklabels(months, fontsize=12)
ax.grid(axis="y", color=RULE, lw=1)
ax.set_axisbelow(True)
clean(ax)
ax.tick_params(axis="x", pad=8)
fig.tight_layout(pad=0.4)
fig.savefig("assets/chart_nps.png", transparent=True)
plt.close(fig)
print("charts ok")
