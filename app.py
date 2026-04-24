import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT PALETTE ── */
:root {
  --bg:        #0a0c14;
  --surface:   #111524;
  --surface2:  #181d2e;
  --border:    #252a3d;
  --accent:    #f5a623;
  --accent2:   #e85d8a;
  --accent3:   #5de8c1;
  --text:      #e8eaf0;
  --muted:     #6b7280;
  --gold:      #f5a623;
}

/* ── BASE ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: var(--bg); color: var(--text); }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label { color: var(--muted) !important; font-size:11px; letter-spacing:1px; text-transform:uppercase; }

/* ── HEADER ── */
.dashboard-header {
  background: linear-gradient(135deg, #111524 0%, #1a1f35 50%, #0f1320 100%);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 36px 40px;
  margin-bottom: 28px;
  position: relative;
  overflow: hidden;
}
.dashboard-header::before {
  content: '';
  position: absolute;
  top: -60px; right: -60px;
  width: 260px; height: 260px;
  background: radial-gradient(circle, rgba(245,166,35,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.dashboard-header::after {
  content: '';
  position: absolute;
  bottom: -80px; left: 30%;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(93,232,193,0.07) 0%, transparent 70%);
  border-radius: 50%;
}
.header-eyebrow {
  font-family:'DM Mono',monospace;
  font-size:11px; letter-spacing:3px;
  color: var(--accent); text-transform:uppercase; margin-bottom:10px;
}
.header-title {
  font-family:'Syne',sans-serif;
  font-size:42px; font-weight:800; line-height:1.1;
  color: var(--text); margin:0 0 10px 0;
}
.header-title span { color: var(--accent); }
.header-sub { font-size:14px; color: var(--muted); margin:0; }

/* ── KPI CARDS ── */
.kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:28px; }
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px 20px;
  position: relative; overflow: hidden;
  transition: border-color .2s;
}
.kpi-card:hover { border-color: var(--accent); }
.kpi-card .glow {
  position:absolute; top:-40px; right:-40px;
  width:120px; height:120px; border-radius:50%;
  opacity:.15;
}
.kpi-label { font-size:10px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-bottom:8px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:32px; font-weight:800; line-height:1; margin-bottom:6px; }
.kpi-delta { font-size:12px; color:var(--accent3); }
.kpi-delta.neg { color:var(--accent2); }

/* ── SECTION TITLE ── */
.section-title {
  font-family:'Syne',sans-serif;
  font-size:18px; font-weight:700;
  color: var(--text); margin:0 0 16px 0;
  display:flex; align-items:center; gap:10px;
}
.section-title::after {
  content:''; flex:1; height:1px;
  background: linear-gradient(90deg, var(--border), transparent);
}

/* ── CHART CARD ── */
.chart-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
  margin-bottom: 20px;
}
.chart-card-title { font-size:13px; font-weight:500; color:var(--muted); margin-bottom:16px; letter-spacing:.5px; }

/* ── INSIGHT PILL ── */
.insight-row { display:flex; gap:12px; flex-wrap:wrap; margin-bottom:28px; }
.insight-pill {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 8px 18px;
  font-size: 13px; color: var(--text);
  display: inline-flex; align-items: center; gap: 8px;
}
.insight-pill strong { color: var(--accent); }

/* ── LEADERBOARD ── */
.lb-row {
  display:flex; align-items:center; justify-content:space-between;
  padding: 12px 0; border-bottom: 1px solid var(--border);
}
.lb-row:last-child { border-bottom: none; }
.lb-rank { font-family:'DM Mono',monospace; font-size:11px; color:var(--muted); width:24px; }
.lb-name { flex:1; font-size:14px; }
.lb-bar-wrap { width:120px; background:var(--surface2); border-radius:4px; height:6px; margin:0 16px; }
.lb-bar { height:6px; border-radius:4px; background: linear-gradient(90deg, var(--accent), var(--accent2)); }
.lb-value { font-family:'DM Mono',monospace; font-size:13px; color:var(--accent); white-space:nowrap; }

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; }
[data-testid="stMetric"] { display:none; }

/* ── MATPLOTLIB OVERRIDE ── */
div[data-testid="stImage"] img { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── MATPLOTLIB THEME ──────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor':  '#111524',
    'axes.facecolor':    '#111524',
    'axes.edgecolor':    '#252a3d',
    'axes.labelcolor':   '#6b7280',
    'axes.titlecolor':   '#e8eaf0',
    'xtick.color':       '#6b7280',
    'ytick.color':       '#6b7280',
    'grid.color':        '#1e2335',
    'grid.linestyle':    '--',
    'grid.linewidth':    0.6,
    'text.color':        '#e8eaf0',
    'font.family':       'DejaVu Sans',
})
ACCENT   = '#f5a623'
ACCENT2  = '#e85d8a'
ACCENT3  = '#5de8c1'
SURFACE  = '#111524'


# ═══════════════════════════════════════════════════════════════════════════════
#  DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    df = df.dropna(how='all')
    df = df[df['Order Date'].str[0:2] != 'Or']
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
    df['Price Each']       = pd.to_numeric(df['Price Each'])
    df['Sales']            = df['Quantity Ordered'] * df['Price Each']
    df['Month']            = df['Order Date'].str[0:2].astype('int32')
    df['City']             = df['Purchase Address'].apply(lambda x: x.split(',')[1].strip())
    df['State']            = df['Purchase Address'].apply(lambda x: x.split(',')[2].strip().split(' ')[0])
    # parse hour
    df['Hour'] = df['Order Date'].apply(lambda x: int(x.split(' ')[1].split(':')[0]) if ' ' in str(x) else 0)
    return df

df = load_data()

MONTHS = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
          7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}

# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR FILTERS
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 24px 0'>
        <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#f5a623'>⚡ Sales Intel</div>
        <div style='font-size:11px;color:#6b7280;letter-spacing:2px;text-transform:uppercase;margin-top:4px'>Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**FILTERS**")
    months_sel = st.multiselect(
        "Month", list(MONTHS.keys()),
        default=list(MONTHS.keys()),
        format_func=lambda x: MONTHS[x]
    )
    cities_all = sorted(df['City'].unique().tolist())
    cities_sel = st.multiselect("City", cities_all, default=cities_all)

    products_all = sorted(df['Product'].unique().tolist())
    products_sel = st.multiselect("Product", products_all, default=products_all)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:11px;color:#6b7280;line-height:1.8'>
    <div style='text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px'>Legend</div>
    <span style='color:#f5a623'>●</span> Revenue &nbsp;
    <span style='color:#e85d8a'>●</span> Growth &nbsp;
    <span style='color:#5de8c1'>●</span> Volume
    </div>
    """, unsafe_allow_html=True)

# apply filters
mask = (
    df['Month'].isin(months_sel) &
    df['City'].isin(cities_sel) &
    df['Product'].isin(products_sel)
)
dff = df[mask]

# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dashboard-header">
    <div class="header-eyebrow">⚡ Annual Intelligence Report · 2019</div>
    <h1 class="header-title">Sales <span>Performance</span><br>Analytics</h1>
    <p class="header-sub">Comprehensive view across cities, products, and time · Filtered to your selection</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  KPI CARDS
# ═══════════════════════════════════════════════════════════════════════════════
total_rev     = dff['Sales'].sum()
total_orders  = dff.shape[0]
avg_order_val = dff['Sales'].mean()
top_city      = dff.groupby('City')['Sales'].sum().idxmax() if not dff.empty else "—"

# month-over-month for delta (last two months in selection)
monthly_sum = dff.groupby('Month')['Sales'].sum().sort_index()
if len(monthly_sum) >= 2:
    delta_pct = (monthly_sum.iloc[-1] - monthly_sum.iloc[-2]) / monthly_sum.iloc[-2] * 100
    delta_str = f"{'▲' if delta_pct>=0 else '▼'} {abs(delta_pct):.1f}% vs prev month"
    delta_cls = '' if delta_pct >= 0 else 'neg'
else:
    delta_str, delta_cls = "—", ""

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="glow" style="background:radial-gradient(circle,#f5a623,transparent)"></div>
    <div class="kpi-label">Total Revenue</div>
    <div class="kpi-value" style="color:#f5a623">${total_rev/1e6:.2f}M</div>
    <div class="kpi-delta {delta_cls}">{delta_str}</div>
  </div>
  <div class="kpi-card">
    <div class="glow" style="background:radial-gradient(circle,#5de8c1,transparent)"></div>
    <div class="kpi-label">Total Orders</div>
    <div class="kpi-value" style="color:#5de8c1">{total_orders:,}</div>
    <div class="kpi-delta">across {len(months_sel)} months</div>
  </div>
  <div class="kpi-card">
    <div class="glow" style="background:radial-gradient(circle,#e85d8a,transparent)"></div>
    <div class="kpi-label">Avg Order Value</div>
    <div class="kpi-value" style="color:#e85d8a">${avg_order_val:.0f}</div>
    <div class="kpi-delta">per transaction</div>
  </div>
  <div class="kpi-card">
    <div class="glow" style="background:radial-gradient(circle,#a78bfa,transparent)"></div>
    <div class="kpi-label">Top City</div>
    <div class="kpi-value" style="color:#a78bfa;font-size:22px">{top_city}</div>
    <div class="kpi-delta">highest revenue</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  ROW 1 — Monthly Sales + Hourly Pattern
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns([3, 2], gap="medium")

with col1:
    st.markdown('<p class="section-title">Monthly Revenue Trend</p>', unsafe_allow_html=True)
    monthly = dff.groupby('Month')['Sales'].sum().reindex(range(1,13), fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 3.6))
    fig.patch.set_facecolor(SURFACE)

    x = np.arange(1, 13)
    bars = ax.bar(x, monthly.values, color=ACCENT, alpha=0.25, width=0.6, zorder=2)

    # highlight top bar
    peak = monthly.idxmax()
    bars[peak - 1].set_alpha(1)
    bars[peak - 1].set_color(ACCENT)

    # overlay line
    ax.plot(x, monthly.values, color=ACCENT, linewidth=2.5, zorder=3, marker='o',
            markersize=5, markerfacecolor=SURFACE, markeredgewidth=2, markeredgecolor=ACCENT)

    ax.set_xticks(x)
    ax.set_xticklabels([MONTHS[m] for m in x], fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1e6:.1f}M'))
    ax.grid(axis='y', zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    # annotate peak
    ax.annotate(f'Peak\n${monthly[peak]/1e6:.2f}M',
                xy=(peak, monthly[peak]), xytext=(peak+0.5, monthly[peak]*1.04),
                fontsize=8, color=ACCENT,
                arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.2))

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown('<p class="section-title">Orders by Hour of Day</p>', unsafe_allow_html=True)
    hourly = dff.groupby('Hour')['Sales'].count().reindex(range(24), fill_value=0)

    fig, ax = plt.subplots(figsize=(5, 3.6))
    fig.patch.set_facecolor(SURFACE)

    colors = [ACCENT3 if h in [11, 12, 13, 19, 20] else '#1e2d3d' for h in range(24)]
    ax.barh(range(24), hourly.values, color=colors, height=0.7, zorder=2)
    ax.set_yticks([0, 6, 12, 18, 23])
    ax.set_yticklabels(['12am', '6am', '12pm', '6pm', '11pm'], fontsize=9)
    ax.set_xlabel('Orders', fontsize=9)
    ax.grid(axis='x', zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    # peak label
    peak_h = hourly.idxmax()
    ax.annotate(f'Peak {peak_h}:00', xy=(hourly[peak_h], peak_h),
                xytext=(hourly[peak_h]*0.55, peak_h+1.5),
                fontsize=8, color=ACCENT3,
                arrowprops=dict(arrowstyle='->', color=ACCENT3, lw=1))

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════════════
#  ROW 2 — City Revenue + Product Market Share
# ═══════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns([3, 2], gap="medium")

with col3:
    st.markdown('<p class="section-title">Revenue by City</p>', unsafe_allow_html=True)
    city_rev = dff.groupby('City')['Sales'].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor(SURFACE)

    palette = [ACCENT if i == len(city_rev)-1 else ACCENT2 if i >= len(city_rev)-3 else '#2a3252'
               for i in range(len(city_rev))]

    bars = ax.barh(city_rev.index, city_rev.values, color=palette, height=0.6, zorder=2)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1e6:.1f}M'))
    ax.grid(axis='x', zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)
    ax.tick_params(axis='y', labelsize=9)

    # value labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(city_rev)*0.01, bar.get_y()+bar.get_height()/2,
                f'${w/1e6:.2f}M', va='center', fontsize=8, color='#6b7280')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col4:
    st.markdown('<p class="section-title">Product Mix</p>', unsafe_allow_html=True)
    prod_rev = dff.groupby('Product')['Sales'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor(SURFACE)

    donut_colors = ['#f5a623','#e85d8a','#5de8c1','#a78bfa','#60a5fa','#f97316','#34d399']
    wedges, texts, autotexts = ax.pie(
        prod_rev.values, labels=None,
        colors=donut_colors[:len(prod_rev)],
        autopct='%1.0f%%', pctdistance=0.78,
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor=SURFACE, linewidth=2)
    )
    for at in autotexts:
        at.set_fontsize(7.5)
        at.set_color('white')

    # centre label
    ax.text(0, 0, f'{len(prod_rev)}\nProducts', ha='center', va='center',
            fontsize=11, fontweight='bold', color='#e8eaf0')

    ax.legend(wedges, [p[:20] for p in prod_rev.index],
              loc='lower center', bbox_to_anchor=(0.5, -0.12),
              ncol=2, fontsize=7, frameon=False, labelcolor='#9ca3af')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════════════
#  ROW 3 — Product Leaderboard + Quantity vs Revenue Scatter
# ═══════════════════════════════════════════════════════════════════════════════
col5, col6 = st.columns([2, 3], gap="medium")

with col5:
    st.markdown('<p class="section-title">Top Products</p>', unsafe_allow_html=True)
    top_prods = dff.groupby('Product').agg(Revenue=('Sales','sum'), Units=('Quantity Ordered','sum')).sort_values('Revenue', ascending=False).head(8)
    max_rev = top_prods['Revenue'].max()

    lb_html = ""
    for i, (prod, row) in enumerate(top_prods.iterrows()):
        pct = row['Revenue'] / max_rev * 100
        lb_html += f"""
        <div class="lb-row">
          <div class="lb-rank">{i+1:02d}</div>
          <div class="lb-name" style="font-size:13px">{prod}</div>
          <div class="lb-bar-wrap"><div class="lb-bar" style="width:{pct:.0f}%"></div></div>
          <div class="lb-value">${row['Revenue']/1e3:.0f}K</div>
        </div>"""

    st.markdown(f'<div class="chart-card">{lb_html}</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<p class="section-title">Revenue vs Volume by Product</p>', unsafe_allow_html=True)
    pdata = dff.groupby('Product').agg(Revenue=('Sales','sum'), Units=('Quantity Ordered','sum')).reset_index()

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    fig.patch.set_facecolor(SURFACE)

    scatter_colors = plt.cm.plasma(np.linspace(0.15, 0.85, len(pdata)))
    sc = ax.scatter(pdata['Units'], pdata['Revenue'],
                    s=pdata['Revenue']/pdata['Revenue'].max()*600 + 60,
                    c=scatter_colors, alpha=0.85, zorder=3, edgecolors='none')

    for _, row in pdata.iterrows():
        ax.annotate(row['Product'][:14], (row['Units'], row['Revenue']),
                    textcoords='offset points', xytext=(6,4),
                    fontsize=7, color='#9ca3af')

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1e6:.1f}M'))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v/1e3:.0f}K'))
    ax.set_xlabel('Units Sold', fontsize=9)
    ax.set_ylabel('Revenue', fontsize=9)
    ax.grid(zorder=0)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.tick_params(length=0)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════════════
#  INSIGHT PILLS
# ═══════════════════════════════════════════════════════════════════════════════
best_month  = MONTHS.get(monthly_sum.idxmax(), '—') if not monthly_sum.empty else '—'
best_prod   = dff.groupby('Product')['Sales'].sum().idxmax() if not dff.empty else '—'
peak_hour   = dff.groupby('Hour')['Sales'].count().idxmax() if not dff.empty else '—'
best_state  = dff.groupby('State')['Sales'].sum().idxmax() if 'State' in dff.columns and not dff.empty else '—'

st.markdown(f"""
<div class="insight-row">
  <div class="insight-pill">📅 Peak month: <strong>{best_month}</strong></div>
  <div class="insight-pill">📦 Best product: <strong>{str(best_prod)[:24]}</strong></div>
  <div class="insight-pill">🕐 Busiest hour: <strong>{peak_hour}:00</strong></div>
  <div class="insight-pill">🏙️ Top city: <strong>{top_city}</strong></div>
  <div class="insight-pill">💰 Total orders: <strong>{total_orders:,}</strong></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  RAW DATA EXPANDER
# ═══════════════════════════════════════════════════════════════════════════════
with st.expander("🗂  Raw Data Explorer"):
    search = st.text_input("Search product or city", "")
    view = dff.copy()
    if search:
        mask2 = (view['Product'].str.contains(search, case=False, na=False) |
                 view['City'].str.contains(search, case=False, na=False))
        view = view[mask2]
    st.dataframe(
        view[['Order Date','Product','Quantity Ordered','Price Each','Sales','City','Month']]\
            .sort_values('Sales', ascending=False).head(200),
        use_container_width=True,
        height=280
    )
    st.caption(f"Showing {min(200, len(view)):,} of {len(view):,} matching records")