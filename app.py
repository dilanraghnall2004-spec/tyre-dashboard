import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tyre Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (Google Sheet)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=csv"
    return pd.read_csv(url)

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("🚛 Tyre Dashboard")
st.markdown("---")

# -----------------------------
# SELECT TYRE
# -----------------------------
query_params = st.query_params
selected_tyre = query_params.get("tyre", df["Tyre_Name"].iloc[0])

selected_tyre = st.selectbox(
    "Select Tyre",
    df["Tyre_Name"],
    index=list(df["Tyre_Name"]).index(selected_tyre)
)

row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

# -----------------------------
# IMAGE NAME FIX (IMPORTANT)
# -----------------------------
def format_image_name(name):
    name = name.replace("/", "_")   # 295/75 → 295_75
    name = name.replace(" ", "_")   # spaces → _
    # DO NOT replace dot (.) because your file has 22.5
    return name

def get_image_url(name):
    base = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    return base + format_image_name(name) + ".jpg"

img_url = get_image_url(selected_tyre)

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([1, 2])

# IMAGE
with col1:
    st.subheader("📸 Tyre Image")
    st.image(img_url, use_container_width=True)

# DETAILS
with col2:
    st.subheader(row["Tyre_Name"])
    st.markdown("---")

    def card(title, value):
        st.markdown(f"""
        <div style="
            background:#1e1e2f;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;">
            <b style="color:#00d4ff;">{title}</b><br>
            <span style="color:white;">{value}</span>
        </div>
        """, unsafe_allow_html=True)

    card("Phase", row.get("Phase", "-"))
    card("Size", row.get("Size", "-"))
    card("Pattern", row.get("Pattern", "-"))
    card("India FG code", row.get("India FG code", "-"))
    card("US FG code", row.get("US FG code", "-"))
    card("SOP date", row.get("SOP date", "-"))
    card("No of tyres sold till date", row.get("No of tyres sold till date", "-"))
    card("No of mould", row.get("No of mould", "-"))
    card("Benchmark tyres", row.get("Benchmark tyres", "-"))
    card("OD", row.get("OD", "-"))
    card("SW", row.get("SW", "-"))
    card("NSD", row.get("NSD", "-"))
    card("RIM", row.get("RIM", "-"))

# -----------------------------
# REFRESH
# -----------------------------
st.button("🔄 Refresh Data")

# -----------------------------
# FULL TABLE
# -----------------------------
with st.expander("📊 View Full Data"):
    st.dataframe(df)
