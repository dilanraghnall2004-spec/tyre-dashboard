import streamlit as st
import pandas as pd
import urllib.parse

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Tyre Dashboard", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.card {
    background-color:#262730;
    padding:12px;
    border-radius:8px;
    margin-bottom:10px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data(ttl=10)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1S-_eEnKvv4A08TBtzF_2lLj8FzItXZOPRchIfIKHV1E/export?format=xlsx"
    return pd.read_excel(url, engine="openpyxl")

df = load_data()

# ---------------- HEADER ----------------
st.title("🚛 Tyre Dashboard")
st.markdown("---")

# ---------------- GET TYRE FROM URL ----------------
query_params = st.query_params
tyre = query_params.get("tyre", None)

if tyre:
    tyre = urllib.parse.unquote(tyre)
    selected_tyre = tyre
else:
    selected_tyre = st.selectbox("Select Tyre", df['Tyre_Name'])

# ---------------- FILTER DATA ----------------
data = df[df['Tyre_Name'] == selected_tyre]

# ---------------- IMAGE FUNCTION (GITHUB RAW) ----------------
def get_image_url(tyre):
    name = tyre.replace("/", "_").replace(" ", "_")
    base_url = "https://raw.githubusercontent.com/dilanraghnall2004-spec/tyre-dashboard/main/images/"
    return base_url + name + ".jpg"

# ---------------- MAIN DISPLAY ----------------
if data.empty:
    st.error("❌ Tyre not found")
else:
    col1, col2 = st.columns([1.2, 1.8])

    # IMAGE
    with col1:
        image_url = get_image_url(selected_tyre)
        st.image(image_url, use_container_width=True)

    # DETAILS
    with col2:
        st.markdown(f"## {selected_tyre}")
        st.markdown("---")

        for col in data.columns:
            if col == "Tyre_Name":
                continue

            value = data.iloc[0][col]

            if pd.isna(value):
                continue

            st.markdown(f"""
            <div class="card">
                <b style="color:#00c6ff;">{col}</b><br>
                {value}
            </div>
            """, unsafe_allow_html=True)

# ---------------- SHARE LINK ----------------
st.markdown("---")

encoded = urllib.parse.quote(selected_tyre)
link = f"https://tyre-dashboard-5wfsa7tiw8f5wbfhlk2uz7.streamlit.app/?tyre={encoded}"

st.subheader("🔗 Share this Tyre")
st.code(link)

# ---------------- REFRESH ----------------
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ---------------- FULL DATA ----------------
with st.expander("📋 View Full Data"):
    st.dataframe(df)
