import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client, Client
import datetime
import time
import random

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
    @keyframes pulse-red {
        0% { background-color: rgba(239, 68, 68, 0.1); }
        50% { background-color: rgba(239, 68, 68, 0.3); }
        100% { background-color: rgba(239, 68, 68, 0.1); }
    }
    .dispute-alert {
        padding: 15px; border-radius: 8px; border: 2px solid #EF4444;
        animation: pulse-red 2s infinite; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & SIMULATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected:
        if st.button("➕ Simulate New Order"):
            is_dispute = random.random() < 0.25
            chosen_status = "⚠️ DISPUTED" if is_dispute else "Low Risk"
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{random.randint(10,99)}@vibe.io",
                "amount": float(random.randint(49, 999)),
                "status": chosen_status
            }
            supabase.table("orders").insert(new_data).execute()
            st.rerun()

# --- HELPER: SUBMIT EVIDENCE ---
def submit_counter_evidence(order_id):
    if db_connected:
        # Update the status in Supabase to '📤 SUBMITTED'
        supabase.table("orders").update({"status": "📤 SUBMITTED"}).eq("order_id", order_id).execute()
        st.toast(f"Evidence for {order_id} submitted to bank!", icon="📨")
        time.sleep(1)
        st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (With Resolution)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    if db_connected:
        res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        df = pd.DataFrame(res.data)
        
        # Calculate Alerts
        disputes = df[df['status'] == "⚠️ DISPUTED"]
        submitted = df[df['status'] == "📤 SUBMITTED"]
        
        # 1. TOP LEVEL STATS
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue Protected", "$28,450")
        c2.metric("Evidence Pending", len(disputes), delta="Action Required" if len(disputes) > 0 else None, delta_color="inverse")
        c3.metric("Under Review", len(submitted), delta="Processing")
        c4.metric("Win Rate", "87%")

        st.divider()

        # --- PULSING ALERT ---
        if not disputes.empty:
            st.markdown(f"""<div class="dispute-alert"><h4>🚨 {len(disputes)} Active Dispute(s) Needing Evidence</h4></div>""", unsafe_allow_html=True)

        col_feed, col_action = st.columns([1.5, 1])

        with col_feed:
            st.subheader("🎯 Action Queue")
            queue_options = df.index.tolist()
            # Sort so Disputed ones are at the very top
            queue_options.sort(key=lambda x: 0 if df.iloc[x]['status'] == "⚠️ DISPUTED" else 1)
            
            selected_row = st.selectbox("Select Transaction", queue_options, 
                                        format_func=lambda x: f"{df.iloc[x]['status']} | {df.iloc[x]['order_id']}")
            
            current_order = df.iloc[selected_row]
            
            st.markdown(f"""
            <div style="background: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid {'#EF4444' if 'DISPUTED' in current_order['status'] else '#6366F1' if 'SUBMITTED' in current_order['status'] else '#10B981'};">
                <h4 style="margin:0;">Order {current_order['order_id']}</h4>
                <p style="margin:0;"><b>Current Status:</b> {current_order['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            if "DISPUTED" in current_order['status']:
                if st.button("🚀 SUBMIT COUNTER-EVIDENCE", type="primary", use_container_width=True):
                    submit_counter_evidence(current_order['order_id'])
            elif "SUBMITTED" in current_order['status']:
                st.button("📄 VIEW SUBMISSION RECEIPT", use_container_width=True, disabled=True)
            else:
                st.button("🔍 REVIEW DATA", use_container_width=True)

        with col_action:
            if "SUBMITTED" in current_order['status']:
                st.success("✅ Evidence was successfully transmitted to the bank on this order.")
                st.write("Current Status: **Awaiting Bank Decision (7-14 days)**")
            else:
                st.markdown(f"""
                    <div class="evidence-paper">
                        <h3 style="text-align:center;">EXHIBIT: {current_order['order_id']}</h3>
                        <p><strong>Customer:</strong> {current_order['customer']}</p>
                        <hr>
                        <p>• Device Fingerprint Match: Verified</p>
                        <p>• Access Log: 100% Consumption</p>
                        <br>
                        <div style="border: 2px solid #374151; padding: 10px; text-align: center;">DRAFT EVIDENCE</div>
                    </div>
                """, unsafe_allow_html=True)

        st.divider()

        # --- THE LEDGER ---
        st.subheader("📋 Order Ledger")
        def style_rows(row):
            if row['status'] == "⚠️ DISPUTED": return ['background-color: rgba(239, 68, 68, 0.1)'] * len(row)
            if row['status'] == "📤 SUBMITTED": return ['background-color: rgba(99, 102, 241, 0.1)'] * len(row)
            return [''] * len(row)

        st.dataframe(df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.apply(style_rows, axis=1), use_container_width=True, hide_index=True)
