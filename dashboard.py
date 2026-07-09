import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="FII to DII — The Dominance Shift",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Dark editorial theme ──────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        background-color: #1A1A24;
        color: #E8E6E0;
    }
    .stApp { background-color: #1A1A24; }

    .hero {
        background: linear-gradient(135deg, #1A1A24 0%, #12121C 100%);
        border-bottom: 1px solid #2E2E3E;
        padding: 60px 40px 50px 40px;
        text-align: center;
        margin-bottom: 0;
    }
    .hero-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #C4933F;
        margin-bottom: 16px;
    }
    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 52px;
        font-weight: 700;
        color: #F0EDE6;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    .hero-thesis {
        font-family: 'Inter', sans-serif;
        font-size: 16px;
        font-weight: 300;
        color: #9B9891;
        max-width: 680px;
        margin: 0 auto 32px auto;
        line-height: 1.7;
        font-style: italic;
    }
    .hero-divider {
        width: 60px;
        height: 2px;
        background: #C4933F;
        margin: 0 auto;
    }
    .section-label {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #C4933F;
        margin-bottom: 8px;
    }
    .section-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 28px;
        color: #F0EDE6;
        margin-bottom: 6px;
    }
    .section-sub {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #6B6860;
        margin-bottom: 28px;
    }
    .kpi-card {
        background: #20202E;
        border: 1px solid #2E2E3E;
        border-top: 2px solid #C4933F;
        border-radius: 4px;
        padding: 20px 22px;
        margin-bottom: 12px;
    }
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #6B6860;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-family: 'Inter', sans-serif;
        font-size: 26px;
        font-weight: 600;
        color: #F0EDE6;
        margin-bottom: 4px;
    }
    .kpi-sub {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #C4933F;
    }
    .event-card {
        background: #20202E;
        border: 1px solid #2E2E3E;
        border-left: 3px solid #C4933F;
        border-radius: 4px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .event-year {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.15em;
        color: #C4933F;
        margin-bottom: 4px;
    }
    .event-name {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: #F0EDE6;
        margin-bottom: 4px;
    }
    .event-desc {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #6B6860;
        line-height: 1.5;
    }
    .insight-box {
        background: #1E1E2C;
        border: 1px solid #2E2E3E;
        border-left: 3px solid #4A7FA5;
        border-radius: 4px;
        padding: 16px 20px;
        margin-top: 16px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #9B9891;
        line-height: 1.6;
    }
    .glossary-term {
        background: #20202E;
        border: 1px solid #2E2E3E;
        border-radius: 4px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .glossary-title {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: #C4933F;
        margin-bottom: 6px;
    }
    .glossary-text {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: #9B9891;
        line-height: 1.6;
    }
    .divider {
        border: none;
        border-top: 1px solid #2E2E3E;
        margin: 40px 0;
    }
    /* Override streamlit defaults */
    .stMarkdown p { color: #9B9891; }
    h1, h2, h3 { color: #F0EDE6 !important; }
</style>
""", unsafe_allow_html=True)

# ── Chart defaults ────────────────────────────────────────────
BG = '#1A1A24'
CARD_BG = '#20202E'
AMBER = '#C4933F'
BLUE = '#4A7FA5'
TEXT = '#E8E6E0'
MUTED = '#6B6860'
GRID = '#2E2E3E'

def style_ax(ax, bg=CARD_BG):
    ax.set_facecolor(bg)
    ax.figure.patch.set_facecolor(bg)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.title.set_color(TEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.8)
    ax.set_axisbelow(True)

# ── Data ──────────────────────────────────────────────────────
@st.cache_data
def load():
    f1 = pd.read_csv('data/market_flows.csv')
    f2 = pd.read_csv('data/volatility_events.csv')
    f3 = pd.read_csv('data/dii_composition.csv')
    f1['NIFTY_close'] = pd.to_numeric(f1['NIFTY_close'].replace('-', np.nan), errors='coerce')
    f1['SENSEX_close'] = pd.to_numeric(f1['SENSEX_close'], errors='coerce')
    return f1, f2, f3

flows, crises, dii = load()

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">India Capital Markets · 1992 – 2025</div>
    <div class="hero-title">FII to DII:<br>The Dominance Shift</div>
    <div class="hero-thesis">
        How three decades of Foreign Capital dependence gave way to Domestic financial muscle-
        Why Indian markets no longer panic when foreign investors leave.
    </div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

fii_2025 = flows[flows['Year'] == 2025]['FII_crore'].values[0]
dii_2025 = flows[flows['Year'] == 2025]['DII_crore'].values[0]
aum_growth = f"{dii['MutualFunds_LakhCr'].iloc[-1] / dii['MutualFunds_LakhCr'].iloc[0]:.0f}x"
folio_2025 = dii['mf_folios_Lakh'].iloc[-1]

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">FII Net Flow — FY 2025-26</div>
        <div class="kpi-value">₹{abs(fii_2025/100000):.2f}L Cr</div>
        <div class="kpi-sub">↓ Net outflow — foreign capital retreat</div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">DII Net Flow — FY 2025-26</div>
        <div class="kpi-value">₹{dii_2025/100000:.2f}L Cr</div>
        <div class="kpi-sub">↑ Domestic capital at all-time high</div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">MF AUM Growth (2000–2025)</div>
        <div class="kpi-value">{aum_growth}</div>
        <div class="kpi-sub">From ₹0.91L Cr to ₹73.73L Cr</div>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Retail Investors (Folios)</div>
        <div class="kpi-value">{folio_2025:,.0f}L</div>
        <div class="kpi-sub">↑ 27x growth since 2000</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 1: TIMELINE ───────────────────────────────────────
st.markdown("""
<div class="section-label">Section 01</div>
<div class="section-title">The Events That Shaped the Shift</div>
<div class="section-sub">Five major market events that defined India's journey from FII dependence to DII dominance</div>
""", unsafe_allow_html=True)

events = [
    ("FY 1992-93", "Mehta Scam", "India's first market scandal. FII had just been permitted entry (Liberalisation) — initially negligible at ₹13 crore. The market had no foreign safety net, and no domestic institutional muscle either. That led to a fiasco directly in New Delhi"),
    ("FY 2008-09", "Global Crisis", "FII fled with ₹47,706 crore as Lehman brothers collapsed. For the first time, DII absorbed the selling, i.e., ₹60,040 crore in net buying. The market still fell 38%, but DII had shown it could step up. The first proof of cushion concept."),
    ("FY 2013-14", "Taper Tantrum", "US Federal Reserve signalled tapering of Quantitative Easing. FII actually net bought ₹79,709 crore but DII exited with ₹28,060 crore — still not reliable as a stabilizer. The domestic ecosystem was in developing phase but not yet mature."),
    ("FY 2019-20", "COVID-19 Crash", "FII modest inflow of ₹6,152 crore, DII deployed a massive ₹1,29,300 crore. Market fell 23.8% but recovered in just 10 months. DII had become a genuine counterweight to market panic for the first time."),
    ("FY 2022-23", "Russia-Ukraine & Rate Hikes", "FII sold ₹37,632 crore as global uncertainty spiked. DII absorbed ₹2,55,500 crore without blinking. Market barely moved — only +0.72%. The thesis was complete. <strong> DII had structurally replaced FII as the market's anchor."),
]

col_a, col_b = st.columns([1, 1])
for i, (year, name, desc) in enumerate(events):
    col = col_a if i % 2 == 0 else col_b
    with col:
        st.markdown(f"""
        <div class="event-card">
            <div class="event-year">{year}</div>
            <div class="event-name">{name}</div>
            <div class="event-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 2: CENTREPIECE CHART ─────────────────────────────
st.markdown("""
<div class="section-label">Section 02</div>
<div class="section-title">The Flows — FII vs DII (1992–2025)</div>
<div class="section-sub">Net investment flows in ₹ Crore across all checkpoint fiscal years</div>
""", unsafe_allow_html=True)

years    = flows['Year'].values
fii_vals = flows['FII_crore'].values
dii_flow = flows['DII_crore'].values
contexts = flows['Context/Event'].values

hover_fii = [f"<b>FY {y}-{str(y+1)[2:]}</b><br>Event: {c}<br>FII Net Flow: ₹{v:,.0f} Cr" 
             for y, c, v in zip(years, contexts, fii_vals)]
hover_dii = [f"<b>FY {y}-{str(y+1)[2:]}</b><br>Event: {c}<br>DII Net Flow: ₹{v:,.0f} Cr" 
             for y, c, v in zip(years, contexts, dii_flow)]

fig_flow = go.Figure()

# FII fill above/below zero
fig_flow.add_trace(go.Scatter(
    x=years, y=fii_vals, fill='tozeroy',
    fillcolor='rgba(74,127,165,0.15)', line=dict(color=AMBER, width=2.5),
    mode='lines+markers', marker=dict(size=7, color=AMBER, symbol='circle'),
    name='FII Flow', hovertemplate='%{customdata}<extra></extra>',
    customdata=hover_fii
))

# DII fill above/below zero
fig_flow.add_trace(go.Scatter(
    x=years, y=dii_flow, fill='tozeroy',
    fillcolor='rgba(196,147,63,0.12)', line=dict(color=BLUE, width=2.5),
    mode='lines+markers', marker=dict(size=7, color=BLUE, symbol='circle'),
    name='DII Flow', hovertemplate='%{customdata}<extra></extra>',
    customdata=hover_dii
))

# Zero line
fig_flow.add_hline(y=0, line_dash='dash', line_color=GRID, line_width=1)

# Crisis year vertical lines
for _, cr in crises.iterrows():
    fig_flow.add_vline(x=cr['Year'], line_dash='dot', line_color='#A54A4A', 
                       line_width=1, opacity=0.5,
                       annotation_text=str(cr['Year']),
                       annotation_position='top',
                       annotation_font_color='#A54A4A',
                       annotation_font_size=10)

fig_flow.update_layout(
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=TEXT, family='Inter, DejaVu Sans'),
    title=dict(text='FII vs DII Net Investment Flows — The Divergence (FY 1992-93 to FY 2025-26)',
               font=dict(size=14, color=TEXT), x=0.01),
    xaxis=dict(gridcolor=GRID, color=MUTED, title='Fiscal Year'),
    yaxis=dict(gridcolor=GRID, color=MUTED, title='Net Flow (₹ Crore)',
               tickformat=',.0f', tickprefix='₹'),
    legend=dict(bgcolor=CARD_BG, bordercolor=GRID, borderwidth=1,
                font=dict(color=TEXT)),
    hovermode='x unified',
    height=420,
    margin=dict(l=60, r=30, t=60, b=50)
)

st.plotly_chart(fig_flow, use_container_width=True)

st.markdown("""
<div class="insight-box">
    <strong style="color:#C4933F">What this chart tells you: </strong> Until 2019, FII and DII flows were comparable in scale.
     2020 onwards, DII flows began dwarfing FII — not because FII got smaller, but because domestic capital
    grew so large it simply overtook foreign flows. By FY 2025-26, DII deployed ₹8,49,000 crore against FII's
    ₹2,26,000 crore outflow. The gap is no longer cyclical — it is structural.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 3: CRISIS BEHAVIOUR ──────────────────────────────
st.markdown("""
<div class="section-label">Section 03</div>
<div class="section-title">Crisis Behaviour — How Each Side Responded</div>
<div class="section-sub">FII and DII conduct during India's defining market shocks</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    crisis_labels = [f"{r['Year']}<br>{r['Context/Event']}" for _, r in crises.iterrows()]
    fii_c_colors = [AMBER if v >= 0 else '#A54A4A' for v in crises['FII_crore']]
    dii_c_colors = [BLUE if v >= 0 else '#7A5A2A' for v in crises['DII_crore']]

    fig_crisis = go.Figure()
    fig_crisis.add_trace(go.Bar(
        name='FII', x=crisis_labels, y=crises['FII_crore'],
        marker_color=fii_c_colors, opacity=0.85,
        hovertemplate='<b>FII</b><br>%{x}<br>₹%{y:,.0f} Cr<extra></extra>'
    ))
    fig_crisis.add_trace(go.Bar(
        name='DII', x=crisis_labels, y=crises['DII_crore'],
        marker_color=dii_c_colors, opacity=0.85,
        hovertemplate='<b>DII</b><br>%{x}<br>₹%{y:,.0f} Cr<extra></extra>'
    ))
    fig_crisis.add_hline(y=0, line_color=GRID, line_width=1)
    fig_crisis.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT), barmode='group',
        title=dict(text='Net Flows During Crisis Years', font=dict(size=12, color=TEXT), x=0.01),
        xaxis=dict(gridcolor=GRID, color=MUTED),
        yaxis=dict(gridcolor=GRID, color=MUTED, title='₹ Crore', tickformat=',.0f', tickprefix='₹'),
        legend=dict(bgcolor=CARD_BG, bordercolor=GRID, font=dict(color=TEXT)),
        height=380, margin=dict(l=60, r=20, t=50, b=60)
    )
    st.plotly_chart(fig_crisis, use_container_width=True)

with col_b:
    fig_impact = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = [AMBER if d < 0 else BLUE for d in crises['Market_Movement%']]
    fig_impact.add_trace(go.Bar(
        x=[str(y) for y in crises['Year']], y=crises['Market_Movement%'],
        marker_color=bar_colors, opacity=0.85, name='Market Movement (%)',
        hovertemplate='<b>%{x}</b><br>Market: %{y:.2f}%<extra></extra>'
    ), secondary_y=False)
    fig_impact.add_trace(go.Scatter(
        x=[str(y) for y in crises['Year']], y=crises['recovery_month'],
        mode='lines+markers', marker=dict(size=9, color='#7FB5D5', symbol='diamond'),
        line=dict(color='#7FB5D5', width=2, dash='dash'),
        name='Recovery (months)',
        hovertemplate='<b>%{x}</b><br>Recovery: %{y} months<extra></extra>'
    ), secondary_y=True)
    fig_impact.add_hline(y=0, line_color=GRID, line_width=1)
    fig_impact.update_layout(
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        title=dict(text='Market Impact & Recovery Time', font=dict(size=12, color=TEXT), x=0.01),
        xaxis=dict(gridcolor=GRID, color=MUTED),
        yaxis=dict(gridcolor=GRID, color=MUTED, title='Market Movement (%)'),
        yaxis2=dict(gridcolor=GRID, color='#7FB5D5', title='Recovery (months)'),
        legend=dict(bgcolor=CARD_BG, bordercolor=GRID, font=dict(color=TEXT)),
        height=380, margin=dict(l=60, r=60, t=50, b=60)
    )
    st.plotly_chart(fig_impact, use_container_width=True)

# Crisis table
st.markdown("<br>", unsafe_allow_html=True)
crisis_display = crises[['Year', 'Context/Event', 'Market_Movement%', 'recovery_month',
                           'FII_behavior', 'DII_behavior']].copy()
crisis_display.columns = ['Year', 'Event', 'Market Move (%)', 'Recovery (months)',
                           'FII Behaviour', 'DII Behaviour']
crisis_display = crisis_display.set_index('Year')
st.dataframe(crisis_display, use_container_width=True)

st.markdown("""
<div class="insight-box">
    <strong style="color:#C4933F">The pattern:</strong> In 1992, there was no DII response — the institution barely existed, even in our project we had to use REIs as DII proxy.
    By 2008, DII absorbed FII selling for the first time. By 2022, DII absorbed 6.8x more than FII sold.
    Each crisis reveals a more confident, larger and more structurally embedded domestic investor base.
    The 2022 Russia-Ukraine event is the clearest proof — FII sold ₹37,632 crore, market moved only +0.72%.
    DII had become the floor.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 4: DII STRENGTH ───────────────────────────────────
st.markdown("""
<div class="section-label">Section 04</div>
<div class="section-title">Where the Domestic Muscle Came From?</div>
<div class="section-sub">The structural constraints behind DII's rise — mutual funds, retail investors, and institutional capital</div>
""", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    fig, ax = plt.subplots(figsize=(7, 5))
    style_ax(ax)
    ax.fill_between(dii['Year'], dii['MutualFunds_LakhCr'], alpha=0.2, color=AMBER)
    ax.plot(dii['Year'], dii['MutualFunds_LakhCr'], color=AMBER, linewidth=2.5,
            marker='o', markersize=7, label='MF AUM (₹ Lakh Cr)')
    ax2 = ax.twinx()
    ax2.plot(dii['Year'], dii['LIC_equity_LakhCr'], color=BLUE, linewidth=2,
             marker='s', markersize=6, linestyle='--', label='LIC Equity (₹ Lakh Cr)')
    ax2.tick_params(colors=MUTED, labelsize=9)
    ax2.set_ylabel('LIC Equity (₹ Lakh Cr)', color=MUTED, fontsize=9)
    for spine in ax2.spines.values():
        spine.set_edgecolor(GRID)
    for yr, val in zip(dii['Year'], dii['MutualFunds_LakhCr']):
        ax.annotate(f'₹{val}L Cr', (yr, val), textcoords='offset points',
                    xytext=(0, 10), ha='center', fontsize=7.5, color=MUTED)
    ax.set_title('MF AUM & LIC Equity Growth', color=TEXT, fontsize=11, pad=12)
    ax.set_ylabel('MF AUM (₹ Lakh Cr)', color=MUTED, fontsize=9)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1+lines2, labels1+labels2, facecolor=CARD_BG,
              edgecolor=GRID, labelcolor=TEXT, fontsize=8)
    st.pyplot(fig)
    plt.close()

with col_b:
    fig, ax = plt.subplots(figsize=(7, 5))
    style_ax(ax)
    color_grad = [plt.cm.YlOrBr(i/5) for i in range(6)]
    bars = ax.bar(dii['Year'], dii['mf_folios_Lakh'], color=color_grad, alpha=0.85, width=3)
    for bar, val in zip(bars, dii['mf_folios_Lakh']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                f'{val:.0f}L', ha='center', fontsize=8, color=MUTED)
    ax.set_title('Retail Investor Folios (Lakh)', color=TEXT, fontsize=11, pad=12)
    ax.set_ylabel('Folios (Lakh)', color=MUTED, fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    # Annotate the dip
    ax.annotate('Post-2008\nretail exit', xy=(2010, 472), xytext=(2007, 800),
                fontsize=7.5, color=MUTED,
                arrowprops=dict(arrowstyle='->', color=MUTED, lw=1))
    ax.annotate('SIP boom\nbegins', xy=(2015, 477), xytext=(2012, 1200),
                fontsize=7.5, color=AMBER,
                arrowprops=dict(arrowstyle='->', color=AMBER, lw=1))
    st.pyplot(fig)
    plt.close()

st.markdown("""
<div class="insight-box">
    <strong style="color:#C4933F">The structural story:</strong> DII dominance wasn't an accident or a policy decision, it was
    the compounding effect of millions of Indians starting SIPs, EPFO channelling provident fund money into
    equity ETFs post-2015, and LIC pumping insurance premiums into markets. The folio count chart tells
    the retail story — a dip after the 2008 crash (retail investors burned and exit), then an explosion
    from 2015 onwards as the SIP culture took root. By 2025, 2,739 lakh folios means roughly every second
    Indian household has some exposure to equity markets. That was an irreversible structural shift.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 5: SENSEX JOURNEY ────────────────────────────────
st.markdown("""
<div class="section-label">Section 05</div>
<div class="section-title">The Market's Journey — Sensex 1992–2025</div>
<div class="section-sub">Index levels at each checkpoint, with crisis moments marked</div>
""", unsafe_allow_html=True)

sensex_data = flows.dropna(subset=['SENSEX_close']).copy()

hover_sensex = [
    f"<b>FY {y}-{str(y+1)[2:]}</b><br>Event: {c}<br>Sensex: {s:,.2f}<br>FII: ₹{f:,.0f} Cr<br>DII: ₹{d:,.0f} Cr"
    for y, c, s, f, d in zip(
        sensex_data['Year'], sensex_data['Context/Event'],
        sensex_data['SENSEX_close'], sensex_data['FII_crore'], sensex_data['DII_crore']
    )
]

fig_sensex = go.Figure()

fig_sensex.add_trace(go.Scatter(
    x=sensex_data['Year'], y=sensex_data['SENSEX_close'],
    fill='tozeroy', fillcolor='rgba(196,147,63,0.1)',
    line=dict(color=AMBER, width=2.5),
    mode='lines+markers',
    marker=dict(size=8, color=AMBER, symbol='circle',
                line=dict(color=CARD_BG, width=1)),
    name='Sensex Close',
    hovertemplate='%{customdata}<extra></extra>',
    customdata=hover_sensex
))

# Crisis vertical lines with annotations
for _, cr in crises.iterrows():
    match = sensex_data[sensex_data['Year'] == cr['Year']]
    if not match.empty:
        fig_sensex.add_vline(
            x=cr['Year'], line_dash='dot',
            line_color='#A54A4A', line_width=1.5, opacity=0.7,
            annotation_text=f"{cr['Year']}<br>{cr['Context/Event']}",
            annotation_position='top left',
            annotation_font_color='#A54A4A',
            annotation_font_size=9
        )

fig_sensex.update_layout(
    paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    font=dict(color=TEXT, family='Inter, DejaVu Sans'),
    title=dict(
        text='Sensex Journey — FY 1992-93 to FY 2025-26 (Hover for FII/DII context)',
        font=dict(size=14, color=TEXT), x=0.01
    ),
    xaxis=dict(gridcolor=GRID, color=MUTED, title='Fiscal Year', dtick=3),
    yaxis=dict(gridcolor=GRID, color=MUTED, title='Sensex Close',
               tickformat=',.0f'),
    hovermode='closest',
    height=420,
    margin=dict(l=60, r=30, t=70, b=50),
    showlegend=False
)

st.plotly_chart(fig_sensex, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SECTION 6: GLOSSARY ───────────────────────────────────────
st.markdown("""
<div class="section-label">Section 06</div>
<div class="section-title">Financial Literacy — Key Terms</div>
<div class="section-sub">Understanding the language of this analysis</div>
""", unsafe_allow_html=True)

terms = [
    ("FII — Foreign Institutional Investor",
     "Foreign entities — (hedge funds, sovereign wealth funds, pension funds); that invest in Indian equity and debt markets. Their flows are large, fast-moving, and highly sensitive to global macro conditions like US interest rates, dollar strength, and geopolitical risk. When global risk appetite drops, FII is typically the first to exit emerging markets like India."),
    ("DII — Domestic Institutional Investor",
     "Indian institutions deploying capital into markets — primarily mutual funds, insurance companies (LIC, HDFC Life), and EPFO. Unlike FII, DII capital is patient, long-term, and largely insulated from global panic. SIP mandates mean DII receives fresh inflows every month regardless of market conditions, making it a structural buyer."),
    ("REI — Retail Equity Investment",
     "Direct equity investment by individual retail investors (First-Generation IPO Hunters, Mutual Fund Aggregators ) — not routed through institutions. In the 1990s, before mutual funds and EPFO equity exposure became significant, REI was the primary domestic capital pool in Indian markets. Used in this analysis as a proxy for DII in the early years (FY 1992-93 crisis and FY 1998-99 crisis) since no standardised DII tracking agency existed during this period."),
    ("SEBI — Securities and Exchange Board of India",
     "India's primary capital market regulator, established in 1992. SEBI governs all market participants — FIIs, DIIs, brokers, exchanges, and listed companies. SEBI's formalisation of FII registration in 1992 and subsequent DII reporting frameworks over the 2000s are what eventually made this analysis possible. Pre-SEBI formalisation, institutional flow data is very sparse and inconsistent."),
    ("AMFI — Association of Mutual Funds in India",
     "The self regulatory body for Indian mutual fund industry, established in 1995. AMFI publishes monthly AUM figures, SIP inflow data, and folio counts — the primary source for DII composition data in this analysis. Reliable AMFI data begins from around 2000; earlier figures are estimates from industry reports."),
    ("BSE — Bombay Stock Exchange",
     "Asia's oldest stock exchange, established in 1875. The Sensex (BSE Sensitive Index) — which usually tracks 30 large-cap companies — is used as the primary market benchmark in this analysis, particularly for pre-1996 data when Nifty did not yet exist. BSE historical data is the most complete source for Indian market performance going back to the early 1990s."),
    ("NSE — National Stock Exchange",
     "Established in 1992 and operational from 1994, NSE introduced electronic trading to India. The Nifty 50 index tracks the top 50 companies by market capitalisation. Used in this analysis from 1999 onwards where available. NSE is also the primary source for FII/DII daily flow data through its publicly accessible historical datasets."),
    ("Securities",
     "Financial instruments that represent ownership (equity/shares), debt (bonds), or the right to buy/sell assets (derivatives). In this analysis, 'securities' refers primarily to listed equities — shares traded on BSE and NSE. When FII or DII 'flows' are discussed, it means net buying or selling of these listed securities on Indian exchanges, in layman terms its like receipts of stocks that proves you own them."),
    ("SIP — Systematic Investment Plan",
     "A method of investing fixed amounts into mutual funds at regular intervals — typically monthly. The SIP revolution post-2014 created a predictable river of domestic capital flowing into markets every month. By 2025, SIP monthly inflows exceed ₹25,000 crore — money that flows in regardless of whether markets are up or down."),
    ("AUM — Assets Under Management",
     "The total market value of assets managed by a fund or institution. India's mutual fund AUM growing from ₹0.91 lakh crore in 2000 to ₹73.73 lakh crore in 2025 , an 81x increase, is the single most important number in understanding why DII became dominant. More AUM means more firepower to pump during market stress."),
    ("EPFO — Employees' Provident Fund Organisation",
     "India's largest retirement savings institution managing provident fund contributions of salaried employees. Post-2015, EPFO was permitted to invest up to 15% of incremental corpus in equity ETFs — channelling retirement savings of crores of workers into the stock market. This added a massive, ultra-long-term, non-panic capital pool to DII."),
    ("LIC — Life Insurance Corporation",
     "India's largest institutional investor and insurer. LIC deploys their insurance premium collections into equity markets — its equity AUM grew from ₹0.11 lakh crore to ₹15.11 lakh crore over this period. During crisis years, LIC has historically been a counter-cyclical buyer, the initial stabilizer — purchasing when others sell, stabilizing markets."),
    ("Taper Tantrum",
     "In 2013, US Federal Reserve Chairman Ben Bernanke signalled the Fed would begin tapering its bond-buying programme (quantitative easing). Emerging markets including India saw massive FII outflows as investors feared rising US interest rates would pull capital back to the US. The rupee fell sharply. This event exposed India's vulnerability to FII dependency, a vulnerability that DII growth would eventually neutralize, and in some way this was the event that influenced the measures to be taken to counter FII dependency"),
    ("Net Flow",
     "The difference between total buying and total selling by a category of investor in a given period. A positive net flow means the category was a net buyer — more money entered markets than left. A negative net flow means net selling. This is more meaningful than gross flows because it shows the actual direction of capital movement and its market impact, and thats what we used in our project, not the gross certian value but the +/- flow in FY, which perfectly works to capture and map the purpose of the project."),
]

col_a, col_b = st.columns(2)
for i, (term, definition) in enumerate(terms):
    col = col_a if i % 2 == 0 else col_b
    with col:
        st.markdown(f"""
        <div class="glossary-term">
            <div class="glossary-title">{term}</div>
            <div class="glossary-text">{definition}</div>
        </div>""", unsafe_allow_html=True)

# ── SECTION 7: LIMITATIONS ───────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="section-label">Section 07</div>
<div class="section-title">Limitations of this Analysis</div>
<div class="section-sub">What the data cannot fully capture — and why that matters</div>
""", unsafe_allow_html=True)

limitations = [
    ("No Standardised DII Tracking in the 90s",
     "The formal DII category, as recognised by SEBI, did not exist in its current form during FY 1992-93 to FY 1998-99. DIIs in this period were fragmented across retail equity participants, UTI (Unit Trust of India), and early insurance deployments — none of which were aggregated under a single reporting framework. This analysis uses Retail Equity Investment (REI) figures as a proxy for early DII flows. These numbers should be treated as directional estimates, not precise institutional flow data."),
    ("DII Composition Data Gap: 2000–2010",
     "(DII Composition) File; tracks Mutual Fund AUM, retail folios, and LIC equity from 2005 onwards. Insurance AUM beyond LIC and EPFO equity deployment data is excluded for the pre-2015 period — EPFO was not permitted to invest in equities until FY 2015-16, and private insurance equity AUM was not consistently reported before 2010. The DII composition picture for 2000–2010 is therefore incomplete and understates total domestic institutional capital."),
    ("Market Benchmark: BSE Sensex Only (Pre-1996)",
     "Nifty 50 (NSE) was launched in April 1996. For FY 1992-93, 1993-94, and 1994-95, only BSE Sensex closing values are available and used. The Sensex tracks 30 large-cap stocks versus Nifty's 50 — this means pre-1996 market movement figures may not fully represent the broader market, particularly mid-cap volatility during the Harshad Mehta era."),
    ("Checkpoint Data, Not Continuous",
     "This analysis uses annual checkpoint data at selected fiscal years — not monthly or daily flows. Intra-year volatility, seasonal FII patterns, and short-term DII responses to specific events within a fiscal year are not captured. A monthly dataset would reveal more granular dynamics, particularly during 2020 where the COVID crash (March 2020) and recovery (April–December 2020) both fall within the same fiscal year."),
]

lim_a, lim_b = st.columns([1, 1])
for i, (title, text) in enumerate(limitations):
    col = lim_a if i % 2 == 0 else lim_b
    with col:
        st.markdown(f"""
        <div class="glossary-term" style="border-left: 3px solid #4A7FA5;">
            <div class="glossary-title" style="color:#4A7FA5;">{title}</div>
            <div class="glossary-text">{text}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box" style="margin-top:16px;">
    <strong style="color:#C4933F">Note on data integrity:</strong> Where exact figures were unavailable for early fiscal years,
    the closest reliable published figure from SEBI, BSE, RBI, or AMFI archives was used.
    All approximations are noted in the data sources. The core thesis — the structural shift from FII dependence
    to DII dominance — is supported by the data across all checkpoint years regardless of the limitations.
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding: 20px 0 40px 0;">
    <div style="font-family:'Inter',sans-serif; font-size:11px; color:#3E3E4E; letter-spacing:0.15em; text-transform:uppercase;">
        Data Sources: SEBI  NSE  BSE_Archives  AMFI  RBI  Ministry of Finance BloomBerg Morgan Stanley 
    </div>
    <div style="font-family:'Inter',sans-serif; font-size:11px; color:#3E3E4E; margin-top:8px;">
        All figures in ₹ Crore unless stated · Fiscal year basis (April–March) · Analysis period FY 1992-93 to FY 2024-25
    </div>
</div>
""", unsafe_allow_html=True)
