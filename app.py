import streamlit as st
import pandas as pd

from modules.data_simulator import simulate_data
from modules.rfm_engine import compute_rfm
from modules.segmentation import segment_customers
from modules.churn_model import predict_churn
from modules.clv import calculate_clv

st.set_page_config(layout="wide")

st.title("RFM Analytics Lab v6")

page = st.sidebar.radio(
    "Navigation",
    [
        "Generate Data",
        "Upload Data",
        "RFM Analysis",
        "Segmentation",
        "Churn Prediction",
        "Customer Lifetime Value"
    ]
)

# -----------------------------
# Data generation
# -----------------------------

if page == "Generate Data":

    customers = st.slider("Customers",100,2000,500)
    transactions = st.slider("Transactions",1000,20000,5000)

    if st.button("Generate Dataset"):

        df = simulate_data(customers,transactions)

        st.session_state["data"] = df

        st.dataframe(df.head())

# -----------------------------
# Upload data
# -----------------------------

if page == "Upload Data":

    file = st.file_uploader("Upload CSV")

    if file:

        df = pd.read_csv(file)

        st.session_state["data"] = df

        st.dataframe(df.head())

# -----------------------------
# RFM analysis
# -----------------------------

if page == "RFM Analysis":

    df = st.session_state.get("data")

    if df is not None:

        rfm = compute_rfm(df)

        st.session_state["rfm"] = rfm

        st.dataframe(rfm.head())

# -----------------------------
# Segmentation
# -----------------------------

if page == "Segmentation":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = segment_customers(rfm)

        st.dataframe(rfm.head())

# -----------------------------
# Churn prediction
# -----------------------------

if page == "Churn Prediction":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = predict_churn(rfm)

        st.dataframe(
            rfm.sort_values("ChurnProbability",ascending=False).head(20)
        )

# -----------------------------
# CLV
# -----------------------------

if page == "Customer Lifetime Value":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = calculate_clv(rfm)

        st.dataframe(
            rfm.sort_values("CLV",ascending=False).head(20)
        )
