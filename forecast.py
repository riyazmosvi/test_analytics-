import streamlit as st

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()
import streamlit as st
import pandas as pd

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()

import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px

if not st.session_state.get("authenticated", False):
    st.warning("🔒 Please log in first from the Home page.")
    st.stop()

st.title("🔮 Revenue Forecasting")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"], key="forecast")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip().str.title()
    if "Revenue" not in df.columns and {"Quantity", "Unitprice"}.issubset(df.columns):
        df["Revenue"] = df["Quantity"] * df["Unitprice"]
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(inplace=True)

    data = df[["Date", "Revenue"]].rename(columns={"Date": "ds", "Revenue": "y"})
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    fig = px.line(forecast, x="ds", y="yhat", title="30-Day Revenue Forecast")
    st.plotly_chart(fig, use_container_width=True)

