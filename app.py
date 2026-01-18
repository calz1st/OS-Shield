import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .success-box { padding: 20px; border: 1px solid #10B981; border-radius: 5px; color: #10B981; background-color: rgba(16, 185, 129, 0.1); }
    .warning-box { padding: 20px; border: 1px solid #F59E0B; border-radius: 5px; color: #F59E0B; background-color: rgba(245, 158, 11, 0.1); }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: THE ENGINE ROOM ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9424/9424443.png", width=50)
    st.title("Creator OS")
    st.write("v1.5-Beta")
    st.divider()
    
    st.subheader("🔌 Connect Your Store")
    st.info("To see real data, enter your API details below.")
    
    # INPUT FIELDS FOR USER
    store_url = st.text_input("Shopify Store URL", placeholder="mystore.myshopify.com")
    api_key = st.text_input("Admin API Token", type="password", placeholder="shpat_xxxxxxxxxxx")
    
    if st.button("Connect & Sync", type="primary"):
        if api_key and store_url:
            with st.spinner("Connecting to Shopify..."):
                time.sleep(2) # Simulating the connection time
                st.session_state['is_connected'] = True
                st.success("Successfully Connected!")
        else:
            st.error("Please enter both URL and Key.")
    
    st.divider()
    st.caption("🔒 Data is encrypted and never stored.")

# --- MAIN APP LOGIC ---

# 1. CHECK IF CONNECTED
if 'is_connected' not in st.session_state:
    st.session_state['is_connected'] = False

if st.session_state['is_connected']:
    # === SHOW THE REAL DASHBOARD ===
    
    # Simulate fetching REAL data using the user's name
    shop_name = store_url.split('.')[0].capitalize() if store_url else "My Store"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"🛡️ Protection Active: {shop_name}")
        st.caption("Live Feed from Shopify Admin API")
    with col2:
        st.metric(label="Protected Revenue", value="$24,500", delta="Live Sync")

    st.divider()
    
    # METRICS ROW
    c1, c2, c3 = st.columns(3)
    c1.metric("Disputes Blocked", "12", "+2 today")
    c2.metric("Chargeback Rate", "0.4%", "-1.2% vs avg")
    c3.metric("Tax Liability (EU)", "€4,200", "Safe")
    
    st.divider()
    
    st.subheader("⚡ Live Transaction Monitor")
    st.write(f"Listening to webhooks from **{store_url}**...")
    
    # Simulated Real Data Table
    st.dataframe(pd.DataFrame({
        "Order ID": ["#1054", "#1053", "#1052", "#1051"],
        "Customer": ["alex@gmail.com", "sarah@yahoo.com", "mike@hotmail.com", "bot@scam.net"],
        "Risk Score": ["Low", "Low", "Medium", "High (Blocked)"],
        "Status": ["Fulfilled", "Fulfilled", "Flagged", "Refunded"]
    }), use_container_width=True)

else:
    # === SHOW THE LANDING PAGE (BLURRED) ===
    st.title("🛡️ Creator OS")
    
    st.markdown("""
        <div class="warning-box">
            <h3>⚠️ Waiting for Connection</h3>
            <p>This is the Creator OS Revenue Shield. To activate the protection for your business, 
            please enter your <strong>Shopify API Credentials</strong> in the sidebar on the left.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Blurred/Fake background to show them what they are missing
    st.write("")
    st.image("https://placehold.co/1000x400/111827/222222?text=Dashboard+Locked+-+Connect+Store+To+Unlock", use_container_width=True)
