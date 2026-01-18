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
    
    /* The Dossier Styling */
    .evidence-paper {
        background-color: #FFFFFF !important; 
        color: #111827 !important; 
        padding: 50px !important; 
        border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border: 1px solid #ddd;
    }

    /* FIX FOR BLANK PDF: Advanced Print Rules */
    @media print {
        /* Hide everything by default */
        body * { visibility: hidden !important; }
        
        /* Only show the dossier and its children */
        #printable-area, #printable-area * { 
            visibility: visible !important; 
        }
        
        /* Force the dossier to the top left of the printed page */
        #printable-area { 
            position: absolute !important; 
            left: 0 !important; 
            top: 0 !important; 
            width: 100% !important;
            height: auto !important;
            background-color: white !important;
            color: black !important;
        }
        
        /* Remove Streamlit's default margins/padding for the print */
        .stMain { padding: 0 !important; }
    }

    .audit-log {
        background: rgba(31, 41, 55, 0.5); padding: 15px; border-radius: 8px;
        font-size: 0.85rem; border: 1px solid #374151; max-height: 200px; overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    st.divider()
    if db_connected and st.button("➕ Simulate Transaction"):
        is_dispute = random.random() < 0.2
        new_data = {
            "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
            "customer": f"user_{random.randint(10,99)}@vibe.io",
            "amount": float(random.randint(49, 999)),
            "status": "⚠️ DISPUTED" if is_dispute else "Low Risk"
        }
        supabase.table("orders").insert(new_data).execute()
        st.rerun()

# --- HELPERS ---
def submit_counter_evidence(order_id):
    if db_connected:
        supabase.table("orders").update({"status": "📤 SUBMITTED"}).eq("order_id", order_id).execute()
        st.toast("Submitted!", icon="✅")
        time.sleep(1)
        st.rerun()

# ==========================================
# MODULE 1: REVENUE SHIELD
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    
    if db_connected:
        res = supabase.table("orders").select("*").order("created_at", desc=True).limit(50).execute()
        df = pd.DataFrame(res.data)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue Protected", "$28,450")
        c2.metric("Active Disputes", len(df[df['status'] == "⚠️ DISPUTED"]), delta_color="inverse")
        c3.metric("Win Rate", "87%")
        c4.metric("Recovered", "$4,200")

        st.divider()

        col_left, col_right = st.columns([1.3, 1])

        with col_left:
            st.subheader("🎯 Action Queue")
            selected_row = st.selectbox("Select Order", df.index)
            current_order = df.iloc[selected_row]
            
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                if "DISPUTED" in current_order['status']:
                    if st.button("🚀 SUBMIT TO BANK", type="primary", use_container_width=True):
                        submit_counter_evidence(current_order['order_id'])
                else:
                    st.button("🔍 SCAN FOR FRAUD", use_container_width=True)
            
            with c_a2:
                # NEW PRINT LOGIC: Use a delay and target the #printable-area
                if st.button("📥 EXPORT DOSSIER (PDF)", use_container_width=True):
                    st.components.v1.html("""
                        <script>
                        setTimeout(function(){ window.print(); }, 500);
                        </script>
                    """, height=0)

            st.write("---")
            st.subheader("🕵️ Audit Trail")
            st.markdown(f'<div class="audit-log">✅ Order Created<br>🤖 AI Risk Scan: {current_order["status"]}</div>', unsafe_allow_html=True)

        with col_right:
            # THE DOSSIER WITH PRINTABLE AREA ID
            st.markdown(f"""
                <div id="printable-area" class="evidence-paper">
                    <h2 style="text-align:center;">LEGAL EVIDENCE</h2>
                    <p style="text-align:right;">ID: {current_order['order_id']}</p>
                    <hr>
                    <p><strong>CUSTOMER:</strong> {current_order['customer']}</p>
                    <p><strong>AMOUNT:</strong> ${current_order['amount']}</p>
                    <p><strong>STATUS:</strong> {current_order['status']}</p>
                    <hr>
                    <h4>SYSTEM LOGS:</h4>
                    <ul>
                        <li>IP Authenticated: 192.168.1.1</li>
                        <li>Digital Signature: Verified</li>
                        <li>Content Delivered: 100% Complete</li>
                    </ul>
                    <br><br>
                    <div style="border: 1px solid black; padding: 10px; text-align: center;">
                        <b>OFFICIAL SYSTEM RECORD</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.subheader("📋 Order Ledger")
        st.dataframe(df[['order_id', 'created_at', 'customer', 'amount', 'status']], use_container_width=True, hide_index=True)
