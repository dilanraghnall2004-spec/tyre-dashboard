import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# LOAD DATA (from GitHub)
# =========================
@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/tyre_data.xlsx"
    return pd.read_excel(url)

df = load_data()

# =========================
# TITLE
# =========================
st.title("🚛 Tyre Dashboard")

# =========================
# SELECT TYRE
# =========================
selected_tyre = st.selectbox("Select Tyre", df["Tyre_Name"])

row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

# =========================
# IMAGE FUNCTION
# =========================
def get_image_url(tyre_name):
    name = tyre_name.replace(" ", "_")
    base = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    return base + name + ".jpg"

image_url = get_image_url(selected_tyre)

# =========================
# MAIN LAYOUT
# =========================
col1, col2 = st.columns([1, 2])

# ---- LEFT: IMAGE ----
with col1:
    st.subheader("📸 Tyre Image")

    st.image(
        image_url,
        use_container_width=True
    )

# ---- RIGHT: DETAILS ----
with col2:
    st.subheader(selected_tyre)

    st.markdown("---")

    # COMPACT GRID (2 columns)
    c1, c2 = st.columns(2)

    with c1:
        st.info(f"**Phase**\n\n{row.get('Phase', '-')}")
        st.info(f"**Size**\n\n{row.get('Size', '-')}")
        st.info(f"**Pattern**\n\n{row.get('Pattern', '-')}")
        st.info(f"**India FG code**\n\n{row.get('India FG code', '-')}")

    with c2:
        st.info(f"**US FG code**\n\n{row.get('US FG code', '-')}")
        st.info(f"**SOP date**\n\n{row.get('SOP date', '-')}")
        st.info(f"**Tyres Sold**\n\n{row.get('No of tyres sold till date', '-')}")
        st.info(f"**Moulds**\n\n{row.get('No of mould', '-')}")

# =========================
# FULL DATA (OPTIONAL)
# =========================
with st.expander("📋 View Full Data"):
    st.dataframe(df, use_container_width=True)
