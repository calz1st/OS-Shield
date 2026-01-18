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
    /* Custom CSS for the Table Headers */
    .stDataFrame thead tr th {
        background-color: #1F2937 !important;
        color: #9CA3AF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected:
        if st.button("➕ Simulate Smart-Risk Order"):
            risk_types = ["Low Risk", "VPN Detected", "Zip Mismatch", "Serial Refunder"]
            chosen_risk = risk_types[datetime.datetime.now().second % 4]
            # Random amount between $20 and $600
            amount = float((datetime.datetime.now().microsecond % 580) + 20)
            
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{datetime.datetime.now().second}@vibe.io",
                "amount": amount,
                "status": chosen_risk
            }
            supabase.table("orders").insert(new_data).execute()
            st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (Double-View)
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

    # --- TOP ROW: MONITOR & DOSSIER ---
    col_feed, col_action = st.columns([1.5, 1])

    with col_feed:
        st.subheader("🎯 Live Transaction Risk Monitor")
        if db_connected:
            res = supabase.table("orders").select("*").order("created_at", desc=True).limit(10).execute()
            df = pd.DataFrame(res.data)
            
            st.write("Review active flags:")
            selected_row = st.selectbox("Action Queue", df.index, 
                                        format_func=lambda x: f"{df.iloc[x]['order_id']} | Risk: {df.iloc[x]['status']}")
            
            current_order = df.iloc[selected_row]
            
            # Risk Analysis Card
            risk_color = "#10B981" if current_order['status'] == "Low Risk" else "#EF4444"
            st.markdown(f"""
            <div style="background: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid {risk_color};">
                <h4 style="margin:0;">Analysis for {current_order['order_id']}</h4>
                <p style="margin:5px 0;"><b>Customer:</b> {current_order['customer']}</p>
                <p style="margin:0;"><b>Financial Impact:</b> <span style="color:{risk_color}; font-weight:bold;">${current_order['amount']}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            if st.button("⚖️ COMPILE DEFENSE CASE", use_container_width=True):
                st.session_state['active_dossier'] = current_order

    with col_action:
        if 'active_dossier' in st.session_state:
            order = st.session_state['active_dossier']
            st.markdown(f"""
                <div class="evidence-paper">
                    <h3 style="text-align:center; text-decoration: underline;">EXHIBIT: {order['order_id']}</h3>
                    <p style="text-align:right;">Date: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
                    <hr>
                    <p><strong>Merchant:</strong> Creator OS Shield</p>
                    <p><strong>Customer:</strong> {order['customer']}</p>
                    <p><strong>Evidence:</strong> Digital Receipt & Access Logs</p>
                    <hr>
                    <p>• Auth successful via Device Fingerprint.</p>
                    <p>• User active in Discord for 14m post-purchase.</p>
                    <p>• Digital assets successfully delivered.</p>
                    <br>
                    <div style="border: 2px solid black; padding: 10px; text-align: center;">
                        <b>[ READY FOR SUBMISSION ]</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="height: 380px; display: flex; align-items: center; justify-content: center; border: 2px dashed #374151; border-radius: 10px;">
                    <p style="color: #6B7280;">Select a flagged transaction to review evidence.</p>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- BOTTOM ROW: THE PROFESSIONAL LEDGER ---
    st.subheader("📋 Order Ledger (Last 50 Transactions)")
    if db_connected:
        # We pull 50 orders for the ledger
        full_res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        ledger_df = pd.DataFrame(full_res.data)

        # We style the Status column to look professional
        def color_status(val):
            if val == "Low Risk": color = '#10B981'
            elif val == "VPN Detected": color = '#F59E0B'
            else: color = '#EF4444' # Critical/Refunder
            return f'color: {color}; font-weight: bold;'

        st.dataframe(
            ledger_df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.map(color_status, subset=['status']),
            use_container_width=True,
            hide_index=True,
            column_config={
                "amount": st.column_config.NumberColumn("Total Value", format="$%.2f"),
                "created_at": st.column_config.DatetimeColumn("Timestamp", format="D MMM, HH:mm"),
                "status": "Risk Level"
            }
        )
