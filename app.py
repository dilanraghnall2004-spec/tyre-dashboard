import streamlit as st
import pandas as pd
import urllib.parse
import requests
from io import BytesIO

# 🔗 Load Excel from OneDrive (LIVE + FIXED)
@st.cache_data(ttl=30)
def load_data():
    url = "https://onedrive.live.com/download?resid=E8C5E0FA2C7E7634!122&authkey=!BnZTu7"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # check if download successful
        
        file_bytes = BytesIO(response.content)
        df = pd.read_excel(file_bytes, engine="openpyxl")
        return df
    
    except Exception as e:
        st.error("❌ Error loading Excel from OneDrive")
        st.stop()

# Load data
df = load_data()

# 🖥️ Page setup
st.set_page_config(page_title="Tyre Dashboard", layout="wide")

st.title("🚛 Tyre Dashboard")

# 🔍 Get tyre from URL (for PPT buttons)
query_params = st.query_params
tyre = query_params.get("tyre", None)

# Decode URL text
if tyre:
    tyre = urllib.parse.unquote(tyre)
    selected_tyre = tyre
else:
    selected_tyre = st.selectbox("Select Tyre", df['Tyre_Name'])

# 📊 Filter data
data = df[df['Tyre_Name'] == selected_tyre]

# ⚠️ Handle case
if data.empty:
    st.error("❌ Tyre not found!")
else:
    st.subheader(f"Details for: {selected_tyre}")

    # 📦 Layout (2 columns)
    col1, col2 = st.columns(2)

    for i, col in enumerate(data.columns):

        # Skip repeated column
        if col == "Tyre_Name":
            continue

        value = data.iloc[0][col]

        # Skip empty values
        if pd.isna(value):
            continue

        if i % 2 == 0:
            col1.write(f"**{col}:** {value}")
        else:
            col2.write(f"**{col}:** {value}")

# 🔄 Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# 📋 Full dataset view
with st.expander("📋 View Full Data"):
    st.dataframe(df)
