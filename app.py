import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .metric-card { background-color: #1F2937; padding: 15px; border-radius: 8px; border-left: 4px solid #8B5CF6; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v3.0 Full Suite")
    st.divider()
    
    # NAVIGATION MENU (Now with 3 Options)
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
# MODULE 3: UNIFIED LTV (The New Stuff)
# ==========================================
elif page == "📊 Unified Data (LTV)":
    st.title("Profit Command Center")
    st.caption("Cross-Platform Attribution • True LTV Analysis")
    st.divider()
    
    # 1. THE BIG NUMBERS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Blended ROAS", "3.2x", "Ad Spend Efficient")
    c2.metric("Customer LTV", "$145.00", "+$12.50 vs last month")
    c3.metric("CAC (Cost to Acquire)", "$42.00", "-$3.00")
    c4.metric("Net Profit / User", "$103.00", "Healthy")
    
    st.divider()
    
    # 2. THE MONEY FLOW (Sankey Diagram)
    st.subheader("💰 The Money Flow Map")
    st.caption("Visualizing where traffic comes from and where money is lost.")
    
    # Defining the Nodes (Stops on the map)
    labels = ["Ads (Meta)", "Ads (TikTok)", "Organic (YouTube)", 
              "Landing Page", 
              "Checkout", 
              "Purchase ($)", "Churn (Lost)", "Upsell ($$)"]
    
    # Defining the Links (Source -> Target)
    # 0=Meta, 1=TikTok, 2=YouTube
    # 3=Landing Page, 4=Checkout
    # 5=Purchase, 6=Churn, 7=Upsell
    
    source = [0, 1, 2,  3, 3,  4, 4,  5, 5] 
    target = [3, 3, 3,  4, 6,  5, 6,  7, 7] # 7 is Upsell (Self loop or next step)
    value  = [5000, 3000, 8000,  # Traffic into Landing Page
              10000, 6000,      # LP to Checkout vs Bounce (Churn)
              3500, 6500,       # Checkout to Purchase vs Abandon
              1200, 2300]       # Purchase to Upsell
    
    # Color logic
    link_colors = ['#8B5CF6']*3 + ['#10B981']*2 + ['#EF4444']*2 + ['#F59E0B']*2

    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = labels,
          color = "#6366F1"
        ),
        link = dict(
          source = source,
          target = target,
          value = value,
          color = "rgba(100, 100, 100, 0.2)"
        ))])
    
    fig.update_layout(title_text="Traffic to Net Profit Flow", font_size=12, height=500, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # 3. CHANNEL BREAKDOWN TABLE
    st.subheader("🏆 Channel ROI Leaderboard")
    channel_data = pd.DataFrame({
        "Channel": ["YouTube (Organic)", "Meta Ads", "TikTok Ads", "Newsletter"],
        "Spend": ["$0", "$5,200", "$3,100", "$0"],
        "Revenue Generated": ["$12,400", "$15,600", "$4,200", "$8,900"],
        "ROAS (Return)": ["∞", "3.0x", "1.35x", "∞"],
        "Quality Score": ["High", "Medium", "Low", "High"]
    })
    
    st.dataframe(channel_data, use_container_width=True, hide_index=True)
