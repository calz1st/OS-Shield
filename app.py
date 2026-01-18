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
    .audit-log {
        background: rgba(31, 41, 55, 0.5); padding: 15px; border-radius: 8px;
        font-size: 0.85rem; border: 1px solid #374151; max-height: 200px; overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR & TOOLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9424/9424443.png", width=60)
    st.title("Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    
    st.divider()
    
    if db_connected:
        if st.button("➕ Simulate Live Transaction", use_container_width=True):
            is_dispute = random.random() < 0.25
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{random.randint(10,99)}@vibe.io",
                "amount": float(random.randint(49, 999)),
                "status": "⚠️ DISPUTED" if is_dispute else "✅ SUCCESS"
            }
            supabase.table("orders").insert(new_data).execute()
            st.rerun()
            
        with st.expander("🛠️ System Tools"):
            if st.button("🗑️ Clear Database"):
                supabase.table("orders").delete().neq("order_id", "0").execute()
                st.rerun()

# --- HELPERS ---
def update_dispute_status(order_id, new_status):
    if db_connected:
        supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()
        st.toast(f"Status updated to {new_status}", icon="✅")
        time.sleep(0.5)
        st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD (Truth Metrics)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    if db_connected:
        res = supabase.table("orders").select("*").order("created_at", desc=True).execute()
        df = pd.DataFrame(res.data)
        
        if not df.empty:
            # --- UPDATED FINANCIAL LOGIC ---
            # 1. Total Protected Revenue (Successful orders + Won disputes)
            total_protected = df[df['status'].isin(['✅ SUCCESS', '✅ WON'])]['amount'].sum()
            
            # 2. Rescued Revenue (Only orders that have been won)
            rescued_val = df[df['status'] == '✅ WON']['amount'].sum()
            
            # 3. Currently At Risk (Open disputes + Pending submissions)
            at_risk_df = df[df['status'].isin(['⚠️ DISPUTED', '📤 SUBMITTED'])]
            at_risk_val = at_risk_df['amount'].sum()
            
            # 1. TOP LEVEL STATS
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Protected Revenue", f"${total_protected:,.2f}", help="Sum of all successful and won orders")
            c2.metric("Currently At Risk", f"${at_risk_val:,.2f}", delta=f"{len(at_risk_df)} Cases", delta_color="inverse")
            c3.metric("Rescued from Disputes", f"${rescued_val:,.2f}", delta="Recovered")
            c4.metric("Avg Order Value", f"${df['amount'].mean():,.2f}")

            st.divider()

            # --- LEDGER ---
            st.subheader("📋 Order Ledger")
            filter_view = st.radio("Display View:", ["All Orders", "Active Cases"], horizontal=True)
            display_df = df if filter_view == "All Orders" else df[df['status'].isin(["⚠️ DISPUTED", "📤 SUBMITTED"])]

            def highlight_status(row):
                if row['status'] == "⚠️ DISPUTED": return ['background-color: rgba(239, 68, 68, 0.15); color: #FCA5A5; font-weight: bold;'] * len(row)
                elif row['status'] == "📤 SUBMITTED": return ['background-color: rgba(99, 102, 241, 0.1); color: #A5B4FC;'] * len(row)
                elif row['status'] == "✅ WON": return ['background-color: rgba(16, 185, 129, 0.1); color: #6EE7B7; font-weight: bold;'] * len(row)
                return ['color: #10B981;'] * len(row)

            st.dataframe(
                display_df[['order_id', 'created_at', 'customer', 'amount', 'status']].style.apply(highlight_status, axis=1),
                use_container_width=True, hide_index=True,
                column_config={"amount": st.column_config.NumberColumn("Amount", format="$%.2f")}
            )

            st.divider()

            # --- ACTION CENTER ---
            col_left, col_right = st.columns([1.3, 1])
            with col_left:
                st.subheader("🎯 Action Queue")
                df_sorted = df.sort_values(by='status', ascending=False) 
                selected_id = st.selectbox("Select Transaction", options=df_sorted['order_id'].tolist())
                current_order = df[df['order_id'] == selected_id].iloc[0]
                
                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    if current_order['status'] == "⚠️ DISPUTED":
                        if st.button("🚀 SUBMIT COUNTER-EVIDENCE", type="primary", use_container_width=True):
                            update_dispute_status(current_order['order_id'], "📤 SUBMITTED")
                    elif current_order['status'] == "📤 SUBMITTED":
                        if st.button("🏆 MARK CASE AS WON", use_container_width=True):
                            update_dispute_status(current_order['order_id'], "✅ WON")
                    else:
                        st.button("🔍 SCAN FOR FRAUD", use_container_width=True)
                with c_b2:
                    st.button("📥 EXPORT DOSSIER (PDF)", use_container_width=True)

                st.write("---")
                st.subheader(f"🕵️ Audit Trail: {current_order['order_id']}")
                st.markdown(f'<div class="audit-log">✅ Order ID: {current_order["order_id"]}<br>🤖 Analysis: {current_order["status"]}</div>', unsafe_allow_html=True)

            with col_right:
                st.markdown(f"""
                    <div class="evidence-paper">
                        <h2 style="text-align:center; text-decoration: underline;">LEGAL EVIDENCE</h2>
                        <p style="text-align:right;">REF: {current_order['order_id']}</p>
                        <hr>
                        <p><strong>CUSTOMER:</strong> {current_order['customer']}</p>
                        <p><strong>VALUE:</strong> ${current_order['amount']}</p>
                        <hr>
                        <h4>COMPLIANCE RECORD:</h4>
                        <p>• Verified Device Fingerprint Auth</p>
                        <p>• Delivery Success: 100%</p>
                        <br><br>
                        <div style="border: 2px solid black; padding: 10px; text-align: center; font-weight: bold;">{current_order['status'].upper()}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No orders found. Simulate a transaction in the sidebar.")
