import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/dilanragnhall2004-spec/tyre-dashboard/main/tyre_data.xlsx"
    return pd.read_excel(url)

df = load_data()

# =========================
# TITLE
# =========================
st.title("🚛 Tyre Dashboard")

# =========================
# SAFE SELECTBOX (FIXED ERROR)
# =========================
tyre_list = df["Tyre_Name"].dropna().tolist()

selected_tyre = st.selectbox(
    "Select Tyre",
    tyre_list,
    index=0   # ✅ ALWAYS SAFE
)

# =========================
# GET DATA
# =========================
row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

# =========================
# IMAGE FUNCTION (GITHUB RAW)
# =========================
def get_image_url(tyre_name):
    filename = tyre_name.replace(" ", "_") + ".jpg"
    return f"https://raw.githubusercontent.com/dilanragnhall2004-spec/tyre-dashboard/main/images/{filename}"

image_url = get_image_url(selected_tyre)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1, 2])

# LEFT → IMAGE
with col1:
    st.subheader("📸 Tyre Image")
    st.image(image_url, use_container_width=True)

# RIGHT → DETAILS GRID
with col2:
    st.subheader(selected_tyre)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Phase**")
        st.write(row.get("Phase", "-"))

        st.markdown("**Size**")
        st.write(row.get("Size", "-"))

        st.markdown("**Pattern**")
        st.write(row.get("Pattern", "-"))

        st.markdown("**India FG code**")
        st.write(row.get("India FG code", "-"))

    with c2:
        st.markdown("**US FG code**")
        st.write(row.get("US FG code", "-"))

        st.markdown("**SOP date**")
        st.write(row.get("SOP date", "-"))

        st.markdown("**Tyres Sold**")
        st.write(row.get("No of tyres sold till date", "-"))

        st.markdown("**Moulds**")
        st.write(row.get("No of mould", "-"))
