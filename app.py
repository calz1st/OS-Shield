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
    .audit-log {
        background: rgba(31, 41, 55, 0.5); padding: 15px; border-radius: 8px;
        font-size: 0.85rem; border: 1px solid #374151; max-height: 300px; overflow-y: auto;
    }
    .log-entry { margin-bottom: 8px; border-bottom: 1px solid #374151; padding-bottom: 8px; display: flex; justify-content: space-between; }
    .log-time { color: #9CA3AF; font-family: monospace; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected:
        if st.button("➕ Simulate Live Transaction"):
            is_dispute = random.random() < 0.2
            chosen_status = "⚠️ DISPUTED" if is_dispute else random.choice(["Low Risk", "VPN Detected", "Zip Mismatch"])
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
        supabase.table("orders").update({"status": "📤 SUBMITTED"}).eq("order_id", order_id).execute()
        st.toast(f"Evidence for {order_id} submitted!", icon="📨")
        time.sleep(1)
        st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (Smart Audit Edition)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    if db_connected:
        res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        df = pd.DataFrame(res.data)
        disputes = df[df['status'] == "⚠️ DISPUTED"]
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue Protected", "$28,450")
        c2.metric("Pending Defense", len(disputes), delta="Urgent" if len(disputes) > 0 else None, delta_color="inverse")
        c3.metric("Win Rate", "87%")
        c4.metric("Avg Loss Saved", "$342/mo")

        st.divider()

        col_feed, col_action = st.columns([1.4, 1])

        with col_feed:
            st.subheader("🎯 Action Queue")
            queue_options = df.index.tolist()
            queue_options.sort(key=lambda x: 0 if df.iloc[x]['status'] == "⚠️ DISPUTED" else 1)
            selected_row = st.selectbox("Select Transaction", queue_options, 
                                        format_func=lambda x: f"{df.iloc[x]['status']} | {df.iloc[x]['order_id']}")
            
            current_order = df.iloc[selected_row]
            
            # --- DYNAMIC AUDIT LOG GENERATOR ---
            st.write("---")
            st.subheader(f"🕵️ Audit Trail: {current_order['order_id']}")
            
            # Convert string timestamp to datetime object
            base_time = pd.to_datetime(current_order['created_at'])
            
            def log_row(time_off, text):
                log_time = (base_time + datetime.timedelta(minutes=time_off)).strftime('%H:%M:%S')
                return f'<div class="log-entry"><span class="log-text">{text}</span><span class="log-time">{log_time}</span></div>'

            logs = []
            logs.append(log_row(0, "✅ Transaction Initialized"))
            logs.append(log_row(1, f"🤖 Risk Analysis Engine: {current_order['status']}"))
            logs.append(log_row(5, "👤 User Portal Access: Session Started"))
            
            if "DISPUTED" in current_order['status']:
                logs.append(log_row(120, "🚨 <b>Chargeback Alert</b>: Notification from Processor"))
                logs.append(log_row(122, "📄 Evidence Dossier: Auto-Drafted"))
            elif "SUBMITTED" in current_order['status']:
                logs.append(log_row(120, "🚨 Chargeback Alert Received"))
                logs.append(log_row(125, "🚀 <b>Counter-Evidence Submitted</b> by User"))
                logs.append(log_row(126, "⏳ Status: Awaiting Bank Decision"))
            else:
                logs.append(log_row(15, "✅ Digital Assets Delivered Successfully"))

            st.markdown(f'<div class="audit-log">{"".join(logs)}</div>', unsafe_allow_html=True)
            
            st.write("")
            if "DISPUTED" in current_order['status']:
                if st.button("🚀 SUBMIT COUNTER-EVIDENCE", type="primary", use_container_width=True):
                    submit_counter_evidence(current_order['order_id'])
            else:
                st.button("📄 PREVIEW EVIDENCE", use_container_width=True)

        with col_action:
            st.markdown(f"""
                <div class="evidence-paper">
                    <h3 style="text-align:center;">LEGAL EXHIBIT: {current_order['order_id']}</h3>
                    <p><strong>Merchant:</strong> Creator OS</p>
                    <p><strong>Customer:</strong> {current_order['customer']}</p>
                    <hr>
                    <p><strong>INTERNAL LOG SUMMARY:</strong></p>
                    <p>• Device: Mobile / iOS</p>
                    <p>• Usage: Active Session</p>
                    <p>• Risk Result: {current_order['status']}</p>
                    <br>
                    <div style="border: 2px solid {'#EF4444' if 'DISPUTED' in current_order['status'] else '#6366F1' if 'SUBMITTED' in current_order['status'] else '#374151'}; padding: 10px; text-align: center; font-weight: bold;">
                        {current_order['status'].upper()}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("📋 Order Ledger")
        def style_rows(row):
            if row['status'] == "⚠️ DISPUTED": return ['background-color: rgba(239, 68, 68, 0.1)'] * len(row)
            if row['status'] == "📤 SUBMITTED": return ['background-color: rgba(99, 102, 241, 0.1)'] * len(row)
            return [''] * len(row)
        st.dataframe(df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.apply(style_rows, axis=1), use_container_width=True, hide_index=True)
