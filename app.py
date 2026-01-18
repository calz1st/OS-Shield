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
        background-color: #FFFFFF !important; color: #111827 !important; 
        padding: 40px !important; border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5); border: 1px solid #ddd;
    }
    @media print {
        body * { visibility: hidden !important; }
        #printable-area, #printable-area * { visibility: visible !important; }
        #printable-area { position: absolute !important; left: 0 !important; top: 0 !important; width: 100% !important; background-color: white !important; }
    }
    .audit-log {
        background: rgba(31, 41, 55, 0.5); padding: 15px; border-radius: 8px;
        font-size: 0.85rem; border: 1px solid #374151; max-height: 200px; overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & SIMULATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9424/9424443.png", width=60)
    st.title("Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected and st.button("➕ Simulate Live Transaction"):
        is_dispute = random.random() < 0.2
        new_data = {
            "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
            "customer": f"user_{random.randint(10,99)}@vibe.io",
            "amount": float(random.randint(49, 999)),
            "status": "⚠️ DISPUTED" if is_dispute else "✅ SUCCESS"
        }
        supabase.table("orders").insert(new_data).execute()
        st.rerun()

# --- HELPERS ---
def submit_counter_evidence(order_id):
    if db_connected:
        supabase.table("orders").update({"status": "📤 SUBMITTED"}).eq("order_id", order_id).execute()
        st.toast("Evidence Transmitted!", icon="✅")
        time.sleep(0.5)
        st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (Fully Linked)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    if db_connected:
        # PULL REAL DATA
        res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        df = pd.DataFrame(res.data)
        
        if not df.empty:
            # --- CALCULATE LIVE METRICS ---
            total_rev = df[df['status'] != '⚠️ DISPUTED']['amount'].sum()
            active_disputes = df[df['status'] == "⚠️ DISPUTED"]
            dispute_val = active_disputes['amount'].sum()
            submitted_count = len(df[df['status'] == "📤 SUBMITTED"])
            total_dispute_cases = len(active_disputes) + submitted_count
            
            # Win Rate Logic: (Submitted / Total Disputes) - simple proxy for simulation
            win_rate = (submitted_count / total_dispute_cases * 100) if total_dispute_cases > 0 else 100
            
            # 1. TOP LEVEL STATS (LINKED)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Protected Revenue", f"${total_rev:,.2f}")
            c2.metric("Action Required", len(active_disputes), delta=f"${dispute_val:,.0f} At Risk", delta_color="inverse")
            c3.metric("Defense Win Rate", f"{win_rate:.0f}%", "+2.4%")
            c4.metric("Avg Case Value", f"${df['amount'].mean():,.2f}")

            st.divider()

            # --- LEDGER ---
            st.subheader("📋 Order Ledger")
            filter_view = st.radio("Display Mode:", ["All Orders", "Disputes Only"], horizontal=True)
            
            display_df = df if filter_view == "All Orders" else df[df['status'].isin(["⚠️ DISPUTED", "📤 SUBMITTED"])]

            def highlight_status(row):
                if "DISPUTED" in row['status']: return ['background-color: rgba(239, 68, 68, 0.15); color: #FCA5A5; font-weight: bold;'] * len(row)
                elif "SUBMITTED" in row['status']: return ['background-color: rgba(99, 102, 241, 0.1); color: #A5B4FC;'] * len(row)
                return ['color: #10B981;'] * len(row)

            if not display_df.empty:
                st.dataframe(
                    display_df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.apply(highlight_status, axis=1),
                    use_container_width=True, hide_index=True,
                    column_config={"amount": st.column_config.NumberColumn("Total", format="$%.2f")}
                )
            else:
                st.info("No disputes found.")

            st.divider()

            # --- ACTION CENTER ---
            col_left, col_right = st.columns([1.3, 1])
            with col_left:
                st.subheader("🎯 Action Queue")
                df_sorted = df.sort_values(by='status', ascending=False) 
                selected_id = st.selectbox("Select Order to Review", options=df_sorted['order_id'].tolist())
                current_order = df[df['order_id'] == selected_id].iloc[0]
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if "DISPUTED" in current_order['status']:
                        if st.button("🚀 SUBMIT TO BANK", type="primary", use_container_width=True):
                            submit_counter_evidence(current_order['order_id'])
                    else:
                        st.button("🔍 SCAN FOR FRAUD", use_container_width=True)
                with c_btn2:
                    if st.button("📥 EXPORT DOSSIER (PDF)", use_container_width=True):
                        st.components.v1.html("<script>setTimeout(function(){ window.print(); }, 300);</script>", height=0)

                st.write("---")
                st.subheader(f"🕵️ Audit Trail: {current_order['order_id']}")
                st.markdown(f'<div class="audit-log">✅ Order Initialized<br>🤖 AI Analysis: {current_order["status"]}</div>', unsafe_allow_html=True)

            with col_right:
                st.markdown(f"""
                    <div id="printable-area" class="evidence-paper">
                        <h2 style="text-align:center; text-decoration: underline;">LEGAL EVIDENCE</h2>
                        <p style="text-align:right;">Order: {current_order['order_id']}</p>
                        <hr>
                        <p><strong>CUSTOMER:</strong> {current_order['customer']}</p>
                        <p><strong>VALUE:</strong> ${current_order['amount']}</p>
                        <p><strong>STATUS:</strong> {current_order['status']}</p>
                        <hr>
                        <h4>SYSTEM AUDIT:</h4>
                        <p>• Device Auth: OK | IP: 192.168.1.1</p>
                        <p>• Usage: 100% Downloaded</p>
                        <br><br>
                        <div style="border: 2px solid black; padding: 10px; text-align: center; font-weight: bold;">OFFICIAL AUDIT RECORD</div>
                    </div>
                """, unsafe_allow_html=True)
