import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Creator OS", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS (The Look & Feel) ---
st.markdown("""
    <style>
    /* Force Dark Mode Background */
    .stApp { background-color: #0E1117; color: white; }
    
    /* The "Paper" Look for the Evidence Dossier */
    .evidence-paper {
        background-color: white;
        color: black;
        padding: 40px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        margin-top: 20px;
    }
    .evidence-header { text-align: center; border-bottom: 2px solid black; padding-bottom: 10px; margin-bottom: 20px; }
    .evidence-item { margin-bottom: 10px; }
    .status-won { color: #10B981; font-weight: bold; }
    .status-lost { color: #EF4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛡️ Creator OS | Revenue Shield")
    st.caption("v1.2 // System Active // Monitoring Orders...")
with col2:
    st.metric(label="ROI Multiplier", value="12.4x", delta="Up this week")

st.divider()

# --- TOP METRICS ---
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Dispute Defender")
    fig = go.Figure(data=[go.Pie(labels=['Won', 'Lost'], values=[78, 22], hole=.6, marker=dict(colors=['#10B981', '#EF4444']))])
    fig.update_layout(height=130, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Money Saved")
    st.metric(label="Total Recovered", value="$14,250", delta="+$1,200")
    st.area_chart([4000, 5000, 7200, 11200, 14250], color="#10B981")

with c3:
    st.subheader("Compliance Risk")
    st.warning("⚠️ Germany: €9,000 / €10,000")
    st.progress(0.9)

st.divider()

# --- INTERACTIVE SECTION: THE "MAGIC" ---
st.subheader("⚡ Live Operations")

col_left, col_right = st.columns([1, 2])

with col_left:
    st.write("Recent Alerts:")
    # A simple activity feed
    events = [
        {"Time": "10:42 AM", "Event": "New Dispute (#994-A)", "Status": "⚠️ Action Needed"},
        {"Time": "09:15 AM", "Event": "Fraud Block (IP 192...)", "Status": "🛡️ Secure"},
        {"Time": "Yesterday", "Event": "Tax Report (UK)", "Status": "✅ Ready"},
    ]
    st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)

    st.write("---")
    st.info("💡 A new dispute (#994-A) was just detected. The system has gathered evidence.")
    
    # THE INTERACTIVE BUTTON
    if st.button("GENERATE EVIDENCE DOSSIER", type="primary", use_container_width=True):
        st.toast("Accessing Access Logs...", icon="🔍")
        time.sleep(1)
        st.toast("Compiling PDF...", icon="📄")
        time.sleep(1)
        st.session_state['show_dossier'] = True

with col_right:
    # This section only shows up AFTER you click the button
    if st.session_state.get('show_dossier'):
        st.markdown("""
            <div class="evidence-paper">
                <div class="evidence-header">
                    <h2>MERCHANT EVIDENCE SUBMISSION</h2>
                    <h4>DISPUTE REF: #994-A</h4>
                </div>
                <p><strong>MERCHANT:</strong> CreatorOS Store</p>
                <p><strong>CUSTOMER:</strong> John Doe (j.doe@example.com)</p>
                <p><strong>IP ADDRESS:</strong> 192.168.1.55 (Matched Billing)</p>
                <hr>
                <h4>DIGITAL CHAIN OF CUSTODY:</h4>
                <div class="evidence-item">✅ <strong>10:00 AM:</strong> Order Placed & Confirmed</div>
                <div class="evidence-item">✅ <strong>10:01 AM:</strong> "Welcome Email" Opened</div>
                <div class="evidence-item">✅ <strong>10:05 AM:</strong> Account Login (Device: iPhone 14)</div>
                <div class="evidence-item">✅ <strong>10:15 AM:</strong> <u>Course Module 1: 100% Completed</u></div>
                <div class="evidence-item">✅ <strong>10:20 AM:</strong> File Downloaded: "Masterclass_Assets.zip"</div>
                <hr>
                <p><strong>CONCLUSION:</strong><br>
                The customer has consumed 100% of the digital product. The claim "Product Not Received" is proven false by the server logs above.</p>
                <br>
                <div style="text-align: center; border: 2px solid black; padding: 10px; font-weight: bold;">
                    STATUS: EVIDENCE SUBMITTED TO BANK
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Placeholder before you click
        st.markdown("""
            <div style="border: 2px dashed #333; padding: 50px; text-align: center; color: #555;">
                Select an alert to view generated evidence.
            </div>
        """, unsafe_allow_html=True)
