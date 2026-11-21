"""W3 visual system: the written rules of the W3 report, expressed as code.

Every final view imports this module, so the three views share one set of
colours, shapes, text styles, scales, number formats and layout rules.
Change a rule here and all three views change together.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# ---------------------------------------------------------------- R1 colour
# Hue carries identity only (which rule produced the value). Two hues, always
# the same meaning in every view. Validated as a categorical pair for colour
# vision deficiency (protan worst case delta E 24.7, contrast >= 3:1).
MODEL = "#2a78d6"        # logistic regression at threshold 0.60 (blue)
RULE = "#eb6834"         # current simple rule: flag every emergency admission (orange)
REFERENCE = "#898781"    # context only: random flagging, base rate, scale guides (grey)
INK = "#0b0b0b"          # titles, values, annotations
INK2 = "#52514e"         # subtitles, axis titles, row labels
MUTED = "#898781"        # tick labels, footnotes
GRID = "#e1e0d9"         # hairline gridlines
AXIS = "#c3c2b7"         # baseline and axis lines
SURFACE = "#ffffff"

# ---------------------------------------------------------------- R2 shape (identity without colour)
# The model is always a filled circle or a solid bar; the emergency rule is
# always a hollow diamond or a hatched bar. Identity survives grey-scale print.
MODEL_MARKER = dict(marker="o", markersize=9, markerfacecolor=MODEL, markeredgecolor=SURFACE, markeredgewidth=1.5)
RULE_MARKER = dict(marker="D", markersize=8, markerfacecolor=SURFACE, markeredgecolor=RULE, markeredgewidth=2.2)
RULE_HATCH = "////"

# ---------------------------------------------------------------- R3 names (same words in every view)
NAME_MODEL = "Model alert (threshold 0.60)"
NAME_RULE = "Emergency rule (flag every emergency admission)"
TERM_CAUGHT = "extreme stays caught"            # recall
TERM_FLAGGED = "admissions flagged"             # share of admissions the rule flags (review workload)
TERM_HIT = "flags that are extreme stays"       # precision
ADMISSION_TYPE_EN = {"URGENCIA": "Emergency", "OBSTETRICA": "Obstetric", "PROGRAMADA": "Scheduled", "DESCONOCIDO": "Unknown"}

# ---------------------------------------------------------------- R4 scales and units
# Shares are always shown as percentages. Recall and share flagged use 0-100 %.
# Precision and extreme-stay rates use 0-20 % in every view (every value shown is
# below 20 %) and always show the base-rate reference.
SCALE_SHARE = (0, 100)
SCALE_PRECISION = (0, 20)

def pct(x, d=1):
    """Format a value already in percent: 35.61 -> '35.6%'."""
    return f"{x:.{d}f}%"

def num(x):
    """Format a count with thousands separators: 14271 -> '14,271'."""
    return f"{int(round(x)):,}"

# ---------------------------------------------------------------- R5 text styles (points)
FONT = ["Inter", "Segoe UI", "DejaVu Sans"]
SIZE_TITLE, SIZE_SUBTITLE, SIZE_PANEL, SIZE_LABEL, SIZE_TICK, SIZE_NOTE = 13, 10, 10, 9.5, 9, 8

def apply_rcparams():
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": FONT,
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "figure.dpi": 110, "savefig.dpi": 200,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "grid.linestyle": "-", "axes.axisbelow": True,
        "xtick.color": MUTED, "ytick.color": INK2, "xtick.labelsize": SIZE_TICK, "ytick.labelsize": SIZE_LABEL,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "axes.labelcolor": INK2, "axes.labelsize": SIZE_LABEL,
        "axes.titlesize": SIZE_PANEL, "axes.titleweight": "semibold", "axes.titlecolor": INK,
        "axes.titlelocation": "left", "axes.titlepad": 8,
        "legend.frameon": False, "legend.fontsize": SIZE_LABEL,
    })

# ---------------------------------------------------------------- R6 layout and reading order
# Title (the finding, one sentence) -> subtitle (population, period, data set)
# -> legend row -> panels in the order the task is read -> footnote (definitions
# and source). Rows always list the model before the emergency rule.
PANEL_GAP = 0.12   # space between juxtaposed panels, as a share of the panel width

def frame(fig, title, subtitle, note, legend=True, legend_items=None, top=0.80):
    """Place title, subtitle, legend row and footnote in the same positions in every view."""
    fig.text(0.012, 0.975, title, fontsize=SIZE_TITLE, fontweight="semibold", color=INK, va="top")
    fig.text(0.012, 0.915, subtitle, fontsize=SIZE_SUBTITLE, color=INK2, va="top")
    if legend:
        items = legend_items or [
            Line2D([], [], linestyle="none", label=NAME_MODEL, **MODEL_MARKER),
            Line2D([], [], linestyle="none", label=NAME_RULE, **RULE_MARKER)]
        fig.legend(handles=items, loc="upper left", bbox_to_anchor=(0.006, 0.875), ncol=len(items),
                   handletextpad=0.4, columnspacing=1.6, fontsize=SIZE_LABEL, labelcolor=INK2)
    fig.text(0.012, 0.012, note, fontsize=SIZE_NOTE, color=MUTED, va="bottom", linespacing=1.35)

def bar_legend_items():
    return [Patch(facecolor=MODEL, edgecolor=SURFACE, label=NAME_MODEL),
            Patch(facecolor=SURFACE, edgecolor=RULE, hatch=RULE_HATCH, linewidth=1.2, label=NAME_RULE)]

def percent_axis(ax, lim, axis="x", step=None):
    step = step or (20 if lim[1] > 50 else 5)
    ticks = list(range(int(lim[0]), int(lim[1]) + 1, step))
    if axis == "x":
        ax.set_xlim(lim); ax.set_xticks(ticks); ax.set_xticklabels([f"{t}%" for t in ticks])
        ax.grid(axis="y", visible=False)
    else:
        ax.set_ylim(lim); ax.set_yticks(ticks); ax.set_yticklabels([f"{t}%" for t in ticks])
        ax.grid(axis="x", visible=False)

RULES = [
    ("R1 Colour", "Hue shows identity only: blue = model alert, orange = emergency rule, grey = context (random flagging, base rates, and from C3 the candidate models not chosen). No other hues. Text is never coloured."),
    ("R2 Non-colour cue", "Model = filled circle or solid bar; emergency rule = hollow diamond or hatched bar; every mark also has a direct label or a legend entry."),
    ("R3 Names", "The same plain words in every view: 'extreme stays caught' (recall), 'admissions flagged' (workload), 'flags that are extreme stays' (precision)."),
    ("R4 Scales and units", "All shares in %, one decimal in labels, whole numbers on ticks. Caught and flagged: 0-100%. Precision and extreme-stay rate: 0-20%, always with the base-rate reference. Counts with thousands separators."),
    ("R5 Text", "Title 13 pt semibold states the finding; subtitle 10 pt gives population, period and data set; panel titles 10 pt; labels 9.5 pt; ticks 9 pt; notes 8 pt."),
    ("R6 Highlight", "The chosen operating point is emphasised by size and an annotation in dark ink, never by a new colour. Everything else stays at normal weight."),
    ("R7 Layout and spacing", "Title, subtitle, legend, panels in task order, footnote, in fixed positions with the same margins. Equal gaps between panels. Model row before emergency-rule row. Hairline grid on the value axis only; no top or right frame."),
    ("R8 More models", "If more candidate models are shown (C3), they are grey points or lines; only the chosen model is blue (R6), so R1 still holds."),
]
