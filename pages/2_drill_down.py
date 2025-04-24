import streamlit as st

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()
import streamlit as st
import pandas as pd
import plotly.express as px

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()

st.title("🔍 Revenue Drilldown by Category")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], key="drilldown")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.title()
    if "Revenue" not in df.columns and {"Quantity", "Unitprice"}.issubset(df.columns):
        df["Revenue"] = df["Quantity"] * df["Unitprice"]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(inplace=True)

    if "Category" in df.columns:
        fig = px.bar(df, x="Category", y="Revenue", color="Category", title="Revenue per Category")
        st.plotly_chart(fig, use_container_width=True)
