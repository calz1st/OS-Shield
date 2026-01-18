import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client, Client
import datetime
import time

# --- 1. DATABASE CONNECTION ---
db_connected = False
try:
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase: Client = create_client(url, key)
        db_connected = True
except Exception:
    db_connected = False

# --- 2. THEMES & STYLES ---
st.set_page_config(page_title="Creator OS | Revenue Shield", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E5E7EB; }
    .evidence-paper {
        background-color: #FFFFFF; color: #111827; padding: 40px; border-radius: 2px;
        font-family: 'Courier New', Courier, monospace; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .step-active { color: #10B981; font-weight: bold; }
    .step-inactive { color: #4B5563; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected:
        if st.button("➕ Simulate Order (Smart Risk)"):
            # Logic: Randomly assign risks
            risk_types = ["Low Risk", "VPN Detected", "Zip Mismatch", "Serial Refunder"]
            chosen_risk = risk_types[datetime.datetime.now().second % 4]
            amount = float(datetime.datetime.now().second * 5) + 49.0
            
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{datetime.datetime.now().second}@gmail.com",
                "amount": amount,
                "status": chosen_risk
            }
            supabase.table("orders").insert(new_data).execute()
            st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (DEEP DIVE)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    # 1. TOP LEVEL STATS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue Protected", "$28,450", "Active")
    c2.metric("Disputes Won", "14/16", "87%")
    c3.metric("Prevented Loss", "$4,200", "+$499")
    c4.metric("Avg. Defense Time", "1.2s", "Instant")

    st.divider()

    col_feed, col_action = st.columns([1.5, 1])

    with col_feed:
        st.subheader("Live Transaction Risk Monitor")
        if db_connected:
            res = supabase.table("orders").select("*").order("created_at", desc=True).limit(10).execute()
            df = pd.DataFrame(res.data)
            
            # Create a selectable table
            # We store the selection in session state
            st.write("Select a transaction to review evidence:")
            selected_row = st.selectbox("Current Queue", df.index, format_func=lambda x: f"{df.iloc[x]['order_id']} - {df.iloc[x]['customer']} ({df.iloc[x]['status']})")
            
            current_order = df.iloc[selected_row]
            
            # Mini Dashboard for the specific order
            st.markdown(f"""
            <div style="background: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;">
                <h4>Reviewing: {current_order['order_id']}</h4>
                <p><b>Amount:</b> ${current_order['amount']} | <b>Risk Factor:</b> {current_order['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            if st.button("⚖️ INITIATE DEFENSE PROTOCOL", use_container_width=True):
                st.session_state['active_dossier'] = current_order
                st.toast("Compiling logs and generating Exhibit A...")

    with col_action:
        if 'active_dossier' in st.session_state:
            order = st.session_state['active_dossier']
            
            # THE DEFENSE STEPPER
            st.markdown(f"""
            <div style="margin-bottom: 20px;">
                <span class="step-active">● Detected</span> → 
                <span class="step-active">● Logged</span> → 
                <span class="step-active">● Compiled</span> → 
                <span class="step-inactive">○ Submitted</span>
            </div>
            """, unsafe_allow_html=True)

            # THE DYNAMIC DOSSIER
            st.markdown(f"""
                <div class="evidence-paper">
                    <h3 style="text-align:center; text-decoration: underline;">EXHIBIT: {order['order_id']}</h3>
                    <p style="text-align:right;">Date: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
                    <hr>
                    <p><strong>Merchant:</strong> Creator OS Shield</p>
                    <p><strong>Customer:</strong> {order['customer']}</p>
                    <p><strong>Evidence Type:</strong> Digital Consumption Receipt</p>
                    <hr>
                    <p><b>Server Logs:</b></p>
                    <p>• Auth successful via Device Fingerprint <b>#AX-99</b></p>
                    <p>• Access to private Discord channel 'VIP-Trading' confirmed.</p>
                    <p>• Digital file '{order['order_id']}_Access_Key' downloaded.</p>
                    <br>
                    <p><b>Conclusion:</b> Service was delivered and utilized. Chargeback is fraudulent.</p>
                    <div style="border: 2px solid black; padding: 10px; text-align: center; margin-top: 10px;">
                        <b>[ AUTO-SUBMITTED TO PAYMENT PROCESSOR ]</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="height: 400px; display: flex; align-items: center; justify-content: center; border: 2px dashed #374151; border-radius: 10px;">
                    <p style="color: #6B7280;">Select a transaction and initiate protocol.</p>
                </div>
            """, unsafe_allow_html=True)

# --- OTHER MODULES (Placeholders for next work session) ---
elif page == "👻 Ghost Hunter":
    st.title("👻 Ghost Hunter")
    st.info("Module 2 work pending... Focus is currently on Revenue Shield.")
    
elif page == "📊 Unified Data":
    st.title("📊 Unified Data")
    st.info("Module 3 work pending... Focus is currently on Revenue Shield.")
