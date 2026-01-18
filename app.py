import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    /* Deep Dark Background */
    .stApp { background-color: #0E1117; color: white; }
    
    /* Stylized Metric Cards */
    .metric-card { 
        background-color: #1F2937; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Adjusting Plotly chart background */
    .js-plotly-plot .plotly .bg { fill-opacity: 0; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v3.1 Final Demo")
    st.divider()
    
    # NAVIGATION MENU
    page = st.radio("Select Module", [
        "🛡️ Revenue Shield", 
        "👻 Ghost Hunter (Retention)", 
        "📊 Unified Data (LTV)"
    ])
    
    st.divider()
    st.info("Simulation Mode: ON")

# ==========================================
# MODULE 1: REVENUE SHIELD
# ==========================================
if page == "🛡️ Revenue Shield":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Revenue Shield")
        st.caption("Active Protection • Dispute Auto-Response")
    with col2:
        st.metric("ROI Multiplier", "12.4x")
    st.divider()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Disputes Defended", "14", "+2 Today")
    m2.metric("Revenue Saved", "$14,250", "+$1,200")
    m3.metric("Tax Risk (DE)", "High", "Action Required")
    
    st.subheader("Recent Defense Logs")
    st.dataframe(pd.DataFrame([
        {"Time": "10:42 AM", "Event": "Auto-Dispute (#994)", "Outcome": "Evidence Sent"},
        {"Time": "09:15 AM", "Event": "Fraud Block (IP 192..)", "Outcome": "Blocked"},
    ]), use_container_width=True, hide_index=True)

# ==========================================
# MODULE 2: GHOST HUNTER
# ==========================================
elif page == "👻 Ghost Hunter (Retention)":
    st.title("Ghost Hunter AI")
    st.caption("Predictive Churn Detection")
    st.divider()
    
    st.info("🤖 **AI Analysis:** Scanned 450 members. Detected **5 High-Risk users**.")
    
    risk_data = [
        {"User": "@CryptoKing_99", "Last Active": "12 Days Ago", "Health Score": 15, "LTV": "$450"},
        {"User": "Sarah_Designs", "Last Active": "8 Days Ago", "Health Score": 22, "LTV": "$120"},
        {"User": "MikeTrading", "Last Active": "9 Days Ago", "Health Score": 18, "LTV": "$890"},
    ]
    
    st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True, column_config={
        "Health Score": st.column_config.ProgressColumn("Health Score", min_value=0, max_value=100)
    })
    
    if st.button("🚀 Auto-Send Recovery DMs"):
        st.toast("Messages Sent!", icon="✅")

# ==========================================
# MODULE 3: UNIFIED LTV (Redesigned)
# ==========================================
elif page == "📊 Unified Data (LTV)":
    st.title("Profit Command Center")
    st.caption("Visualizing the Customer Journey & Drop-offs")
    st.divider()
    
    # 1. THE BIG NUMBERS
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Blended ROAS", "3.2x")
    with c2: st.metric("Customer LTV", "$145.00", "+$12")
    with c3: st.metric("CAC", "$42.00", "-$3")
    with c4: st.metric("Net Profit/User", "$103.00")
    
    st.divider()
    
    # 2. THE NEW & IMPROVED MONEY FLOW MAP
    st.subheader("💰 The Money Flow Map")
    
    # --- SANKEY DIAGRAM CONFIGURATION ---
    
    # 1. Define Nodes (Labels now include totals for clarity)
    labels = [
        "Ads (Meta): 5k", "Ads (TikTok): 3k", "Organic (YouTube): 8k",  # 0, 1, 2 (Sources)
        "Landing Page: 16k",                                          # 3 (Step 1)
        "Checkout: 10k",                                              # 4 (Step 2 - Success)
        "Lost Traffic: 12.5k",                                        # 5 (The "Bucket of Loss")
        "Purchase: 3.5k",                                             # 6 (Step 3 - Success)
        "Upsell (VIP): 1.2k", "Standard Customer: 2.3k"               # 7, 8 (Step 4 - Outcomes)
    ]
    
    # 2. Define Node Colors (Matching the theme)
    node_colors = [
        "#818CF8", "#818CF8", "#818CF8", # Sources (Indigo)
        "#6366F1",                       # Landing Page (Deeper Indigo)
        "#34D399",                       # Checkout (Teal)
        "#EF4444",                       # Lost (Red)
        "#10B981",                       # Purchase (Green)
        "#FBBF24", "#10B981"             # Upsell (Gold), Standard (Green)
    ]

    # 3. Define Links (Source -> Target) and their Volumes
    source = [0, 1, 2,    3, 3,    4, 4,    6, 6]
    target = [3, 3, 3,    4, 5,    6, 5,    7, 8]
    value  = [5000, 3000, 8000,  10000, 6000,  3500, 6500,  1200, 2300]
    
    # 4. Define Link Colors (The key to clarity!)
    link_colors = [
        'rgba(99, 102, 241, 0.3)', 'rgba(99, 102, 241, 0.3)', 'rgba(99, 102, 241, 0.3)', # Traffic In (Blueish)
        'rgba(16, 185, 129, 0.5)', # LP -> Checkout (Green - Good!)
        'rgba(239, 68, 68, 0.4)',  # LP -> Lost (Red - Bad!)
        'rgba(16, 185, 129, 0.7)', # Checkout -> Purchase (Stronger Green)
        'rgba(239, 68, 68, 0.6)',  # Checkout -> Lost (Stronger Red)
        'rgba(245, 158, 11, 0.7)', # Purchase -> Upsell (Gold - Great!)
        'rgba(16, 185, 129, 0.5)'  # Purchase -> Standard (Green)
    ]

    # 5. Build the Figure
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 20,
          thickness = 25,
          line = dict(color = "#1F2937", width = 1),
          label = labels,
          color = node_colors,
          hovertemplate = 'Node: %{label}<extra></extra>'
        ),
        link = dict(
          source = source,
          target = target,
          value = value,
          color = link_colors,
          hovertemplate = 'Flow: %{source.label} → %{target.label}<br>Volume: <b>%{value}</b><extra></extra>'
        ))])
    
    fig.update_layout(
        height=600,
        font=dict(size=12, color="white"),
        margin=dict(t=40, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)', # Transparent background
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. CHANNEL BREAKDOWN TABLE
    st.divider()
    st.subheader("🏆 Channel ROI Leaderboard")
    channel_data = pd.DataFrame({
        "Channel": ["YouTube (Organic)", "Meta Ads", "TikTok Ads"],
        "Spend": ["$0", "$5,200", "$3,100"],
        "Revenue": ["$12,400", "$15,600", "$4,200"],
        "ROAS": ["∞", "3.0x", "1.35x"],
    })
    st.dataframe(channel_data, use_container_width=True, hide_index=True)
