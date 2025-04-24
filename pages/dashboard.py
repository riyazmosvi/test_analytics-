import streamlit as st

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()
import streamlit as st
import pandas as pd

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()

st.title("📊 Dashboard Overview")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.title()
    if "Revenue" not in df.columns and {"Quantity", "Unitprice"}.issubset(df.columns):
        df["Revenue"] = df["Quantity"] * df["Unitprice"]
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(inplace=True)

    st.metric("💰 Total Revenue", f"${df['Revenue'].sum():,.0f}")
    st.metric("🧾 Total Orders", len(df))
    st.metric("📊 Avg Order Value", f"${df['Revenue'].mean():.2f}")
    st.dataframe(df.head())
