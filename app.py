import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Tyre Dashboard", layout="wide")

def load_data():
    base_url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=csv"

    url = f"{base_url}&t={int(time.time())}"
    
    df = pd.read_csv(url)
    return df

df = load_data()

df = df.fillna("-")

for col in df.columns:
    try:
        df[col] = pd.to_numeric(df[col])
    except:
        pass

st.title("🚛 Tyre Dashboard")
st.markdown("---")

query_params = st.query_params
selected_tyre = query_params.get("tyre", df["Tyre_Name"].iloc[0])

selected_tyre = st.selectbox(
    "🔍 Select Tyre",
    df["Tyre_Name"],
    index=list(df["Tyre_Name"]).index(selected_tyre)
)

row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

def format_image_name(name):
    return name.replace("/", "_").replace(" ", "_")

def get_image_url(name):
    base = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    return base + format_image_name(name) + ".jpg"

img_url = get_image_url(selected_tyre)

def format_value(val):
    if pd.isna(val) or val == "":
        return "-"
    if isinstance(val, (int, float)):
        return f"{val:,.0f}"
    return val

def card(title, value):
    value = format_value(value)
    return f"""
    <div style="
        background:#1e1e2f;
        padding:15px;
        border-radius:12px;
        margin-bottom:10px;
        height:100%;
        box-shadow:0 2px 6px rgba(0,0,0,0.3);">
        <b style="color:#00d4ff;">{title}</b><br>
        <span style="color:white;font-size:16px;">{value}</span>
    </div>
    """

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📸 Tyre Image")
    st.image(img_url, use_container_width=True)

with col2:
    st.subheader(row["Tyre_Name"])
    st.markdown("---")

    skip_cols = ["Tyre_Name"]

    columns = [c for c in df.columns if c not in skip_cols]

    for i in range(0, len(columns), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(columns):
                col_name = columns[i + j]
                cols[j].markdown(
                    card(col_name, row.get(col_name)),
                    unsafe_allow_html=True
                )

if st.button("🔄 Refresh Data"):
    st.rerun()

with st.expander("📊 View Full Data"):
    st.dataframe(df)
