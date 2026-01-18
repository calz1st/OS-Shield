import streamlit as st
import pandas as pd
from supabase import create_client, Client
import datetime

# --- DATABASE CONNECTION ---
# This pulls the keys from your Streamlit Secrets automatically
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Creator OS | Database Mode", layout="wide")

st.title("🛡️ Creator OS: Persistent Simulation")
st.caption("Connected to Supabase Database")

# --- FUNCTION: SAVE SIMULATED DATA ---
def save_simulated_order():
    # Create a fake order
    new_order = {
        "created_at": str(datetime.datetime.now()),
        "order_id": f"#{datetime.datetime.now().strftime('%M%S')}",
        "customer": "simulated_user@test.com",
        "amount": 499.00,
        "status": "Protected"
    }
    # This sends it to your database table named 'orders'
    # NOTE: You must create a table named 'orders' in Supabase UI first!
    try:
        supabase.table("orders").insert(new_order).execute()
        st.success("Order saved to Database!")
    except Exception as e:
        st.error(f"Error: {e}")

# --- SIDEBAR ---
with st.sidebar:
    if st.button("➕ Generate Simulated Order"):
        save_simulated_order()

# --- MAIN VIEW: FETCH DATA FROM DATABASE ---
st.subheader("📋 Real-Time Database Feed")

# Fetch data from Supabase
response = supabase.table("orders").select("*").order("created_at", desc=True).execute()
db_data = response.data

if db_data:
    df = pd.DataFrame(db_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No data in database yet. Click the button in the sidebar to simulate an order!")
