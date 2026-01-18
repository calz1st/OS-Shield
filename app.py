import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import requests # This is the tool that talks to the real internet

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .status-badge { color: #10B981; font-weight: bold; border: 1px solid #10B981; padding: 2px 8px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION: GET REAL SHOPIFY DATA ---
def fetch_shopify_orders(shop_url, access_token):
    # This cleans the URL if the user adds "https://" or slashes
    clean_url = shop_url.replace("https://", "").replace("/", "")
    url = f"https://{clean_url}/admin/api/2023-10/orders.json?status=any&limit=5"
    headers = {"X-Shopify-Access-Token": access_token}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("orders", [])
        else:
            return None # Connection failed
    except:
        return None

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v2.0 Hybrid Engine")
    st.divider()
    
    # THE MAGIC SWITCH
    demo_mode = st.toggle("Simulate Demo Mode", value=True)
    
    st.divider()
    
    if not demo_mode:
        st.subheader("🔌 Live Connection")
        store_url = st.text_input("Store URL", placeholder="example.myshopify.com")
        api_key = st.text_input("Admin Access Token", type="password")
        connect_btn = st.button("Connect to Shopify", type="primary")
    else:
        st.info("Currently running in Simulation Mode. Switch off above to connect real data.")

# --- MAIN DASHBOARD LOGIC ---

# DEFAULT VALUES (Simulation)
orders_data = []
total_saved = "$14,250"
revenue_delta = "+$1,200"
dispute_win_rate = 78
shop_name = "Simulation Store"
connection_status = "Demo Active"

# REAL DATA LOGIC
if not demo_mode and 'connect_btn' in locals() and connect_btn:
    with st.spinner("Connecting to Shopify API..."):
        real_orders = fetch_shopify_orders(store_url, api_key)
        
        if real_orders:
            # If connection works, we overwrite the fake data with REAL data
            shop_name = store_url.split('.')[0].capitalize()
            connection_status = "🟢 Live Connected"
            st.toast("Sync Successful!", icon="✅")
            
            # Process real orders into our table format
            for order in real_orders:
                orders_data.append({
                    "Order ID": f"#{order['order_number']}",
                    "Customer": order['email'] or "No Email",
                    "Total": f"${order['total_price']}",
                    "Status": order['financial_status'].capitalize()
                })
            
            # Update metrics based on real data (Simple logic for now)
            total_saved = f"${len(real_orders) * 50}" # Fake calculation for prototype
            
        else:
            st.error("Connection Failed. Check your URL and Access Token.")

# IF DEMO MODE IS ON (Or no real data yet), LOAD FAKE DATA
if not orders_data:
    orders_data = [
        {"Order ID": "#1054", "Customer": "alex@gmail.com", "Total": "$49.00", "Status": "Paid"},
        {"Order ID": "#1053", "Customer": "sarah@yahoo.com", "Total": "$199.00", "Status": "Paid"},
        {"Order ID": "#1052", "Customer": "bot@scam.net", "Total": "$499.00", "Status": "Voided"},
    ]

# --- UI RENDER ---

# Header
c1, c2 = st.columns([3, 1])
with c1:
    st.title(f"Revenuse Shield: {shop_name}")
    st.caption(f"Status: {connection_status}")
with c2:
    st.metric("Total Protected", total_saved, revenue_delta)

st.divider()

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Active Disputes", "3", "-2 from last week")
m2.metric("Win Rate", f"{dispute_win_rate}%", "+5%")
m3.metric("Global Tax Risk", "Low", "No Action Needed")

st.markdown("### 📋 Recent Orders & Risk Analysis")

# Convert list to dataframe for display
df = pd.DataFrame(orders_data)

# Show the table
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.TextColumn(
            "Payment Status",
            help="Status from Shopify",
            validate="^[a-zA-Z0-9_]+$"
        ),
    }
)

if demo_mode:
    st.info("💡 Tip: Toggle 'Simulate Demo Mode' off in the sidebar to enter your Real API Keys.")
