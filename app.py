import streamlit as st
import pandas as pd
import urllib.parse

# 🔗 Load data from Google Sheets (LIVE)
@st.cache_data(ttl=10)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=xlsx"
    df = pd.read_excel(url, engine="openpyxl")
    return df

df = load_data()

# UI
st.set_page_config(page_title="Tyre Dashboard", layout="wide")
st.title("🚛 Tyre Dashboard")

# URL param (for PPT buttons)
query_params = st.query_params
tyre = query_params.get("tyre", None)

if tyre:
    tyre = urllib.parse.unquote(tyre)
    selected_tyre = tyre
else:
    selected_tyre = st.selectbox("Select Tyre", df['Tyre_Name'])

# Filter data
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

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Full data
with st.expander("📋 View Full Data"):
    st.dataframe(df)
