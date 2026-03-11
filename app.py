import streamlit as st
import pandas as pd

from modules.data_simulator import simulate_data
from modules.rfm_engine import compute_rfm
from modules.segmentation import segment_customers
from modules.clustering import perform_kmeans
from modules.cohort_analysis import compute_cohort
from modules.churn_model import predict_churn
from modules.clv import calculate_clv
from modules.marketing_engine import next_best_offer
from modules.campaign_simulator import campaign_roi
from modules.report_generator import generate_report
from modules.visualization import *

st.set_page_config(layout="wide")

st.title("📊 RFM Analytics Lab v6 Pro")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Generate Data",
        "Upload Data",
        "Data Explorer",
        "RFM Analysis",
        "Segmentation",
        "ML Clustering",
        "Cohort Retention",
        "Churn Prediction",
        "Customer Lifetime Value",
        "Next Best Offer Engine",
        "Campaign Simulator",
        "Executive Dashboard",
        "Automated Report"
    ]
)


if page == "Generate Data":

    customers = st.slider("Customers",100,2000,500)
    transactions = st.slider("Transactions",1000,20000,5000)

    if st.button("Generate Dataset"):

        df = simulate_data(customers,transactions)

        st.session_state["data"] = df

        st.dataframe(df.head())


# -------------------------------------------------
# Upload Data
# -------------------------------------------------

elif page == "Upload Data":

    file = st.file_uploader("Upload CSV")

    if file:

        df = pd.read_csv(file)

        st.session_state["data"] = df


# -------------------------------------------------
# Data Explorer
# -------------------------------------------------

elif page == "Data Explorer":

    df = st.session_state.get("data")

    if df is not None:

        st.dataframe(df.head())

        fig = sales_distribution(df)

        st.plotly_chart(fig)


# -------------------------------------------------
# RFM Analysis
# -------------------------------------------------

elif page == "RFM Analysis":

    df = st.session_state.get("data")

    if df is not None:

        rfm = compute_rfm(df)

        st.session_state["rfm"] = rfm

        st.dataframe(rfm.head())

        fig = rfm_scatter(rfm)

        st.plotly_chart(fig)


# -------------------------------------------------
# Segmentation
# -------------------------------------------------

elif page == "Segmentation":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = segment_customers(rfm)

        st.session_state["rfm"] = rfm

        fig = segment_pie_chart(rfm)

        st.plotly_chart(fig)


# -------------------------------------------------
# ML Clustering
# -------------------------------------------------

elif page == "ML Clustering":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        k = st.slider("Clusters",2,8,4)

        rfm = perform_kmeans(rfm,k)

        fig = cluster_scatter(rfm)

        st.plotly_chart(fig)


# -------------------------------------------------
# Cohort Retention
# -------------------------------------------------

elif page == "Cohort Retention":

    df = st.session_state.get("data")

    if df is not None:

        cohort = compute_cohort(df)

        fig = cohort_heatmap(cohort)

        st.pyplot(fig)


# -------------------------------------------------
# Churn Prediction
# -------------------------------------------------

elif page == "Churn Prediction":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = predict_churn(rfm)

        st.dataframe(
            rfm.sort_values("ChurnProbability",ascending=False).head(20)
        )


# -------------------------------------------------
# CLV
# -------------------------------------------------

elif page == "Customer Lifetime Value":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        rfm = calculate_clv(rfm)

        fig = clv_distribution(rfm)

        st.plotly_chart(fig)


# -------------------------------------------------
# Next Best Offer
# -------------------------------------------------

elif page == "Next Best Offer Engine":

    segment = st.selectbox(
        "Segment",
        ["Champions","Loyal","Potential","At Risk","Lost"]
    )

    st.success(next_best_offer(segment))


# -------------------------------------------------
# Campaign Simulator
# -------------------------------------------------

elif page == "Campaign Simulator":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        seg = st.selectbox("Segment",rfm.Segment.unique())

        discount = st.slider("Discount %",5,50,10)

        response = st.slider("Response Rate %",1,60,15)

        revenue = campaign_roi(rfm,seg,discount,response)

        st.metric("Projected Revenue",round(revenue,2))


# -------------------------------------------------
# Executive Dashboard
# -------------------------------------------------

elif page == "Executive Dashboard":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        st.metric("Customers",len(rfm))

        st.metric("Average Value",round(rfm.Monetary.mean(),2))

        st.metric("Revenue",round(rfm.Monetary.sum(),2))


# -------------------------------------------------
# Report
# -------------------------------------------------

elif page == "Automated Report":

    rfm = st.session_state.get("rfm")

    if rfm is not None:

        report = generate_report(rfm)

        st.download_button(
            "Download CRM Report",
            report,
            "crm_report.txt"
        )
# -------------------------------------------------
# Dashboard
# -------------------------------------------------
elif page == "Dashboard":

    rfm = st.session_state.get("rfm")

    if rfm is None:
        st.info("Run RFM Analysis first.")
        st.stop()

    st.header("CRM Analytics Dashboard")

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Customers",len(rfm))
    col2.metric("Revenue",round(rfm.Monetary.sum(),2))
    col3.metric("Avg Customer Value",round(rfm.Monetary.mean(),2))
    col4.metric("Avg Frequency",round(rfm.Frequency.mean(),2))

    seg = rfm["Segment"].value_counts().reset_index()
    seg.columns = ["Segment","Customers"]

    fig = px.pie(seg,values="Customers",names="Segment")
    st.plotly_chart(fig,use_container_width=True)

    fig = px.scatter(
        rfm,
        x="Recency",
        y="Frequency",
        size="Monetary",
        color="Segment"
    )

    st.plotly_chart(fig,use_container_width=True)
# -------------------------------------------------
# Data generation
# -------------------------------------------------
