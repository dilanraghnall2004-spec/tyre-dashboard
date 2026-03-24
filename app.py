import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# LOAD DATA
# =========================
@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/tyre_data.xlsx"
    return pd.read_excel(url)

df = load_data()

# =========================
# GET TYRE FROM URL (DO NOT CHANGE LINK)
# =========================
query_params = st.query_params
selected_tyre = query_params.get("tyre", df["Tyre_Name"].iloc[0])

# Dropdown (still works)
selected_tyre = st.selectbox(
    "Select Tyre",
    df["Tyre_Name"],
    index=df[df["Tyre_Name"] == selected_tyre].index[0]
)

row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

# =========================
# IMAGE FIX (ONLY INTERNAL)
# =========================
def get_image_url(tyre_name):
    # DO NOT change URL — only convert for image
    image_name = tyre_name.replace("/", "_").replace(" ", "_")
    return f"https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/{image_name}.jpg"

image_url = get_image_url(selected_tyre)

# =========================
# SAFE VALUE
# =========================
def get_val(col):
    val = row.get(col)
    return val if pd.notna(val) else "-"

# =========================
# LAYOUT
# =========================
st.title("🚛 Tyre Dashboard")

col1, col2 = st.columns([1, 2])

# ---- IMAGE ----
with col1:
    st.subheader("📸 Tyre Image")
    st.image(image_url, use_container_width=True)

# ---- DETAILS (COMPACT GRID) ----
with col2:
    st.subheader(selected_tyre)
    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.info(f"**Phase**\n\n{get_val('Phase')}")
        st.info(f"**Size**\n\n{get_val('Size')}")
        st.info(f"**Pattern**\n\n{get_val('Pattern')}")
        st.info(f"**India FG code**\n\n{get_val('India FG code')}")

    with c2:
        st.info(f"**US FG code**\n\n{get_val('US FG code')}")
        st.info(f"**SOP date**\n\n{get_val('SOP date')}")
        st.info(f"**Tyres Sold**\n\n{get_val('No of tyres sold till date')}")
        st.info(f"**Moulds**\n\n{get_val('No of mould')}")

# =========================
# FULL DATA
# =========================
with st.expander("📋 View Full Data"):
    st.dataframe(df, use_container_width=True)
