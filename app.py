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
        font-size: 0.85rem; border: 1px solid #374151; max-height: 250px; overflow-y: auto;
    }
    .risk-report {
        background: rgba(239, 68, 68, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #EF4444;
    }
    @media print {
        body * { visibility: hidden; }
        #printable-dossier, #printable-dossier * { visibility: visible; }
        #printable-dossier { position: absolute; left: 0; top: 0; width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & SIMULATION ---
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

# --- HELPERS ---
def submit_counter_evidence(order_id):
    if db_connected:
        supabase.table("orders").update({"status": "📤 SUBMITTED"}).eq("order_id", order_id).execute()
        st.toast(f"Evidence for {order_id} submitted!", icon="📨")
        time.sleep(1)
        st.rerun()

def run_fraud_scan(order_id, status):
    with st.spinner(f"AI Scanning Order {order_id}..."):
        time.sleep(1.5)
        # Simulation of analysis based on status
        if "Low Risk" in status:
            return {"score": random.randint(5, 15), "flags": ["✅ Trusted Device", "✅ Domestic IP"], "verdict": "SAFE"}
        else:
            return {"score": random.randint(65, 95), "flags": ["🚩 VPN/Proxy Detected", "🚩 High-Velocity Attempt", "🚩 Mismatched Billing Zip"], "verdict": "DANGEROUS"}

# ==========================================
# MODULE 1: REVENUE SHIELD (Fraud Scan Active)
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

        col_feed, col_action = st.columns([1.4, 1.1])

        with col_feed:
            st.subheader("🎯 Action Queue")
            queue_options = df.index.tolist()
            queue_options.sort(key=lambda x: 0 if df.iloc[x]['status'] == "⚠️ DISPUTED" else 1)
            selected_row = st.selectbox("Select Transaction", queue_options, 
                                        format_func=lambda x: f"{df.iloc[x]['status']} | {df.iloc[x]['order_id']}")
            
            current_order = df.iloc[selected_row]
            
            # THE DYNAMIC SCANNER BUTTONS
            c_act1, c_act2 = st.columns(2)
            with c_act1:
                if "DISPUTED" in current_order['status']:
                    if st.button("🚀 SUBMIT TO BANK", type="primary", use_container_width=True):
                        submit_counter_evidence(current_order['order_id'])
                else:
                    # THE ACTIVE SCAN BUTTON
                    if st.button("🔍 SCAN FOR FRAUD", use_container_width=True):
                        st.session_state['scan_result'] = run_fraud_scan(current_order['order_id'], current_order['status'])
            
            with c_act2:
                if st.button("📥 EXPORT DOSSIER (PDF)", use_container_width=True):
                    st.components.v1.html("<script>window.print();</script>", height=0)

            # --- SHOW THE SCAN RESULTS ---
            if 'scan_result' in st.session_state:
                res = st.session_state['scan_result']
                color = "#10B981" if res['verdict'] == "SAFE" else "#EF4444"
                st.markdown(f"""
                <div style="background: rgba(31, 41, 55, 0.7); padding: 20px; border-radius: 10px; border: 1px solid {color}; margin-top: 20px;">
                    <h4 style="color:{color};">AI Risk Report: {res['verdict']}</h4>
                    <p><b>Risk Score:</b> {res['score']}/100</p>
                    <ul style="list-style-type: none; padding: 0;">
                        {''.join([f'<li>{f}</li>' for f in res['flags']])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # --- DYNAMIC AUDIT TRAIL ---
            st.write("---")
            st.subheader(f"🕵️ Audit Trail: {current_order['order_id']}")
            base_time = pd.to_datetime(current_order['created_at'])
            def log_row(time_off, text):
                log_time = (base_time + datetime.timedelta(minutes=time_off)).strftime('%H:%M:%S')
                return f'<div class="log-entry"><span>{text}</span><span class="log-time">{log_time}</span></div>'
            
            logs = [log_row(0, "✅ Transaction Initialized"), log_row(1, "🤖 AI Pre-Scan Complete")]
            if 'scan_result' in st.session_state:
                logs.append(log_row(2, f"🔍 Deep Scan Initiated: {st.session_state['scan_result']['verdict']}"))
            st.markdown(f'<div class="audit-log">{"".join(logs)}</div>', unsafe_allow_html=True)

        with col_action:
            st.markdown(f"""
                <div id="printable-dossier" class="evidence-paper">
                    <h3 style="text-align:center; text-decoration: underline;">LEGAL EXHIBIT: {current_order['order_id']}</h3>
                    <p style="text-align:right; font-size: 0.8rem;">REF: CR-OS-{current_order['order_id'][1:]}</p>
                    <hr>
                    <p><strong>Customer:</strong> {current_order['customer']}</p>
                    <p><strong>Amount:</strong> ${current_order['amount']}</p>
                    <hr>
                    <p><strong>COMPLIANCE SUMMARY:</strong></p>
                    <p>• Device ID: Authenticated</p>
                    <p>• Delivery: 100% Downloaded</p>
                    <br><br>
                    <div style="border: 2px solid black; padding: 15px; text-align: center; font-weight: bold;">
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
