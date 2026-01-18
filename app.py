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

# --- 2. PREMIUM UI STYLING ---
st.set_page_config(page_title="Creator OS | Premium", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    /* Global Deep Dark Theme */
    .stApp { background-color: #0E1117; color: #E5E7EB; }
    
    /* Glassmorphism Cards */
    .metric-card {
        background: rgba(31, 41, 55, 0.7);
        padding: 24px;
        border-radius: 12px;
        border: 1px solid rgba(75, 85, 99, 0.3);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom Evidence Dossier (Paper Look) */
    .evidence-paper {
        background-color: #FFFFFF;
        color: #111827;
        padding: 40px;
        border-radius: 2px;
        font-family: 'Courier New', Courier, monospace;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        line-height: 1.6;
    }
    
    /* Status Labels */
    .status-high { color: #EF4444; font-weight: bold; border: 1px solid #EF4444; padding: 2px 6px; border-radius: 4px; }
    .status-low { color: #10B981; font-weight: bold; border: 1px solid #10B981; padding: 2px 6px; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/9424/9424443.png", width=60)
    st.title("Creator OS")
    st.caption("v3.5 // Enterprise Suite")
    st.divider()
    
    page = st.radio("Navigation", ["🛡️ Revenue Shield", "👻 Ghost Hunter", "📊 Unified Data"])
    
    st.divider()
    if db_connected:
        st.success("🟢 DB Connected")
        if st.button("➕ Generate Real-Sim Order"):
            # Adds more varied data for a better simulation
            amount = float(datetime.datetime.now().second * 10) + 9.99
            risk = "High" if amount > 300 else "Low"
            new_data = {
                "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
                "customer": f"user_{datetime.datetime.now().second}@vibe.io",
                "amount": amount,
                "status": risk
            }
            supabase.table("orders").insert(new_data).execute()
            st.toast(f"Logged {risk} Risk Order: ${amount}", icon="✅")
            time.sleep(0.5)
            st.rerun()
    else:
        st.warning("🔴 DB Missing")

# ==========================================
# MODULE 1: REVENUE SHIELD (Polished)
# ==========================================
if page == "🛡️ Revenue Shield":
    st.title("🛡️ Revenue Shield")
    st.markdown("Automated chargeback defense and transaction risk scoring.")
    
    # Hero Metrics
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Total Protected", "$28,450", "+12%")
    with c2: st.metric("Win Rate", "82%", "+4%")
    with c3: st.metric("Open Disputes", "3", "-1")

    st.divider()
    
    col_logs, col_view = st.columns([1.2, 1])
    
    with col_logs:
        st.subheader("Live Transaction Feed")
        if db_connected:
            try:
                res = supabase.table("orders").select("*").order("created_at", desc=True).limit(8).execute()
                df = pd.DataFrame(res.data)
                # Display with color-coded risk
                st.dataframe(df[['order_id', 'amount', 'status', 'customer']], 
                             use_container_width=True, hide_index=True)
            except:
                st.info("Log into Supabase to view live data.")
        
        st.markdown("---")
        st.info("⚠️ **Alert:** Order #994-A matches 'Friendly Fraud' behavior patterns.")
        if st.button("BUILD EVIDENCE CASE"):
            st.session_state['show_case'] = True

    with col_view:
        if st.session_state.get('show_case'):
            st.markdown("""
                <div class="evidence-paper">
                    <h3 style="text-align:center; text-decoration: underline;">EXHIBIT A: TRANSACTION LOGS</h3>
                    <p style="text-align:right;"><strong>REF:</strong> #994-A</p>
                    <p><strong>SUBJECT:</strong> Digital Product Delivery Verification</p>
                    <hr>
                    <p><strong>1. PROOF OF ACCESS:</strong> User logged in from IP <b>192.168.1.1</b> at 14:02 UTC. This IP matches the billing address on file.</p>
                    <p><strong>2. CONTENT CONSUMPTION:</strong> User accessed 'Module 1: Getting Started' and completed the 15-minute video training.</p>
                    <p><strong>3. DOWNLOAD CONFIRMATION:</strong> Digital asset <i>'Creator_Assets_v1.zip'</i> was successfully downloaded at 14:20 UTC.</p>
                    <br>
                    <p><strong>VERDICT:</strong> Product was received and utilized. Claim 'Product Not Received' is factually incorrect.</p>
                    <div style="border: 2px solid black; padding: 15px; text-align: center; margin-top: 20px;">
                        <b>[ AUTO-SUBMITTED TO STRIPE/PLATFORM ]</b>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="height: 400px; display: flex; align-items: center; justify-content: center; border: 2px dashed #374151; border-radius: 10px;">
                    <p style="color: #6B7280;">Select an flagged order to view the evidence case.</p>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# MODULE 2: GHOST HUNTER (Polished)
# ==========================================
elif page == "👻 Ghost Hunter":
    st.title("👻 Ghost Hunter AI")
    st.markdown("Monitoring community engagement to prevent subscription churn.")
    
    # Retention Pulse
    chart_data = pd.DataFrame({'days': range(10), 'activity': [30, 45, 40, 60, 55, 70, 65, 80, 75, 90]})
    st.area_chart(chart_data.set_index('days'), height=150, color="#10B981")
    
    st.divider()
    
    st.subheader("High Risk Members")
    risk_users = [
        {"User": "@CryptoKing_99", "Risk": "Critical", "Reason": "0 logins in 14 days", "Score": 12},
        {"User": "Sarah_Designs", "Risk": "Medium", "Reason": "Left VIP Discord", "Score": 34},
        {"User": "MikeTrading", "Risk": "High", "Reason": "Payment Method Expiring", "Score": 18},
    ]
    st.dataframe(pd.DataFrame(risk_users), use_container_width=True, hide_index=True, column_config={
        "Score": st.column_config.ProgressColumn("Engagement", min_value=0, max_value=100, color="red")
    })
    
    st.button("🚀 DEPLOY RECOVERY PROTOCOL", type="primary", use_container_width=True)

# ==========================================
# MODULE 3: UNIFIED DATA (Polished)
# ==========================================
elif page == "📊 Unified Data":
    st.title("📊 Unified Data")
    st.markdown("Visualizing the flow from Ad Spend to Net Profit.")
    
    # THE CLEAR FLOW MAP
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
        node = dict(pad=20, thickness=20, label=labels, color="#818CF8"),
        link = dict(source=source, target=target, value=value, color=link_colors)
    )])
    fig.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
    
    # ROI Leaderboard
    c1, c2 = st.columns(2)
    with c1:
        st.success("🏆 **Best Channel:** YouTube (Organic)")
    with c2:
        st.error("📉 **Worst Channel:** TikTok Ads")
