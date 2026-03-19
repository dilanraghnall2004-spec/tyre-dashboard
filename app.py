import streamlit as st
import pandas as pd
import urllib.parse

# 🔗 Load Excel from OneDrive (LIVE AUTO UPDATE)
@st.cache_data(ttl=30)
def load_data():
    url = "https://onedrive.live.com/download?resid=E8C5E0FA2C7E7634!122&authkey=!BnZTu7"
    df = pd.read_excel(url, engine="openpyxl")
    return df

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

# ⚠️ Handle error
if data.empty:
    st.error("❌ Tyre not found!")
else:
    st.subheader(f"Details for: {selected_tyre}")

    # 📦 Clean layout (2 columns)
    col1, col2 = st.columns(2)

    for i, col in enumerate(data.columns):

        # ❌ Skip Tyre_Name (already shown)
        if col == "Tyre_Name":
            continue

        value = data.iloc[0][col]

        # ❌ Skip empty values
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

# 📋 Optional full data
with st.expander("📋 View Full Data"):
    st.dataframe(df)
