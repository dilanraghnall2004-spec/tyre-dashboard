import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Tyre Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (Google Sheets / GitHub / Local)
# -----------------------------
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.markdown("## 🚛 Tyre Dashboard")
st.markdown("---")

# -----------------------------
# GET TYRE FROM URL
# -----------------------------
query_params = st.query_params
selected_tyre = query_params.get("tyre", df["Tyre_Name"].iloc[0])

# Dropdown
selected_tyre = st.selectbox("Select Tyre", df["Tyre_Name"], 
                             index=list(df["Tyre_Name"]).index(selected_tyre))

# Get row
row = df[df["Tyre_Name"] == selected_tyre].iloc[0]

# -----------------------------
# IMAGE FUNCTION (JPG + JPEG)
# -----------------------------
def get_image_url(tyre_name):
    base = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    
    name = tyre_name.replace(" ", "_")
    
    jpg = base + name + ".jpg"
    jpeg = base + name + ".jpeg"
    
    return jpg, jpeg

jpg_url, jpeg_url = get_image_url(selected_tyre)

# -----------------------------
# MAIN LAYOUT (SIDE BY SIDE)
# -----------------------------
col1, col2 = st.columns([1, 2])

# LEFT → IMAGE
with col1:
    st.markdown("### 📸 Tyre Image")

    # Try jpg first, then jpeg
    try:
        st.image(jpg_url, use_container_width=True)
    except:
        try:
            st.image(jpeg_url, use_container_width=True)
        except:
            st.warning("Image not found")

# RIGHT → DETAILS
with col2:
    st.markdown(f"## {row['Tyre_Name']}")
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

    card("Phase", row["Phase"])
    card("Size", row["Size"])
    card("Pattern", row["Pattern"])
    card("India FG code", row.get("India FG code", "—"))
    card("US FG code", row.get("US FG code", "—"))
    card("SOP date", row.get("SOP date", "—"))
    card("No of tyres sold till date", row.get("No of tyres sold till date", "—"))
    card("No of mould", row.get("No of mould", "—"))
    card("Benchmark tyres", row.get("Benchmark tyres", "—"))
    card("OD", row.get("OD", "—"))
    card("SW", row.get("SW", "—"))
    card("NSD", row.get("NSD", "—"))
    card("RIM", row.get("RIM", "—"))

# -----------------------------
# REFRESH BUTTON
# -----------------------------
st.button("🔄 Refresh Data")

# -----------------------------
# FULL DATA TABLE
# -----------------------------
with st.expander("📊 View Full Data"):
    st.dataframe(df)
