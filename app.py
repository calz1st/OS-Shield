import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client, Client
import datetime
import time

# --- 1. THE DATABASE CONNECTION ---
db_connected = False
try:
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase: Client = create_client(url, key)
        db_connected = True
except Exception:
    db_connected = False

# --- 2. PAGE SETTINGS ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .metric-card { background-color: #1F2937; padding: 20px; border-radius: 10px; border: 1px solid #374151; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v3.2 Persistent Suite")
    st.divider()
    
    # NAVIGATION MENU
    page = st.radio("Select Module", [
        "🛡️ Revenue Shield", 
        "👻 Ghost Hunter (Retention)", 
        "📊 Unified Data (LTV)"
    ])
    
    st.divider()
    
    # DATABASE CONTROLS
    if db_connected:
        st.success("🟢 Database Linked")
        if st.button("➕ Simulate New Order"):
            try:
                new_data = {
                    "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                    "customer": "sim_user@vibe.com",
                    "amount": 499.0,
                    "status": "Protected"
                }
                supabase.table("orders").insert(new_data).execute()
                st.toast("Order Saved!", icon="✅")
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error("Error saving data. Check table columns!")
    else:
        st.warning("🔴 Database Not Linked")

# ==========================================
# MODULE 1: REVENUE SHIELD (Persistent)
# ==========================================
if page == "🛡️ Revenue Shield":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Revenue Shield")
        st.caption("Live Protection Feed from Supabase")
    with col2:
        st.metric("ROI Multiplier", "12.4x")
    
    st.divider()
    
    if db_connected:
        try:
            # PULL REAL DATA FROM SUPABASE
            response = supabase.table("orders").select("*").order("created_at", desc=True).execute()
            if response.data:
                df = pd.DataFrame(response.data)
                # Cleaning up columns for display
                st.dataframe(df[['order_id', 'customer', 'amount', 'status', 'created_at']], 
                             use_container_width=True, hide_index=True)
            else:
                st.info("Database is empty. Click 'Simulate' in the sidebar!")
        except Exception as e:
            st.error(f"API Error: {e}")
    else:
        st.info("Simulation Mode: Connect Supabase for persistent logs.")

# ==========================================
# MODULE 2: GHOST HUNTER
# ==========================================
elif page == "👻 Ghost Hunter (Retention)":
    st.title("Ghost Hunter AI")
    st.caption("Predictive Churn Detection")
    st.divider()
    
    st.info("🤖 **AI Analysis:** Detected **5 High-Risk users** (Ghosting for >7 days).")
    
    risk_data = [
        {"User": "@CryptoKing_99", "Last Active": "12 Days Ago", "Health Score": 15, "LTV": "$450"},
        {"User": "Sarah_Designs", "Last Active": "8 Days Ago", "Health Score": 22, "LTV": "$120"},
        {"User": "MikeTrading", "Last Active": "9 Days Ago", "Health Score": 18, "LTV": "$890"},
    ]
    
    st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True, column_config={
        "Health Score": st.column_config.ProgressColumn("Health Score", min_value=0, max_value=100)
    })
    
    if st.button("🚀 Auto-Send Recovery DMs"):
        st.balloons()
        st.toast("Messages Sent!", icon="✅")

# ==========================================
# MODULE 3: UNIFIED LTV (The Clear Version)
# ==========================================
elif page == "📊 Unified Data (LTV)":
    st.title("Profit Command Center")
    st.subheader("💰 The Money Flow Map")
    
    # --- UPDATED COLORFUL SANKEY ---
    labels = ["Ads: 8k", "Organic: 8k", "Landing Page", "Checkout", "Lost: 12.5k", "Purchase: 3.5k", "Upsell"]
    source = [0, 1, 2,  3, 3,  4, 4,  5] # Adjusted indices for flow
    target = [2, 2, 2,  3, 4,  5, 4,  6]
    value  = [5000, 3000, 8000, 10000, 6000, 3500, 6500, 1200]
    
    # We'll use the precise indices from the "Clear version" we designed
    labels = ["Meta Ads", "TikTok Ads", "YouTube", "Landing Page", "Checkout", "Lost Traffic", "Purchase", "Upsell"]
    source = [0, 1, 2,  3, 3,  4, 4,  6]
    target = [3, 3, 3,  4, 5,  6, 5,  7]
    value  = [5000, 3000, 8000, 10000, 6000, 3500, 6500, 1200]
    link_colors = ['rgba(129, 140, 248, 0.4)', 'rgba(129, 140, 248, 0.4)', 'rgba(129, 140, 248, 0.4)', 
                   'rgba(52, 211, 153, 0.5)', 'rgba(239, 68, 68, 0.4)', 
                   'rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.6)', 'rgba(251, 191, 36, 0.7)']

    fig = go.Figure(data=[go.Sankey(
        node = dict(pad=15, thickness=20, label=labels, color="#818CF8"),
        link = dict(source=source, target=target, value=value, color=link_colors)
    )])
    fig.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)
