import streamlit as st
import pandas as pd
import urllib.parse
import os

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Tyre Dashboard", layout="wide")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #1f4e79;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
@st.cache_data(ttl=10)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=xlsx"
    return pd.read_excel(url, engine="openpyxl")

df = load_data()

# ------------------ HEADER ------------------
st.markdown('<div class="main-title">🚛 Tyre Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔍 Select Tyre")

query_params = st.query_params
tyre = query_params.get("tyre", None)

if tyre:
    tyre = urllib.parse.unquote(tyre)
    selected_tyre = tyre
else:
    selected_tyre = st.sidebar.selectbox("Choose Tyre", df['Tyre_Name'])

# ------------------ FILTER DATA ------------------
data = df[df['Tyre_Name'] == selected_tyre]

# ------------------ IMAGE FUNCTION ------------------
def get_image_name(tyre):
    name = tyre.replace("/", "_").replace(" ", "_")
    
    if os.path.exists(f"images/{name}.jpg"):
        return f"images/{name}.jpg"
    elif os.path.exists(f"images/{name}.jpeg"):
        return f"images/{name}.jpeg"
    else:
        return None

# ------------------ MAIN CONTENT ------------------
if data.empty:
    st.error("❌ Tyre not found!")
else:
    st.subheader(selected_tyre)

    col1, col2 = st.columns([1, 2])

    # 📸 IMAGE
    image_path = get_image_name(selected_tyre)

    if image_path:
        col1.image(image_path, use_container_width=True)
    else:
        col1.warning("No image available")

    # 📊 DETAILS
    with col2:
        for col in data.columns:
            if col == "Tyre_Name":
                continue

            value = data.iloc[0][col]

            if pd.isna(value):
                continue

            st.markdown(f"""
            <div class="card">
                <b>{col}</b><br>{value}
            </div>
            """, unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("© 2026 Tyre Dashboard | Developed by Dilaa")

# ------------------ REFRESH BUTTON ------------------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ------------------ FULL DATA VIEW ------------------
with st.expander("📋 View Full Data"):
    st.dataframe(df)
