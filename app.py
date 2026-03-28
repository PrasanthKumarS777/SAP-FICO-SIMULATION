# SAP FI/CO Financial Simulation Dashboard
# PrecisionParts Pvt. Ltd. | Company Code: IN01 | Fiscal Year: 2024

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="SAP FI/CO | PrecisionParts Pvt. Ltd.",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

C = {
    "bg":          "#0A1F14",
    "card":        "#132A1A",
    "card2":       "#1B3A24",
    "border":      "#2D6A4F",
    "green_dark":  "#1B4332",
    "green_mid":   "#2D6A4F",
    "green_light": "#40916C",
    "green_pale":  "#74C69D",
    "orange":      "#F77F00",
    "orange_light":"#FCBF49",
    "orange_dark": "#E85D04",
    "text":        "#E9F5EC",
    "text_muted":  "#95B8A0",
    "white":       "#FFFFFF",
    "red":         "#E63946",
    "gain":        "#52B788",
    "loss":        "#E63946",
}

CHART_COLORS = [
    "#F77F00","#40916C","#FCBF49",
    "#74C69D","#E85D04","#2D6A4F",
    "#FFD166","#06D6A0","#EF476F"
]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* {{ font-family: 'Inter', sans-serif !important; }}
.main {{ background-color: {C['bg']}; }}
.block-container {{
    padding: 1.2rem 2rem 2rem 2rem;
    max-width: 100% !important;
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #071410 0%, #0D2018 50%, #071410 100%);
    border-right: 1px solid {C['border']};
    min-width: 260px !important;
    max-width: 280px !important;
}}
section[data-testid="stSidebar"] * {{
    color: {C['text']} !important;
}}
button[data-testid="collapsedControl"] {{
    background: {C['orange']} !important;
    border-radius: 50% !important;
    border: 2px solid {C['orange_dark']} !important;
    box-shadow: 0 4px 12px rgba(247,127,0,0.5) !important;
    color: white !important;
}}
button[data-testid="collapsedControl"]:hover {{
    background: {C['orange_dark']} !important;
    transform: scale(1.1) !important;
    box-shadow: 0 6px 16px rgba(247,127,0,0.7) !important;
}}
button[data-testid="collapsedControl"] svg {{
    fill: white !important;
    color: white !important;
    stroke: white !important;
}}
[data-testid="stSidebarCollapseButton"] button {{
    background: {C['orange']} !important;
    border-radius: 50% !important;
    border: 2px solid {C['orange_dark']} !important;
    box-shadow: 0 4px 12px rgba(247,127,0,0.4) !important;
}}
[data-testid="stSidebarCollapseButton"] button:hover {{
    background: {C['orange_dark']} !important;
    transform: scale(1.1) !important;
}}
[data-testid="stSidebarCollapseButton"] svg {{
    fill: white !important;
    color: white !important;
    stroke: white !important;
}}
[data-testid="metric-container"] {{
    background: linear-gradient(135deg, {C['card']} 0%, {C['card2']} 100%);
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}}
[data-testid="metric-container"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(247,127,0,0.2);
    border-color: {C['orange']};
}}
[data-testid="stMetricLabel"] {{
    color: {C['text_muted']} !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}}
[data-testid="stMetricValue"] {{
    color: {C['orange']} !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricDelta"] {{
    color: {C['green_pale']} !important;
    font-size: 0.78rem !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid {C['border']};
    border-radius: 10px;
    overflow: hidden;
}}
hr {{ border-color: {C['border']} !important; opacity: 0.4; }}
.stTabs [data-baseweb="tab-list"] {{
    background: {C['card']};
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {C['text_muted']};
    border-radius: 8px;
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {C['orange_dark']}, {C['orange']}) !important;
    color: white !important;
}}
.dash-header {{
    background: linear-gradient(135deg, {C['green_dark']} 0%, {C['green_mid']} 60%, {C['orange_dark']}22 100%);
    border: 1px solid {C['border']};
    border-left: 5px solid {C['orange']};
    border-radius: 14px;
    padding: 1.2rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}}
.kpi-section-title {{
    color: {C['orange']};
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}}
.badge {{
    display: inline-block;
    background: {C['orange']}22;
    color: {C['orange']};
    border: 1px solid {C['orange']}66;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
}}
.badge-green {{
    background: {C['green_light']}22;
    color: {C['green_pale']};
    border: 1px solid {C['green_light']}66;
}}
.info-card {{
    background: linear-gradient(135deg, {C['card']} 0%, {C['card2']} 100%);
    border: 1px solid {C['border']};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
}}
.checklist-item {{
    background: {C['card2']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.3rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}}
.tcode {{
    background: {C['orange']}22;
    color: {C['orange']};
    border: 1px solid {C['orange']}55;
    border-radius: 5px;
    padding: 1px 7px;
    font-size: 0.7rem;
    font-weight: 700;
    font-family: monospace !important;
}}
.sidebar-logo {{
    background: linear-gradient(135deg, {C['orange_dark']}, {C['orange']});
    border-radius: 10px;
    padding: 0.8rem 1rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(247,127,0,0.3);
}}
.stat-row {{
    display: flex;
    justify-content: space-between;
    background: {C['card2']};
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin: 0.25rem 0;
    border-left: 3px solid {C['orange']};
}}
button[data-testid="collapsedControl"] span {{
    font-size: 0 !important;
    width: 0 !important;
}}
[data-testid="stSidebarCollapseButton"] span {{
    font-size: 0 !important;
    width: 0 !important;
}}
button[data-testid="collapsedControl"] {{
    background: #F77F00 !important;
    border-radius: 50% !important;
    border: 2px solid #E85D04 !important;
    width: 2rem !important;
    height: 2rem !important;
}}
[data-testid="stSidebarCollapseButton"] button {{
    background: #F77F00 !important;
    border-radius: 50% !important;
    border: 2px solid #E85D04 !important;
}}

button[data-testid="collapsedControl"] span,
[data-testid="stSidebarCollapseButton"] span {
    font-size: 0px !important;
    line-height: 0px !important;
    visibility: hidden !important;
    width: 0px !important;
    height: 0px !important;
    display: none !important;
}
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] button {
    background-color: #F77F00 !important;
    border-radius: 50% !important;
    border: 2px solid #E85D04 !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    gl  = pd.read_csv("transactions/gl_journal_entries.csv")
    ap  = pd.read_csv("transactions/vendor_invoices.csv")
    ar  = pd.read_csv("transactions/customer_invoices.csv")
    co  = pd.read_csv("transactions/cost_allocations.csv")
    dep = pd.read_csv("transactions/depreciation.csv")
    fx  = pd.read_csv("transactions/fx_revaluation.csv")
    coa = pd.read_csv("master_data/chart_of_accounts.csv")
    vm  = pd.read_csv("master_data/vendor_master.csv")
    cm  = pd.read_csv("master_data/customer_master.csv")
    cc  = pd.read_csv("master_data/cost_centers.csv")
    for df, cols in [
        (gl, ["Posting_Date"]),
        (ap, ["Posting_Date","Due_Date"]),
        (ar, ["Posting_Date","Due_Date"]),
        (co, ["Posting_Date"]),
    ]:
        for col in cols:
            df[col] = pd.to_datetime(df[col])
    return gl, ap, ar, co, dep, fx, coa, vm, cm, cc

gl, ap, ar, co, dep, fx, coa, vm, cm, cc = load_data()
REPORT_DATE = datetime(2024, 5, 31)

def chart_layout(fig, height=380, show_legend=True):
    fig.update_layout(
        height=height,
        plot_bgcolor=C["card"], paper_bgcolor=C["card"],
        font=dict(family="Inter", color=C["text"], size=11),
        legend=dict(
            bgcolor=C["card2"], bordercolor=C["border"], borderwidth=1,
            font=dict(color=C["text"]),
            orientation="h", yanchor="bottom", y=1.02
        ) if show_legend else dict(visible=False),
        xaxis=dict(gridcolor=C["border"], gridwidth=0.5,
                   linecolor=C["border"], tickfont=dict(color=C["text_muted"])),
        yaxis=dict(gridcolor=C["border"], gridwidth=0.5,
                   linecolor=C["border"], tickfont=dict(color=C["text_muted"])),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def aging_bucket(d):
    if d <= 0:    return "Not Yet Due"
    elif d <= 30: return "1-30 Days"
    elif d <= 60: return "31-60 Days"
    else:         return "61-90 Days"

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class='sidebar-logo'>
        <div style='font-size:1.4rem;font-weight:800;color:white;letter-spacing:0.05em'>
            🌿 SAP FI/CO
        </div>
        <div style='font-size:0.72rem;color:white;opacity:0.85;margin-top:2px'>
            S/4HANA Simulation
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='info-card'>
        <div style='font-size:0.7rem;color:{C["text_muted"]};text-transform:uppercase;
                    letter-spacing:0.08em;font-weight:600'>Company</div>
        <div style='font-size:0.95rem;color:{C["text"]};font-weight:600;margin-top:2px'>
            PrecisionParts Pvt. Ltd.
        </div>
        <div style='margin-top:8px;display:flex;gap:6px;flex-wrap:wrap'>
            <span class='badge'>IN01</span>
            <span class='badge'>FY2024</span>
            <span class='badge-green'>Apr 2024</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Executive Overview",
        "📒  GL & Trial Balance",
        "📦  Accounts Payable",
        "💰  Accounts Receivable",
        "🏭  Cost Center Accounting",
        "📅  Month-End Close",
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:0.68rem;color:{C["text_muted"]};text-transform:uppercase;
                letter-spacing:0.1em;font-weight:600;margin-bottom:6px'>
        Modules Active
    </div>
    """, unsafe_allow_html=True)
    for mod, desc in [("FI-GL","General Ledger"),("FI-AP","Accounts Payable"),
                       ("FI-AR","Accounts Receivable"),("CO-CCA","Cost Centers"),
                       ("FI-AA","Asset Accounting"),("FI-FX","FX Revaluation")]:
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
                    padding:4px 0;border-bottom:1px solid {C["border"]}33'>
            <span style='font-size:0.72rem;color:{C["orange"]};font-weight:700'>{mod}</span>
            <span style='font-size:0.68rem;color:{C["text_muted"]}'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "🏠  Executive Overview":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
                <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>
                    🏠 Executive Financial Overview
                </div>
                <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
                    PrecisionParts Pvt. Ltd. &nbsp;|&nbsp; Company Code: IN01 &nbsp;|&nbsp; April 2024
                </div>
            </div>
            <div><span class='badge'>Period 1</span>&nbsp;<span class='badge-green'>✔ LIVE</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_revenue   = ar["Invoice_Amount"].sum()
    total_collected = ar["Payment_Amount"].sum()
    total_ar_out    = ar["Outstanding_Amount"].sum()
    total_ap_out    = ap["Outstanding_Amount"].sum()
    total_expenses  = gl[(gl["Debit_Amount"]>0) &
                         (gl["GL_Account"].between(300000,399999))]["Debit_Amount"].sum()
    dep_total  = dep["Current_Period_Dep"].sum()
    fx_gain    = fx["FX_Gain_Loss"].sum()
    net_profit = total_revenue - total_expenses - dep_total + fx_gain
    coll_rate  = (total_collected / total_revenue * 100) if total_revenue else 0

    st.markdown(f"<div class='kpi-section-title'>📊 Key Financial Indicators — T-Code: F.01</div>",
                unsafe_allow_html=True)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("💹 Revenue",         f"₹{total_revenue/1e6:.2f}M",   "April 2024")
    c2.metric("📉 Expenses",        f"₹{(total_expenses+dep_total)/1e6:.2f}M","incl. Dep")
    c3.metric("📊 Net Profit/Loss", f"₹{net_profit/1e3:.1f}K",      "+FX Adj")
    c4.metric("💱 FX Gain",         f"₹{fx_gain:,.0f}",             "F.05 Net")
    c5.metric("⚙️ Total Assets",    "₹7.37M",                       "Balance Sheet")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi-section-title'>⚡ Liquidity & Working Capital</div>",
                unsafe_allow_html=True)
    c6,c7,c8,c9 = st.columns(4)
    c6.metric("📥 AR Outstanding",  f"₹{total_ar_out/1e6:.2f}M", "4 customers")
    c7.metric("📤 AP Outstanding",  f"₹{total_ap_out/1e6:.2f}M", "3 vendors")
    c8.metric("💰 Collection Rate", f"{coll_rate:.1f}%",          "vs invoiced")
    c9.metric("🏦 Cash & Bank",     "₹5.64M",                    "GL: 100100")

    st.markdown("---")
    col_a, col_b = st.columns([3,2])
    with col_a:
        st.markdown(f"### 📊 Revenue vs Expenses")
        st.markdown(f"<span class='tcode'>F.01</span>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Revenue", x=["April 2024"], y=[total_revenue],
            marker_color=C["green_light"],
            text=[f"₹{total_revenue:,.0f}"], textposition="outside",
            textfont=dict(color=C["green_pale"],size=12)))
        fig.add_trace(go.Bar(name="Expenses", x=["April 2024"],
            y=[total_expenses+dep_total], marker_color=C["orange"],
            text=[f"₹{(total_expenses+dep_total):,.0f}"], textposition="outside",
            textfont=dict(color=C["orange_light"],size=12)))
        fig.add_trace(go.Bar(name="Net P/L", x=["April 2024"],
            y=[abs(net_profit)],
            marker_color=C["red"] if net_profit<0 else C["gain"],
            text=[f"₹{net_profit:,.0f}"], textposition="outside",
            textfont=dict(color=C["text_muted"],size=12)))
        chart_layout(fig, height=360)
        fig.update_layout(barmode="group", yaxis_title="Amount (INR)")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("### 🥧 Expense Split")
        st.markdown(f"<span class='tcode'>KSB1</span>", unsafe_allow_html=True)
        exp_data = gl[gl["GL_Account"].between(300000,399999)].groupby(
            "Account_Description")["Debit_Amount"].sum().reset_index()
        dep_row = pd.DataFrame([{"Account_Description":"Depreciation","Debit_Amount":dep_total}])
        exp_data = pd.concat([exp_data, dep_row], ignore_index=True)
        fig_pie = px.pie(exp_data, values="Debit_Amount", names="Account_Description",
                         color_discrete_sequence=CHART_COLORS, hole=0.5)
        fig_pie.update_traces(textfont_color="white",
                              marker=dict(line=dict(color=C["bg"],width=2)))
        fig_pie.update_layout(height=360, paper_bgcolor=C["card"], plot_bgcolor=C["card"],
                               font=dict(family="Inter",color=C["text"]),
                               legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                           font=dict(color=C["text"],size=10)),
                               annotations=[dict(text="Expenses",x=0.5,y=0.5,
                                                  showarrow=False,
                                                  font=dict(size=13,color=C["text_muted"]),
                                                  xref="paper",yref="paper")])
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown("### 📥 AR Outstanding by Customer")
        st.markdown(f"<span class='tcode'>FBL5N</span>", unsafe_allow_html=True)
        ar_cust = ar[ar["Outstanding_Amount"]>0].groupby(
            "Customer_Name")["Outstanding_Amount"].sum().reset_index()
        ar_cust = ar_cust.sort_values("Outstanding_Amount", ascending=True)
        fig_ar = go.Figure(go.Bar(
            x=ar_cust["Outstanding_Amount"], y=ar_cust["Customer_Name"],
            orientation="h",
            marker=dict(color=ar_cust["Outstanding_Amount"],
                        colorscale=[[0,C["green_mid"]],[0.5,C["orange"]],[1.0,C["orange_dark"]]],
                        showscale=False),
            text=[f"₹{v:,.0f}" for v in ar_cust["Outstanding_Amount"]],
            textposition="outside", textfont=dict(color=C["text_muted"],size=11)))
        chart_layout(fig_ar, height=300, show_legend=False)
        fig_ar.update_layout(xaxis_title="Outstanding (INR)", yaxis_title="")
        st.plotly_chart(fig_ar, use_container_width=True)

    with col_d:
        st.markdown("### 📤 AP Outstanding by Vendor")
        st.markdown(f"<span class='tcode'>FBL1N</span>", unsafe_allow_html=True)
        ap_vend = ap[ap["Outstanding_Amount"]>0].groupby(
            "Vendor_Name")["Outstanding_Amount"].sum().reset_index()
        ap_vend = ap_vend.sort_values("Outstanding_Amount", ascending=True)
        fig_ap = go.Figure(go.Bar(
            x=ap_vend["Outstanding_Amount"], y=ap_vend["Vendor_Name"],
            orientation="h",
            marker=dict(color=ap_vend["Outstanding_Amount"],
                        colorscale=[[0,C["green_dark"]],[0.5,C["orange_dark"]],[1.0,C["orange"]]],
                        showscale=False),
            text=[f"₹{v:,.0f}" for v in ap_vend["Outstanding_Amount"]],
            textposition="outside", textfont=dict(color=C["text_muted"],size=11)))
        chart_layout(fig_ap, height=300, show_legend=False)
        fig_ap.update_layout(xaxis_title="Outstanding (INR)", yaxis_title="")
        st.plotly_chart(fig_ap, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — GL & TRIAL BALANCE
# ══════════════════════════════════════════════════════════════
elif page == "📒  GL & Trial Balance":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>📒 General Ledger & Trial Balance</div>
        <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
            <span class='tcode'>FB50</span>&nbsp;
            <span class='tcode'>FS10N</span>&nbsp;
            <span class='tcode'>S_ALR_87012284</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    gl_summary = gl.groupby(["GL_Account","Account_Description"]).agg(
        Total_Debit=("Debit_Amount","sum"),
        Total_Credit=("Credit_Amount","sum")).reset_index()
    gl_summary["Net_Balance"] = gl_summary["Total_Debit"] - gl_summary["Total_Credit"]
    gl_summary = pd.merge(gl_summary, coa[["GL_Account","Account_Type","Account_Group"]],
                          on="GL_Account", how="left")
    total_dr = gl_summary["Total_Debit"].sum()
    total_cr = gl_summary["Total_Credit"].sum()

    c1,c2,c3 = st.columns(3)
    c1.metric("📊 Total Debits",  f"₹{total_dr/1e6:.3f}M")
    c2.metric("📊 Total Credits", f"₹{total_cr/1e6:.3f}M")
    c3.metric("⚖️ Difference",    f"₹{(total_dr-total_cr):,.0f}",
              "✅ BALANCED" if total_dr==total_cr else "❌ NOT BALANCED")

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📋 Trial Balance","📊 Account Analysis","📜 Document Log"])

    with tab1:
        col_a, col_b = st.columns([3,2])
        with col_a:
            st.markdown(f"#### Trial Balance &nbsp;<span class='tcode'>S_ALR_87012284</span>",
                        unsafe_allow_html=True)
            display_tb = gl_summary[["GL_Account","Account_Description","Account_Type",
                                      "Total_Debit","Total_Credit","Net_Balance"]].copy()
            display_tb.columns = ["GL Acct","Description","Type","Debit (₹)","Credit (₹)","Net (₹)"]
            st.dataframe(display_tb.style
                .format({"Debit (₹)":"{:,.0f}","Credit (₹)":"{:,.0f}","Net (₹)":"{:,.0f}"}),
                use_container_width=True, height=400)

        with col_b:
            st.markdown(f"#### Balance by Account Type &nbsp;<span class='tcode'>FS10N</span>",
                        unsafe_allow_html=True)
            type_sum = gl_summary.groupby("Account_Type")["Net_Balance"].sum().reset_index()
            fig_type = go.Figure(go.Bar(
                x=type_sum["Account_Type"], y=type_sum["Net_Balance"],
                marker=dict(color=[C["orange"] if v>0 else C["green_light"]
                                   for v in type_sum["Net_Balance"]],
                            line=dict(color=C["bg"],width=1.5)),
                text=[f"₹{v:,.0f}" for v in type_sum["Net_Balance"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            chart_layout(fig_type, height=400, show_legend=False)
            fig_type.update_layout(yaxis_title="Net Balance (INR)")
            st.plotly_chart(fig_type, use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### Debit vs Credit by GL Account")
            top_accts = gl_summary.nlargest(8,"Total_Debit")
            fig_dvcr = go.Figure()
            fig_dvcr.add_trace(go.Bar(name="Debit",
                x=top_accts["Account_Description"], y=top_accts["Total_Debit"],
                marker_color=C["orange"], marker_line_color=C["bg"], marker_line_width=1.5))
            fig_dvcr.add_trace(go.Bar(name="Credit",
                x=top_accts["Account_Description"], y=top_accts["Total_Credit"],
                marker_color=C["green_light"], marker_line_color=C["bg"], marker_line_width=1.5))
            chart_layout(fig_dvcr, height=380)
            fig_dvcr.update_layout(barmode="group",
                                    xaxis_tickangle=-30, yaxis_title="Amount (INR)")
            st.plotly_chart(fig_dvcr, use_container_width=True)

        with col_d:
            st.markdown("#### GL Distribution by Account Group")
            grp = gl_summary.groupby("Account_Group")["Total_Debit"].sum().reset_index()
            fig_grp = px.pie(grp, values="Total_Debit", names="Account_Group",
                             color_discrete_sequence=CHART_COLORS, hole=0.45)
            fig_grp.update_traces(textfont_color="white",
                                   marker=dict(line=dict(color=C["bg"],width=2)))
            fig_grp.update_layout(height=380, paper_bgcolor=C["card"],
                                   font=dict(family="Inter",color=C["text"]),
                                   legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                               font=dict(color=C["text"],size=10)))
            st.plotly_chart(fig_grp, use_container_width=True)

    with tab3:
        st.markdown(f"#### All GL Documents &nbsp;<span class='tcode'>FB50</span>",
                    unsafe_allow_html=True)
        gl_disp = gl[["Doc_Number","Posting_Date","T_Code","GL_Account",
                       "Account_Description","Debit_Amount","Credit_Amount","Reference"]].copy()
        gl_disp.columns = ["Doc No","Date","T-Code","GL Acct","Description",
                            "Debit (₹)","Credit (₹)","Reference"]
        st.dataframe(gl_disp.style.format({"Debit (₹)":"{:,.0f}","Credit (₹)":"{:,.0f}"}),
                     use_container_width=True, height=420)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — ACCOUNTS PAYABLE
# ══════════════════════════════════════════════════════════════
elif page == "📦  Accounts Payable":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>📦 Accounts Payable — FI-AP</div>
        <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
            <span class='tcode'>FB60</span>&nbsp;
            <span class='tcode'>F110</span>&nbsp;
            <span class='tcode'>FBL1N</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📋 Total Invoices", f"{len(ap)}")
    c2.metric("💵 Total Invoiced", f"₹{ap['Invoice_Amount'].sum()/1e6:.3f}M")
    c3.metric("✅ Total Paid",     f"₹{ap['Payment_Amount'].sum():,.0f}")
    c4.metric("⏳ Outstanding",    f"₹{ap['Outstanding_Amount'].sum():,.0f}")

    st.markdown("---")
    open_ap = ap[ap["Outstanding_Amount"]>0].copy()
    open_ap["Days_Overdue"] = (REPORT_DATE - open_ap["Due_Date"]).dt.days
    open_ap["Aging_Bucket"] = open_ap["Days_Overdue"].apply(aging_bucket)
    aging_colors = {"Not Yet Due":C["green_light"],"1-30 Days":C["orange_light"],
                    "31-60 Days":C["orange"],"61-90 Days":C["orange_dark"]}

    tab1, tab2 = st.tabs(["📊 Analytics","📋 Invoice Register"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### ⏰ AP Aging Buckets &nbsp;<span class='tcode'>FBL1N</span>",
                        unsafe_allow_html=True)
            aging_sum = open_ap.groupby("Aging_Bucket")["Outstanding_Amount"].sum().reset_index()
            fig_aging = go.Figure(go.Bar(
                x=aging_sum["Aging_Bucket"], y=aging_sum["Outstanding_Amount"],
                marker_color=[aging_colors.get(b,C["orange"]) for b in aging_sum["Aging_Bucket"]],
                marker_line_color=C["bg"], marker_line_width=2,
                text=[f"₹{v:,.0f}" for v in aging_sum["Outstanding_Amount"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            chart_layout(fig_aging, show_legend=False)
            fig_aging.update_layout(yaxis_title="Outstanding (INR)")
            st.plotly_chart(fig_aging, use_container_width=True)

        with col_b:
            st.markdown(f"#### 🏭 Vendor Balance Overview &nbsp;<span class='tcode'>FBL1N</span>",
                        unsafe_allow_html=True)
            vend_out = ap.groupby("Vendor_Name").agg(
                Invoiced=("Invoice_Amount","sum"),
                Paid=("Payment_Amount","sum"),
                Outstanding=("Outstanding_Amount","sum")).reset_index()
            fig_vend = go.Figure()
            fig_vend.add_trace(go.Bar(name="Invoiced",
                x=vend_out["Vendor_Name"], y=vend_out["Invoiced"],
                marker_color=C["green_mid"], marker_line_color=C["bg"], marker_line_width=1.5))
            fig_vend.add_trace(go.Bar(name="Paid",
                x=vend_out["Vendor_Name"], y=vend_out["Paid"],
                marker_color=C["green_pale"], marker_line_color=C["bg"], marker_line_width=1.5))
            fig_vend.add_trace(go.Bar(name="Outstanding",
                x=vend_out["Vendor_Name"], y=vend_out["Outstanding"],
                marker_color=C["orange"], marker_line_color=C["bg"], marker_line_width=1.5))
            chart_layout(fig_vend)
            fig_vend.update_layout(barmode="group", yaxis_title="INR")
            st.plotly_chart(fig_vend, use_container_width=True)

        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### 🥧 Outstanding Distribution by Vendor")
            fig_vp = px.pie(vend_out[vend_out["Outstanding"]>0],
                            values="Outstanding", names="Vendor_Name",
                            color_discrete_sequence=CHART_COLORS, hole=0.5)
            fig_vp.update_traces(textfont_color="white",
                                  marker=dict(line=dict(color=C["bg"],width=2)))
            fig_vp.update_layout(height=320, paper_bgcolor=C["card"],
                                  font=dict(family="Inter",color=C["text"]),
                                  legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                              font=dict(color=C["text"],size=10)))
            st.plotly_chart(fig_vp, use_container_width=True)

        with col_d:
            st.markdown(f"#### 💳 Payment Run Summary &nbsp;<span class='tcode'>F110</span>",
                        unsafe_allow_html=True)
            paid = ap[ap["Payment_Amount"]>0]
            for _, row in paid.iterrows():
                st.markdown(f"""
                <div class='stat-row'>
                    <div>
                        <div style='font-size:0.82rem;color:{C["text"]};font-weight:600'>
                            {row["Vendor_Name"]}
                        </div>
                        <div style='font-size:0.7rem;color:{C["text_muted"]}'>
                            Doc: {row["Doc_Number"]} &nbsp;|&nbsp; {str(row["Payment_Date"])[:10]}
                        </div>
                    </div>
                    <div style='font-size:0.95rem;color:{C["gain"]};font-weight:700'>
                        ₹{row["Payment_Amount"]:,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='text-align:right;margin-top:8px;font-size:0.82rem;
                        color:{C["orange"]};font-weight:700'>
                Total Paid: ₹{paid["Payment_Amount"].sum():,.0f}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"#### All Vendor Invoices &nbsp;<span class='tcode'>FB60</span>",
                    unsafe_allow_html=True)
        ap_d = ap[["Doc_Number","Posting_Date","Due_Date","Vendor_ID","Vendor_Name",
                    "Invoice_Amount","Payment_Amount","Outstanding_Amount","T_Code"]].copy()
        ap_d.columns = ["Doc No","Post Date","Due Date","Vendor ID","Vendor Name",
                         "Invoice (₹)","Paid (₹)","Outstanding (₹)","T-Code"]
        st.dataframe(ap_d.style.format({"Invoice (₹)":"{:,.0f}","Paid (₹)":"{:,.0f}",
                                         "Outstanding (₹)":"{:,.0f}"}),
                     use_container_width=True, height=350)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — ACCOUNTS RECEIVABLE
# ══════════════════════════════════════════════════════════════
elif page == "💰  Accounts Receivable":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>💰 Accounts Receivable — FI-AR</div>
        <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
            <span class='tcode'>FB70</span>&nbsp;
            <span class='tcode'>F-28</span>&nbsp;
            <span class='tcode'>FBL5N</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    total_inv = ar["Invoice_Amount"].sum()
    total_rec = ar["Payment_Amount"].sum()
    total_out = ar["Outstanding_Amount"].sum()
    coll_rate = (total_rec/total_inv*100) if total_inv else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("📋 Invoices",       f"{len(ar)}")
    c2.metric("💵 Total Invoiced", f"₹{total_inv/1e6:.3f}M")
    c3.metric("✅ Collected",      f"₹{total_rec:,.0f}")
    c4.metric("📈 Collection Rate",f"{coll_rate:.1f}%")

    st.markdown("---")
    open_ar = ar[ar["Outstanding_Amount"]>0].copy()
    open_ar["Days_Overdue"] = (REPORT_DATE - open_ar["Due_Date"]).dt.days
    open_ar["Aging_Bucket"] = open_ar["Days_Overdue"].apply(aging_bucket)
    aging_colors = {"Not Yet Due":C["green_light"],"1-30 Days":C["orange_light"],
                    "31-60 Days":C["orange"],"61-90 Days":C["orange_dark"]}

    tab1, tab2 = st.tabs(["📊 Analytics","📋 Customer Register"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### ⏰ AR Aging Report &nbsp;<span class='tcode'>FBL5N</span>",
                        unsafe_allow_html=True)
            aging_sum = open_ar.groupby("Aging_Bucket")["Outstanding_Amount"].sum().reset_index()
            fig_ag = go.Figure(go.Bar(
                x=aging_sum["Aging_Bucket"], y=aging_sum["Outstanding_Amount"],
                marker_color=[aging_colors.get(b,C["orange"]) for b in aging_sum["Aging_Bucket"]],
                marker_line_color=C["bg"], marker_line_width=2,
                text=[f"₹{v:,.0f}" for v in aging_sum["Outstanding_Amount"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            chart_layout(fig_ag, show_legend=False)
            fig_ag.update_layout(yaxis_title="Outstanding (INR)")
            st.plotly_chart(fig_ag, use_container_width=True)

        with col_b:
            st.markdown("#### 🎯 Collection Efficiency Gauge")
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number+delta", value=coll_rate,
                delta={"reference":80,"valueformat":".1f",
                       "increasing":{"color":C["gain"]},"decreasing":{"color":C["loss"]}},
                title={"text":"Collection Rate (%)","font":{"size":15,"color":C["text"]}},
                number={"font":{"size":40,"color":C["orange"]},"suffix":"%"},
                gauge={"axis":{"range":[0,100],"tickfont":{"color":C["text_muted"]}},
                       "bar":{"color":C["orange"],"thickness":0.25},
                       "bgcolor":C["card2"],"bordercolor":C["border"],
                       "steps":[{"range":[0,40],"color":C["green_dark"]},
                                 {"range":[40,70],"color":C["green_mid"]},
                                 {"range":[70,100],"color":C["green_light"]}],
                       "threshold":{"line":{"color":C["orange_light"],"width":3},
                                    "thickness":0.75,"value":80}}))
            fig_g.update_layout(height=380, paper_bgcolor=C["card"],
                                 font=dict(family="Inter"))
            st.plotly_chart(fig_g, use_container_width=True)

        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### 👥 Invoice vs Collection by Customer")
            cust_sum = ar.groupby("Customer_Name").agg(
                Invoiced=("Invoice_Amount","sum"),
                Collected=("Payment_Amount","sum"),
                Outstanding=("Outstanding_Amount","sum")).reset_index()
            fig_cs = go.Figure()
            fig_cs.add_trace(go.Bar(name="Invoiced",
                x=cust_sum["Customer_Name"], y=cust_sum["Invoiced"],
                marker_color=C["green_mid"], marker_line_color=C["bg"], marker_line_width=1.5))
            fig_cs.add_trace(go.Bar(name="Collected",
                x=cust_sum["Customer_Name"], y=cust_sum["Collected"],
                marker_color=C["green_pale"], marker_line_color=C["bg"], marker_line_width=1.5))
            fig_cs.add_trace(go.Bar(name="Outstanding",
                x=cust_sum["Customer_Name"], y=cust_sum["Outstanding"],
                marker_color=C["orange"], marker_line_color=C["bg"], marker_line_width=1.5))
            chart_layout(fig_cs, height=340)
            fig_cs.update_layout(barmode="group", yaxis_title="INR")
            st.plotly_chart(fig_cs, use_container_width=True)

        with col_d:
            st.markdown("#### 🥧 Outstanding by Customer")
            fig_cp = px.pie(cust_sum[cust_sum["Outstanding"]>0],
                            values="Outstanding", names="Customer_Name",
                            color_discrete_sequence=CHART_COLORS, hole=0.5)
            fig_cp.update_traces(textfont_color="white",
                                  marker=dict(line=dict(color=C["bg"],width=2)))
            fig_cp.update_layout(height=340, paper_bgcolor=C["card"],
                                  font=dict(family="Inter",color=C["text"]),
                                  legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                              font=dict(color=C["text"],size=10)))
            st.plotly_chart(fig_cp, use_container_width=True)

    with tab2:
        st.markdown(f"#### All Customer Invoices &nbsp;<span class='tcode'>FB70 / F-28</span>",
                    unsafe_allow_html=True)
        ar_d = ar[["Doc_Number","Customer_Name","Invoice_Amount",
                    "Payment_Amount","Outstanding_Amount","Due_Date"]].copy()
        ar_d.columns = ["Doc No","Customer","Invoice (₹)","Received (₹)","Outstanding (₹)","Due Date"]
        st.dataframe(ar_d.style.format({"Invoice (₹)":"{:,.0f}","Received (₹)":"{:,.0f}",
                                         "Outstanding (₹)":"{:,.0f}"}),
                     use_container_width=True, height=380)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — COST CENTER ACCOUNTING
# ══════════════════════════════════════════════════════════════
elif page == "🏭  Cost Center Accounting":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>🏭 Cost Center Accounting — CO-CCA</div>
        <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
            <span class='tcode'>KSB1</span>&nbsp;
            <span class='tcode'>S_ALR_87013611</span>&nbsp;
            <span class='tcode'>KB11N</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    variance = co.groupby(["Cost_Center","Cost_Center_Name"]).agg(
        Total_Actual=("Actual_Amount","sum"),
        Total_Plan=("Plan_Amount","sum")).reset_index()
    variance["Variance"]   = variance["Total_Actual"] - variance["Total_Plan"]
    variance["Variance_%"] = ((variance["Variance"]/variance["Total_Plan"])*100).round(2)

    c1,c2,c3 = st.columns(3)
    c1.metric("💰 Total Actual",  f"₹{variance['Total_Actual'].sum():,.0f}")
    c2.metric("📋 Total Planned", f"₹{variance['Total_Plan'].sum():,.0f}")
    c3.metric("📊 Total Variance",f"₹{variance['Variance'].sum():,.0f}",
              "⚠️ Unfavourable" if variance["Variance"].sum()>0 else "✅ Favourable")

    st.markdown("---")
    tab1, tab2 = st.tabs(["📊 Variance Analysis","📜 Line Items"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### Actual vs Plan &nbsp;<span class='tcode'>S_ALR_87013611</span>",
                        unsafe_allow_html=True)
            fig_v = go.Figure()
            fig_v.add_trace(go.Bar(name="Actual",
                x=variance["Cost_Center_Name"], y=variance["Total_Actual"],
                marker_color=C["orange"], marker_line_color=C["bg"], marker_line_width=1.5,
                text=[f"₹{v:,.0f}" for v in variance["Total_Actual"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            fig_v.add_trace(go.Bar(name="Plan",
                x=variance["Cost_Center_Name"], y=variance["Total_Plan"],
                marker_color=C["green_light"], marker_line_color=C["bg"], marker_line_width=1.5,
                text=[f"₹{v:,.0f}" for v in variance["Total_Plan"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            chart_layout(fig_v)
            fig_v.update_layout(barmode="group",
                                 xaxis_title="Cost Center", yaxis_title="Amount (INR)")
            st.plotly_chart(fig_v, use_container_width=True)

        with col_b:
            st.markdown(f"#### Variance % &nbsp;<span class='tcode'>S_ALR_87013611</span>",
                        unsafe_allow_html=True)
            colors_v = [C["orange_dark"] if v>0 else C["gain"] for v in variance["Variance_%"]]
            fig_pct = go.Figure(go.Bar(
                x=variance["Cost_Center_Name"], y=variance["Variance_%"],
                marker_color=colors_v, marker_line_color=C["bg"], marker_line_width=1.5,
                text=[f"{v:+.2f}%" for v in variance["Variance_%"]],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            fig_pct.add_hline(y=0, line_dash="dash",
                               line_color=C["text_muted"], line_width=1)
            chart_layout(fig_pct, show_legend=False)
            fig_pct.update_layout(yaxis_title="Variance (%)")
            st.plotly_chart(fig_pct, use_container_width=True)

        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown("#### Cost Distribution by Center")
            fig_cc = px.pie(variance, values="Total_Actual", names="Cost_Center_Name",
                            color_discrete_sequence=[C["orange"],C["green_light"],C["green_pale"]],
                            hole=0.5)
            fig_cc.update_traces(textfont_color="white",
                                  marker=dict(line=dict(color=C["bg"],width=2)))
            fig_cc.update_layout(height=300, paper_bgcolor=C["card"],
                                  font=dict(family="Inter",color=C["text"]),
                                  legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                              font=dict(color=C["text"],size=10)))
            st.plotly_chart(fig_cc, use_container_width=True)

        with col_d:
            st.markdown("#### Variance Summary Table")
            var_d = variance[["Cost_Center_Name","Total_Actual","Total_Plan",
                               "Variance","Variance_%"]].copy()
            var_d.columns = ["Cost Center","Actual (₹)","Plan (₹)","Variance (₹)","Var %"]
            st.dataframe(var_d.style.format({"Actual (₹)":"{:,.0f}","Plan (₹)":"{:,.0f}",
                                              "Variance (₹)":"{:,.0f}","Var %":"{:+.2f}%"}),
                         use_container_width=True, height=200)

    with tab2:
        st.markdown(f"#### Cost Center Line Items &nbsp;<span class='tcode'>KSB1</span>",
                    unsafe_allow_html=True)
        co_d = co[["Doc_Number","Posting_Date","Cost_Center_Name",
                    "Description","Actual_Amount","Plan_Amount"]].copy()
        co_d["Variance"] = co_d["Actual_Amount"] - co_d["Plan_Amount"]
        co_d.columns = ["Doc No","Date","Cost Center","Description",
                         "Actual (₹)","Plan (₹)","Variance (₹)"]
        st.dataframe(co_d.style.format({"Actual (₹)":"{:,.0f}","Plan (₹)":"{:,.0f}",
                                         "Variance (₹)":"{:,.0f}"}),
                     use_container_width=True, height=400)


# ══════════════════════════════════════════════════════════════
# PAGE 6 — MONTH-END CLOSE
# ══════════════════════════════════════════════════════════════
elif page == "📅  Month-End Close":
    st.markdown(f"""
    <div class='dash-header'>
        <div style='font-size:1.5rem;font-weight:800;color:{C["white"]}'>📅 Month-End Closing Activities</div>
        <div style='font-size:0.85rem;color:{C["text_muted"]};margin-top:4px'>
            <span class='tcode'>AFAB</span>&nbsp;
            <span class='tcode'>F.05</span>&nbsp;
            <span class='tcode'>F.01</span>&nbsp;
            <span class='tcode'>OB52</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    dep_total  = dep["Current_Period_Dep"].sum()
    fx_gain    = fx["FX_Gain_Loss"].sum()
    revenue    = ar["Invoice_Amount"].sum()
    expenses   = (gl[gl["GL_Account"].between(300000,399999)]["Debit_Amount"].sum() + dep_total)
    net_profit = revenue - expenses + fx_gain

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("⚙️ Depreciation",   f"₹{dep_total:,.0f}", "AFAB — 3 assets")
    c2.metric("💱 FX Net Gain",    f"₹{fx_gain:,.0f}",   "F.05 Revaluation")
    c3.metric("📊 Net Profit/Loss",f"₹{net_profit:,.0f}","F.01 P&L")
    c4.metric("✅ Close Status",   "11/11 DONE",          "Period Closed OB52")

    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["📊 P&L & Balance Sheet","⚙️ Depreciation & FX","✅ Close Checklist"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### P&L Statement &nbsp;<span class='tcode'>F.01</span>",
                        unsafe_allow_html=True)
            pl_items = {
                "Sales Revenue":    revenue,
                "Raw Material":     gl[gl["GL_Account"]==300000]["Debit_Amount"].sum(),
                "Salaries & Wages": gl[gl["GL_Account"]==310000]["Debit_Amount"].sum(),
                "Rent Expense":     gl[gl["GL_Account"]==320000]["Debit_Amount"].sum(),
                "Depreciation":     dep_total,
                "Miscellaneous":    gl[gl["GL_Account"]==340000]["Debit_Amount"].sum(),
                "FX Gain":          fx_gain,
            }
            pl_colors = [C["green_light"] if k in ["Sales Revenue","FX Gain"]
                         else C["orange"] for k in pl_items.keys()]
            fig_pl = go.Figure(go.Bar(
                x=list(pl_items.keys()), y=list(pl_items.values()),
                marker_color=pl_colors, marker_line_color=C["bg"], marker_line_width=1.5,
                text=[f"₹{v:,.0f}" for v in pl_items.values()],
                textposition="outside", textfont=dict(color=C["text_muted"])))
            chart_layout(fig_pl, height=400, show_legend=False)
            fig_pl.update_layout(xaxis_title="", yaxis_title="Amount (INR)")
            st.plotly_chart(fig_pl, use_container_width=True)

        with col_b:
            st.markdown(f"#### Balance Sheet — Asset Mix &nbsp;<span class='tcode'>F.01</span>",
                        unsafe_allow_html=True)
            cash_bank = (gl[gl["GL_Account"]==100100]["Debit_Amount"].sum() -
                         gl[gl["GL_Account"]==100100]["Credit_Amount"].sum())
            fixed_net = dep["Acquisition_Value"].sum() - dep_total
            bs_assets = {"Cash & Bank": cash_bank,
                          "Accounts Receivable": ar["Outstanding_Amount"].sum(),
                          "Fixed Assets (Net)": fixed_net}
            fig_bs = px.pie(names=list(bs_assets.keys()),
                            values=list(bs_assets.values()),
                            title="Asset Composition",
                            color_discrete_sequence=[C["orange"],C["green_light"],C["green_pale"]],
                            hole=0.5)
            fig_bs.update_traces(textfont_color="white",
                                  marker=dict(line=dict(color=C["bg"],width=2)))
            fig_bs.update_layout(height=400, paper_bgcolor=C["card"],
                                  font=dict(family="Inter",color=C["text"]),
                                  title_font_color=C["text_muted"],
                                  legend=dict(bgcolor=C["card2"],bordercolor=C["border"],
                                              font=dict(color=C["text"],size=10)))
            st.plotly_chart(fig_bs, use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            st.markdown(f"#### Depreciation Schedule &nbsp;<span class='tcode'>AFAB</span>",
                        unsafe_allow_html=True)
            for _, row in dep.iterrows():
                pct = (row["Current_Period_Dep"] / row["Acquisition_Value"]) * 100
                st.markdown(f"""
                <div class='info-card'>
                    <div style='display:flex;justify-content:space-between;align-items:center'>
                        <div>
                            <div style='font-size:0.82rem;color:{C["text"]};font-weight:600'>
                                {row["Asset_No"]} — {row["Asset_Description"]}
                            </div>
                            <div style='font-size:0.7rem;color:{C["text_muted"]};margin-top:2px'>
                                Acq. Value: ₹{row["Acquisition_Value"]:,.0f}
                                &nbsp;|&nbsp; WDV: ₹{row["WDV"]:,.0f}
                            </div>
                        </div>
                        <div style='text-align:right'>
                            <div style='font-size:1rem;color:{C["orange"]};font-weight:700'>
                                ₹{row["Current_Period_Dep"]:,.0f}
                            </div>
                            <div style='font-size:0.68rem;color:{C["text_muted"]}'>
                                {pct:.3f}% dep.
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='margin-top:10px;padding:8px 12px;background:{C["green_dark"]};
                        border-radius:8px;border-left:4px solid {C["orange"]}'>
                <span style='color:{C["text_muted"]};font-size:0.75rem'>
                    GL Dr: 330000 (Dep. Expense) &nbsp;|&nbsp; Cr: 150100 (Acc. Dep.)
                </span><br>
                <span style='color:{C["orange"]};font-weight:700'>
                    Total Dep. Posted: ₹{dep_total:,.2f}
                </span>
            </div>
            """, unsafe_allow_html=True)

        with col_d:
            st.markdown(f"#### FX Revaluation &nbsp;<span class='tcode'>F.05</span>",
                        unsafe_allow_html=True)
            for _, row in fx.iterrows():
                gain = row["FX_Gain_Loss"] > 0
                st.markdown(f"""
                <div class='info-card' style='border-left:3px solid
                     {"#52B788" if gain else C["orange_dark"]}'>
                    <div style='font-size:0.82rem;color:{C["text"]};font-weight:600'>
                        {row["Description"]}
                    </div>
                    <div style='font-size:0.72rem;color:{C["text_muted"]};margin-top:4px'>
                        {row["Original_Currency"]} {row["Original_Amount"]:,.0f}
                        &nbsp;|&nbsp; Rate: {row["Exchange_Rate_Posting"]}
                        → {row["Exchange_Rate_Revaluation"]}
                    </div>
                    <div style='margin-top:6px;font-size:1rem;font-weight:700;
                                color:{"#52B788" if gain else C["orange_dark"]}'>
                        {"🟢 GAIN" if gain else "🔴 LOSS"}: ₹{abs(row["FX_Gain_Loss"]):,.0f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style='margin-top:10px;padding:8px 12px;background:{C["green_dark"]};
                        border-radius:8px;border-left:4px solid {C["gain"]}'>
                <span style='color:{C["gain"]};font-weight:700;font-size:0.9rem'>
                    ✅ Net FX Position: ₹{fx_gain:,.0f} GAIN
                </span>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown(f"#### Month-End Close Checklist &nbsp;<span class='tcode'>OB52</span>",
                    unsafe_allow_html=True)
        checklist = [
            ("GL Journal Entries Posted",     "FB50"),
            ("Vendor Invoices Processed",      "FB60"),
            ("Customer Invoices Processed",    "FB70"),
            ("Automatic Payment Run",          "F110"),
            ("Incoming Payments Posted",       "F-28"),
            ("Depreciation Run Executed",      "AFAB"),
            ("FX Revaluation Completed",       "F.05"),
            ("Cost Center Allocations Posted", "KB11N"),
            ("Trial Balance Verified",         "S_ALR_87012284"),
            ("Financial Statements Generated", "F.01"),
            ("Posting Period Closed",          "OB52"),
        ]
        col_e, col_f = st.columns(2)
        half = len(checklist)//2 + 1
        for activity, tcode in checklist[:half]:
            col_e.markdown(f"""
            <div class='checklist-item'>
                <span style='font-size:1rem'>✅</span>
                <span style='flex:1;font-size:0.83rem;color:{C["text"]}'>{activity}</span>
                <span class='tcode'>{tcode}</span>
            </div>
            """, unsafe_allow_html=True)
        for activity, tcode in checklist[half:]:
            col_f.markdown(f"""
            <div class='checklist-item'>
                <span style='font-size:1rem'>✅</span>
                <span style='flex:1;font-size:0.83rem;color:{C["text"]}'>{activity}</span>
                <span class='tcode'>{tcode}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-top:1.5rem;padding:1rem 1.5rem;
                    background:linear-gradient(135deg,{C["green_dark"]},{C["green_mid"]});
                    border-radius:12px;border:1px solid {C["green_light"]};
                    text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3)'>
            <div style='font-size:1.2rem;font-weight:800;color:{C["orange"]}'>
                🎉 PERIOD 1 — APRIL 2024 FULLY CLOSED
            </div>
            <div style='font-size:0.8rem;color:{C["text_muted"]};margin-top:4px'>
                11/11 Activities Complete &nbsp;|&nbsp;
                Company Code IN01 &nbsp;|&nbsp;
                Posting Period Locked via OB52
            </div>
        </div>
        """, unsafe_allow_html=True)
