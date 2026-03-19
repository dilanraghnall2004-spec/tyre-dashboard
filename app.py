import streamlit as st
import pandas as pd
import urllib.parse

# ✅ Load Excel from GitHub RAW (WORKING)
@st.cache_data(ttl=30)
def load_data():
    url = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/tyre_data.xlsx"
    df = pd.read_excel(url, engine="openpyxl")
    return df

df = load_data()

# UI
st.set_page_config(page_title="Tyre Dashboard", layout="wide")
st.title("🚛 Tyre Dashboard")

# Get tyre from PPT link
query_params = st.query_params
tyre = query_params.get("tyre", None)

if tyre:
    tyre = urllib.parse.unquote(tyre)
    selected_tyre = tyre
else:
    selected_tyre = st.selectbox("Select Tyre", df['Tyre_Name'])

# Filter
data = df[df['Tyre_Name'] == selected_tyre]

if data.empty:
    st.error("❌ Tyre not found!")
else:
    st.subheader(f"Details for: {selected_tyre}")

    col1, col2 = st.columns(2)

    for i, col in enumerate(data.columns):
        if col == "Tyre_Name":
            continue

        value = data.iloc[0][col]

        if pd.isna(value):
            continue

        if i % 2 == 0:
            col1.write(f"**{col}:** {value}")
        else:
            col2.write(f"**{col}:** {value}")

# Refresh
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Full data
with st.expander("📋 View Full Data"):
    st.dataframe(df)
