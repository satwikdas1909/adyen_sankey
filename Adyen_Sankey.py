

"""
Adyen FY‑2024 Sankey diagram
Author: ChatGPT (April 2025)

How to run & publish
--------------------
$ pip install plotly
$ python adyen_2024_sankey.py        # creates adyen_2024_sankey.html
$ git init                           # if this is a fresh folder
$ git remote add origin https://github.com/satwikdas1909/adyen_sankey
$ git add adyen_2024_sankey.py adyen_2024_sankey.html
$ git commit -m "Add Adyen FY‑2024 Sankey diagram"
$ git branch -M main
$ git push -u origin main
"""

import plotly.graph_objects as go

# -------------------------------------------------
# COLOUR PALETTE  (same swatch you provided)
# -------------------------------------------------
DARK_GREEN  = "#d4d72c"   # vertical blocks for revenue/profit
LIGHT_GREEN = "#f1f3b6"   # flows for revenue/profit or credits
DARK_BLUE   = "#008bb9"   # vertical blocks for cost items
LIGHT_BLUE  = "#C2EBF8"   # flows for cost items
TEAL        = "#0d4b5a"   # (unused) – could mark special credits

# -------------------------------------------------
# NODES  (index order matters for link table below)
# -------------------------------------------------
labels = [
    # revenue + cost‑of‑service branch
    "Non‑interest Revenue",      # 0
    "Cost of Service",           # 1 (vertical block)
    "FI Costs",                  # 2
    "COGS",                      # 3
    "Net Non‑interest Revenue",  # 4 (vertical block)

    # interest layer
    "Interest Income",           # 5
    "Interest Expense",          # 6

    # net‑revenue & opex branch
    "Net Revenue",               # 7 (vertical block)
    "Employee Benefits",         # 8
    "Amort./Depr.",              # 9
    "Other Opex",                #10
    "Other Income",              #11  (credit)

    # operating profit
    "Operating Profit",          #12 (vertical block)

    # finance
    "Finance Income",            #13
    "Finance Expense",           #14
    "Other Fin. Results",        #15
    "Pre‑tax Income",            #16 (vertical block)

    # tax & bottom line
    "Income Tax",               #17
    "Net Income"                #18 (vertical block)
]

# -------------------------------------------------
# VALUES  (all € million, one decimal)
# -------------------------------------------------
NI_REVENUE      = 2225.6
FI_COSTS        = 148.2
COGS            = 89.7
COST_OF_SERVICE = FI_COSTS + COGS          # 237.9
NET_NI_REV      = 1987.8

INT_INCOME      = 27.1
INT_EXPENSE     = 18.8
NET_REVENUE     = 1996.1                   # per statement

EMP_BENEFITS    = 701.2
AMORT_DEPR      = 104.5
OTHER_OPEX      = 309.6
OTHER_INCOME    = 7.0
OPERATING_PROF  = 887.8

FIN_INCOME      = 349.8
FIN_EXPENSE     = 7.9
OTHER_FIN_RES   = 3.0                      # net cost
PRETAX_INCOME   = 1226.7
INCOME_TAX      = 301.6
NET_INCOME      = 925.2

# -------------------------------------------------
# LINKS  (source, target, value)
# -------------------------------------------------
links = [
    # Non‑interest revenue feeds revenue block
    (0, 1, COST_OF_SERVICE),      # to CoS
    (0, 4, NET_NI_REV),           # to Net NI revenue

    # CoS splits to details
    (1, 2, FI_COSTS),
    (1, 3, COGS),

    # Net NI revenue feeds Net revenue
    (4, 7, NET_NI_REV),

    # Interest income / expense adjust Net revenue
    (5, 7, INT_INCOME),
    (7, 6, INT_EXPENSE),          # cost outflow

    # Net revenue splits to opex items & operating profit
    (7, 8, EMP_BENEFITS),
    (7, 9, AMORT_DEPR),
    (7,10, OTHER_OPEX),
    (7,12, NET_REVENUE - EMP_BENEFITS - AMORT_DEPR - OTHER_OPEX),  # 880.8

    # Other operating income flows into Operating Profit
    (11,12, OTHER_INCOME),

    # Operating profit flows to finance expense / other & pretax
    (12,14, FIN_EXPENSE),
    (12,15, OTHER_FIN_RES),
    (12,16, OPERATING_PROF - FIN_EXPENSE - OTHER_FIN_RES),          # 876.9

    # Finance income flows into pretax
    (13,16, FIN_INCOME),

    # Pretax → tax & bottom line
    (16,17, INCOME_TAX),
    (16,18, NET_INCOME)
]

sources, targets, values = zip(*links)

# -------------------------------------------------
# NODE COLOURS
# -------------------------------------------------
node_colours = [
    LIGHT_GREEN,           # Non‑interest revenue
    DARK_BLUE,             # Cost‑of‑Service block
    LIGHT_BLUE, LIGHT_BLUE,

    DARK_GREEN,            # Net NI revenue block

    LIGHT_GREEN,           # Interest income node
    LIGHT_BLUE,            # Interest expense node

    DARK_GREEN,            # Net revenue block
    LIGHT_BLUE, LIGHT_BLUE, LIGHT_BLUE,
    TEAL,                  # Other income (credit)

    DARK_GREEN,            # Operating profit block

    LIGHT_GREEN,           # Finance income (credit)
    LIGHT_BLUE,            # Finance expense
    LIGHT_BLUE,            # Other fin results (cost)

    DARK_GREEN,            # Pre‑tax block
    LIGHT_BLUE,            # Tax
    DARK_GREEN             # Net income
]

# -------------------------------------------------
# LINK COLOURS  (flows)
# -------------------------------------------------
link_colours = []
COST_TARGETS = {1,2,3,6,8,9,10,14,15,17}
CREDIT_TARGETS = {11,13}
for s, t, _ in links:
    if t in COST_TARGETS:
        link_colours.append(LIGHT_BLUE)
    elif t in CREDIT_TARGETS:
        link_colours.append(LIGHT_GREEN)   # credits
    else:
        link_colours.append(LIGHT_GREEN)

# -------------------------------------------------
# BUILD & SAVE
# -------------------------------------------------
fig = go.Figure(data=[go.Sankey(
    arrangement="snap",
    node=dict(
        pad=16,
        thickness=18,
        line=dict(width=0.4, color="grey"),
        label=labels,
        color=node_colours
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colours,
        hovertemplate='%{source.label} → %{target.label}<br>€%{value:,.1f} m<extra></extra>'
    )
)])

fig.update_layout(
    title="Adyen – FY 2024 Income‑statement Flow (€ m)",
    font=dict(size=11)
)

# save interactive HTML
fig.write_html("adyen_2024_sankey.html")
print("✅  adyen_2024_sankey.html written")
fig.show()