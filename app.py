import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIGURATION (The "Dark Mode" Look) ---
st.set_page_config(
    page_title="Creator OS",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS to force the "Professional Dark" look
st.markdown("""
    <style>
    .stApp {
        background-color: #111827;
        color: white;
    }
    .status-badge {
        color: #10B981;
        font-weight: bold;
        padding: 5px;
        border: 1px solid #10B981;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE TOP HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛡️ Creator OS | Revenue Shield")
    st.markdown("🟢 **System Active & Monitoring**")
with col2:
    st.metric(label="ROI Multiplier", value="12x")

st.divider()

# --- 3. THE DASHBOARD METRICS ---
# We create three columns for the "Cards"
col_def, col_rev, col_tax = st.columns(3)

with col_def:
    st.subheader("Dispute Defender")
    # This creates the Donut Chart
    fig = go.Figure(data=[go.Pie(labels=['Won', 'Lost'], values=[75, 25], hole=.6)])
    fig.update_layout(height=150, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.button("View Evidence Files")

with col_rev:
    st.subheader("Revenue Recovered")
    st.metric(label="Total Saved", value="$14,250.00", delta="+ $1,200 this week")
    # Simple area chart for visuals
    st.area_chart([5000, 7200, 9500, 11200, 13000, 14250])

with col_tax:
    st.subheader("Global Compliance")
    st.info("⚠️ Approaching Tax Threshold in Germany")
    st.progress(0.9)
    st.caption("€9,000 / €10,000 Limit")

# --- 4. THE ACTIVITY FEED ---
st.subheader("Recent Activity Log")
# Creating a fake table of data
data = {
    "Time": ["2 min ago", "1 hour ago", "4 hours ago"],
    "Event": ["🛡️ Fraud Blocked", "⚖️ Dispute Won", "📄 Evidence Sent"],
    "Status": ["Blocked", "Success", "Submitted"]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)
