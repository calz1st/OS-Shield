import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CSS STYLING (Professional Dark Mode) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* Health Score Colors */
    .health-good { color: #10B981; font-weight: bold; }
    .health-risk { color: #F59E0B; font-weight: bold; }
    .health-critical { color: #EF4444; font-weight: bold; }
    
    /* Card Styling */
    .metric-card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v2.1 Demo Suite")
    st.divider()
    
    # NAVIGATION MENU
    page = st.radio("Select Module", ["🛡️ Revenue Shield", "👻 Ghost Hunter (Retention)"])
    
    st.divider()
    st.info("Simulation Mode: ON")
    st.caption("Running on synthetic data.")

# ==========================================
# MODULE 1: REVENUE SHIELD (The Original)
# ==========================================
if page == "🛡️ Revenue Shield":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Revenue Shield")
        st.caption("Active Protection • Dispute Auto-Response • Tax Compliance")
    with col2:
        st.metric("ROI Multiplier", "12.4x", "Active")
    st.divider()

    # Top Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Disputes Defended", "14", "+2 Today")
    m2.metric("Revenue Saved", "$14,250", "+$1,200")
    m3.metric("Tax Risk (DE)", "High", "Action Required")
    
    st.subheader("Recent Defense Logs")
    shield_data = pd.DataFrame([
        {"Time": "10:42 AM", "Event": "Auto-Dispute (#994)", "Outcome": "Evidence Sent"},
        {"Time": "09:15 AM", "Event": "Fraud Block (IP 192..)", "Outcome": "Blocked"},
        {"Time": "Yesterday", "Event": "VAT Threshold Alert", "Outcome": "Flagged"},
    ])
    st.dataframe(shield_data, use_container_width=True, hide_index=True)
    
    if st.button("Generate Evidence Dossier (Simulation)"):
        st.success("Generating PDF for Dispute #994...")
        time.sleep(1)
        st.markdown("✅ **Evidence Submitted to Stripe.**")

# ==========================================
# MODULE 2: GHOST HUNTER (The New Feature)
# ==========================================
elif page == "👻 Ghost Hunter (Retention)":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Ghost Hunter AI")
        st.caption("Predictive Churn Detection • Auto-Reactivation")
    with col2:
        st.metric("Churn Risk", "High", "+4 Members at Risk", delta_color="inverse")
    
    st.divider()

    # The Logic: Explain what's happening
    st.info("🤖 **AI Analysis:** Scanned 450 members. Detected **5 High-Risk users** (Ghosting for >7 days).")

    # MOCK DATA: AT-RISK MEMBERS
    # We create a table of people who are about to quit
    risk_data = [
        {"User": "@CryptoKing_99", "Last Active": "12 Days Ago", "Health Score": 15, "LTV": "$450"},
        {"User": "Sarah_Designs", "Last Active": "8 Days Ago", "Health Score": 22, "LTV": "$120"},
        {"User": "MikeTrading", "Last Active": "9 Days Ago", "Health Score": 18, "LTV": "$890"},
        {"User": "Anon_User22", "Last Active": "15 Days Ago", "Health Score": 10, "LTV": "$50"},
        {"User": "J_Doe_88", "Last Active": "6 Days Ago", "Health Score": 45, "LTV": "$200"},
    ]
    df_risk = pd.DataFrame(risk_data)

    # Display the "Kill List" (People leaving)
    st.subheader("⚠️ At-Risk Member List")
    
    # We use a special Column Config to show a Progress Bar for "Health Score"
    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Health Score": st.column_config.ProgressColumn(
                "Health Score (0-100)",
                help="Lower score means higher chance of quitting.",
                format="%d",
                min_value=0,
                max_value=100,
            ),
             "User": st.column_config.TextColumn("Member Name", help="Discord/Whop Username"),
        }
    )

    st.divider()

    # THE INTERACTIVE ACTION
    st.subheader("⚡ Automated Recovery Actions")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 🎁 The 'Soft Nudge'")
        st.write("Send a personalized DM: *'Hey [Name], noticed you've been gone. Here is a free resource pack to get you back on track.'*")
        if st.button("🚀 Auto-Send DMs (5 Users)"):
            with st.status("Engaging Ghost Hunter Protocol...", expanded=True) as status:
                st.write("📝 Generating personalized AI messages...")
                time.sleep(1)
                st.write("📨 Sending to Discord API...")
                time.sleep(1)
                st.write("✅ Messages Delivered.")
                status.update(label="Recovery Complete!", state="complete", expanded=False)
            st.balloons() # Fun animation for success

    with c2:
        st.markdown("### 🏷️ The 'Downsell' Offer")
        st.write("For users with Score < 15: Offer a **50% discount** for next month instead of cancelling.")
        if st.button("💸 Activate Discount Sequence"):
            st.toast("Discount offers sent to 2 Critical users.", icon="🏷️")
