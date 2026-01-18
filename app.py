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
    /* Pulsing Alert for Disputes */
    @keyframes pulse-red {
        0% { background-color: rgba(239, 68, 68, 0.1); }
        50% { background-color: rgba(239, 68, 68, 0.3); }
        100% { background-color: rgba(239, 68, 68, 0.1); }
    }
    .dispute-alert {
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #EF4444;
        animation: pulse-red 2s infinite;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected:
        if st.button("➕ Simulate Live Transaction"):
            # Simulation Logic: 20% chance of a DISPUTE
            is_dispute = random.random() < 0.2
            
            if is_dispute:
                chosen_status = "⚠️ DISPUTED"
                amount = random.choice([199.0, 499.0, 999.0])
            else:
                risk_types = ["Low Risk", "VPN Detected", "Zip Mismatch"]
                chosen_status = random.choice(risk_types)
                amount = float(random.randint(20, 500))
            
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{random.randint(10,99)}@vibe.io",
                "amount": amount,
                "status": chosen_status
            }
            supabase.table("orders").insert(new_data).execute()
            st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (Alert System)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    # FETCH DATA EARLY FOR ALERTS
    if db_connected:
        res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        df = pd.DataFrame(res.data)
        
        # Calculate Dispute Count
        dispute_count = len(df[df['status'] == "⚠️ DISPUTED"])
        
        # 1. TOP LEVEL STATS
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue Protected", "$28,450")
        c2.metric("Disputes Won", "14/16", "87%")
        # Pulse the Dispute Count if it's > 0
        c3.metric("🚨 Active Disputes", dispute_count, delta="Action Required" if dispute_count > 0 else None, delta_color="inverse")
        c4.metric("Prevented Loss", "$4,200")

        st.divider()

        # --- URGENT ALERT BOX ---
        if dispute_count > 0:
            st.markdown(f"""
            <div class="dispute-alert">
                <h4 style="margin:0; color: #EF4444;">🚨 URGENT: {dispute_count} Active Dispute(s) Detected</h4>
                <p style="margin:5px 0; color: #FCA5A5;">Immediate action required to prevent revenue clawback. Review the Action Queue below.</p>
            </div>
            """, unsafe_allow_html=True)

        # --- MONITOR & DOSSIER ---
        col_feed, col_action = st.columns([1.5, 1])

        with col_feed:
            st.subheader("🎯 Action Queue")
            
            # Filter dropdown to show Disputed orders first
            queue_options = df.index.tolist()
            # Sort the index so Disputed ones are at the top
            queue_options.sort(key=lambda x: 0 if df.iloc[x]['status'] == "⚠️ DISPUTED" else 1)
            
            selected_row = st.selectbox("Select order to defend:", queue_options, 
                                        format_func=lambda x: f"{df.iloc[x]['status']} | {df.iloc[x]['order_id']} (${df.iloc[x]['amount']})")
            
            current_order = df.iloc[selected_row]
            
            # Risk Analysis Card
            status_style = "background: rgba(239, 68, 68, 0.2); border-left: 5px solid #EF4444;" if "DISPUTED" in current_order['status'] else "background: #1F2937; border-left: 5px solid #10B981;"
            
            st.markdown(f"""
            <div style="{status_style} padding: 20px; border-radius: 10px;">
                <h4 style="margin:0;">Target: {current_order['order_id']}</h4>
                <p style="margin:5px 0;"><b>Customer:</b> {current_order['customer']}</p>
                <p style="margin:0;"><b>Financial Status:</b> {current_order['status']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write("")
            btn_label = "⚖️ COUNTER DISPUTE" if "DISPUTED" in current_order['status'] else "⚖️ COMPILE EVIDENCE"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state['active_dossier'] = current_order

        with col_action:
            if 'active_dossier' in st.session_state:
                order = st.session_state['active_dossier']
                st.markdown(f"""
                    <div class="evidence-paper">
                        <h3 style="text-align:center; text-decoration: underline;">LEGAL EXHIBIT: {order['order_id']}</h3>
                        <p style="text-align:right;">Date: {datetime.datetime.now().strftime('%Y-%m-%d')}</p>
                        <hr>
                        <p><strong>RE:</strong> Dispute Counter-Evidence for {order['customer']}</p>
                        <hr>
                        <p><strong>SERVER ACCESS LOGS:</strong></p>
                        <p>• Verified IP: 192.168.1.1</p>
                        <p>• Access Method: Digital Portal</p>
                        <p>• Consumption: 100% of Module 1</p>
                        <br>
                        <div style="border: 2px solid #EF4444; padding: 10px; text-align: center; color: #EF4444; font-weight: bold;">
                            READY FOR LEGAL SUBMISSION
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Select a transaction from the queue to start defense.")

        st.divider()

        # --- THE LEDGER ---
        st.subheader("📋 Order Ledger")
        
        def style_rows(row):
            if row['status'] == "⚠️ DISPUTED":
                return ['background-color: rgba(239, 68, 68, 0.1)'] * len(row)
            return [''] * len(row)

        st.dataframe(
            df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.apply(style_rows, axis=1),
            use_container_width=True,
            hide_index=True
        )
