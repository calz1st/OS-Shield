import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client, Client
import datetime
import time

# --- 1. THE DATABASE CONNECTION ---
db_connected = False
try:
    if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        supabase: Client = create_client(url, key)
        db_connected = True
except Exception:
    db_connected = False

# --- 2. PAGE SETTINGS & STYLING ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    /* Evidence Dossier Styling */
    .evidence-paper {
        background-color: white; color: black; padding: 30px; border-radius: 5px;
        font-family: 'Courier New', monospace; box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    .status-badge { color: #10B981; font-weight: bold; border: 1px solid #10B981; padding: 2px 8px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🛡️ Creator OS")
    st.caption("v3.3 Hybrid Suite")
    st.divider()
    
    page = st.radio("Select Module", [
        "🛡️ Revenue Shield", 
        "👻 Ghost Hunter (Retention)", 
        "📊 Unified Data (LTV)"
    ])
    
    st.divider()
    
    if db_connected:
        st.success("🟢 Database Linked")
        # CALCULATE GLOBAL PROFIT FROM DB
        try:
            res = supabase.table("orders").select("amount").execute()
            total_val = sum([item['amount'] for item in res.data]) if res.data else 0
            st.metric("Global Protected Profit", f"${total_val:,.2f}")
        except:
            pass
            
        if st.button("➕ Simulate New Order"):
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": "sim_user@vibe.com",
                "amount": 499.0,
                "status": "Protected"
            }
            supabase.table("orders").insert(new_data).execute()
            st.toast("Simulated Order Saved!", icon="✅")
            time.sleep(1)
            st.rerun()
    else:
        st.warning("🔴 Database Not Linked")

# ==========================================
# MODULE 1: REVENUE SHIELD (Back to Original)
# ==========================================
if page == "🛡️ Revenue Shield":
    col_header, col_roi = st.columns([3, 1])
    with col_header:
        st.title("Revenue Shield")
        st.caption("Active Protection • Chargeback Defense")
    with col_roi:
        st.metric("ROI Multiplier", "12.4x", delta="Stable")
    
    st.divider()
    
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("Live Defense Feed")
        if db_connected:
            try:
                response = supabase.table("orders").select("*").order("created_at", desc=True).limit(5).execute()
                if response.data:
                    df = pd.DataFrame(response.data)
                    st.dataframe(df[['order_id', 'customer', 'amount', 'status']], use_container_width=True, hide_index=True)
                else:
                    st.info("No orders in DB yet.")
            except:
                st.error("Check Supabase Table Columns!")
        
        st.write("---")
        st.write("📢 **Latest Alert:** Potential Friendly Fraud detected on #994-A.")
        if st.button("GENERATE EVIDENCE DOSSIER", type="primary", use_container_width=True):
            st.session_state['show_dossier'] = True

    with col_right:
        if st.session_state.get('show_dossier'):
            st.markdown("""
                <div class="evidence-paper">
                    <h3 style="text-align:center;">EVIDENCE DOSSIER: #994-A</h3>
                    <hr>
                    <p><strong>Customer:</strong> John Doe (j.doe@example.com)</p>
                    <p><strong>Status:</strong> <span style="color:green">MATCHED (IP & BILLING)</span></p>
                    <p><strong>Digital Custody:</strong></p>
                    <ul>
                        <li>✅ 10:05 AM - Course Login</li>
                        <li>✅ 10:15 AM - Video 1 (100% Viewed)</li>
                        <li>✅ 10:20 AM - Assets Downloaded</li>
                    </ul>
                    <div style="border:1px solid black; padding:10px; text-align:center; font-weight:bold;">
                        AUTO-SUBMITTED TO BANK
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Select 'Generate' to view the Evidence Dossier.")

# ==========================================
# MODULE 2: GHOST HUNTER (Back to Original)
# ==========================================
elif page == "👻 Ghost Hunter (Retention)":
    st.title("Ghost Hunter AI")
    st.caption("Predictive Churn Detection System")
    st.divider()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Churn Risk", "High", "+4 Members")
    m2.metric("Saved this Month", "12 Members", "+2")
    m3.metric("Retention Rate", "94%", "+1.2%")

    st.subheader("⚠️ At-Risk Member Analysis")
    risk_data = [
        {"User": "@CryptoKing_99", "Last Active": "12 Days Ago", "Health": 15, "Action": "Send Discount"},
        {"User": "Sarah_Designs", "Last Active": "8 Days Ago", "Health": 22, "Action": "Soft Nudge"},
        {"User": "MikeTrading", "Last Active": "15 Days Ago", "Health": 10, "Action": "Call/Email"},
    ]
    st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True, column_config={
        "Health": st.column_config.ProgressColumn("User Health Score", min_value=0, max_value=100)
    })
    
    if st.button("🚀 EXECUTE AUTO-RECOVERY PROTOCOL"):
        with st.status("Ghost Hunter active...", expanded=True) as status:
            st.write("Scanning Discord activity...")
            time.sleep(1)
            st.write("Sending AI-personalized DMs...")
            time.sleep(1)
            status.update(label="Recovery Sequence Complete!", state="complete")
        st.balloons()

# ==========================================
# MODULE 3: UNIFIED DATA (Back to Original)
# ==========================================
elif page == "📊 Unified Data (LTV)":
    st.title("Profit Command Center")
    st.caption("Visualizing the Customer Journey")
    st.divider()
    
    # THE CLEAR COLORFUL MAP
    st.subheader("💰 The Money Flow Map")
    
    labels = ["Meta Ads", "TikTok Ads", "YouTube", "Landing Page", "Checkout", "Lost Traffic", "Purchase", "Upsell"]
    source = [0, 1, 2,  3, 3,  4, 4,  6]
    target = [3, 3, 3,  4, 5,  6, 5,  7]
    value  = [5000, 3000, 8000, 10000, 6000, 3500, 6500, 1200]
    
    link_colors = [
        'rgba(129, 140, 248, 0.4)', 'rgba(129, 140, 248, 0.4)', 'rgba(129, 140, 248, 0.4)', 
        'rgba(52, 211, 153, 0.5)', 'rgba(239, 68, 68, 0.4)', 
        'rgba(16, 185, 129, 0.7)', 'rgba(239, 68, 68, 0.6)', 'rgba(251, 191, 36, 0.7)'
    ]

    fig = go.Figure(data=[go.Sankey(
        node = dict(pad=15, thickness=20, label=labels, color="#818CF8"),
        link = dict(source=source, target=target, value=value, color=link_colors)
    )])
    fig.update_layout(height=550, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Channel ROI Leaderboard")
    st.table(pd.DataFrame({
        "Source": ["YouTube", "Meta", "TikTok"],
        "Spend": ["$0", "$5,200", "$3,100"],
        "Revenue": ["$12,400", "$15,600", "$4,200"],
        "ROAS": ["∞", "3.0x", "1.35x"]
    }))
