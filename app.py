import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Tyre Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (FORCE FRESH DATA)
# -----------------------------
def load_data():
    base_url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=csv"
    
    # Avoid caching
    url = f"{base_url}&t={int(time.time())}"
    
    df = pd.read_csv(url)
    return df

df = load_data()

# -----------------------------
# CLEAN DATA (IMPORTANT)
# -----------------------------
df = df.fillna("-")

numeric_cols = [
    "No of tyres sold till date",
    "No of mould",
    "OD",
    "SW",
    "NSD",
    "RIM"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

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
# IMAGE
# -----------------------------
def format_image_name(name):
    return name.replace("/", "_").replace(" ", "_")

def get_image_url(name):
    base = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    return base + format_image_name(name) + ".jpg"

img_url = get_image_url(selected_tyre)

# -----------------------------
# FORMAT VALUE FUNCTION
# -----------------------------
def format_value(val):
    if pd.isna(val) or val == "":
        return "-"
    if isinstance(val, (int, float)):
        return f"{val:,.0f}"
    return val

# -----------------------------
# CARD UI
# -----------------------------
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

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([1, 2])

# LEFT SIDE
with col1:
    st.subheader("📸 Tyre Image")
    st.image(img_url, use_container_width=True)

# RIGHT SIDE
with col2:
    st.subheader(row["Tyre_Name"])
    st.markdown("---")

    # ROW 1
    c1, c2, c3 = st.columns(3)
    c1.markdown(card("Phase", row.get("Phase")), unsafe_allow_html=True)
    c2.markdown(card("Size", row.get("Size")), unsafe_allow_html=True)
    c3.markdown(card("Pattern", row.get("Pattern")), unsafe_allow_html=True)

    # ROW 2
    c1, c2, c3 = st.columns(3)
    c1.markdown(card("India FG code", row.get("India FG code")), unsafe_allow_html=True)
    c2.markdown(card("US FG code", row.get("US FG code")), unsafe_allow_html=True)
    c3.markdown(card("SOP date", row.get("SOP date")), unsafe_allow_html=True)

    # ROW 3
    c1, c2, c3 = st.columns(3)
    c1.markdown(card("Tyres Sold", row.get("No of tyres sold till date")), unsafe_allow_html=True)
    c2.markdown(card("No of mould", row.get("No of mould")), unsafe_allow_html=True)
    c3.markdown(card("Benchmark", row.get("Benchmark tyres")), unsafe_allow_html=True)

    # ROW 4
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(card("OD", row.get("OD")), unsafe_allow_html=True)
    c2.markdown(card("SW", row.get("SW")), unsafe_allow_html=True)
    c3.markdown(card("NSD", row.get("NSD")), unsafe_allow_html=True)
    c4.markdown(card("RIM", row.get("RIM")), unsafe_allow_html=True)

# -----------------------------
# REFRESH BUTTON
# -----------------------------
if st.button("🔄 Refresh Data"):
    st.rerun()

# -----------------------------
# FULL TABLE
# -----------------------------
with st.expander("📊 View Full Data"):
    st.dataframe(df)
