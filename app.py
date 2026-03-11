import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from modules.data_simulator import simulate_data
from modules.rfm_engine import compute_rfm
from modules.segmentation import segment_customers
from modules.churn_model import predict_churn
from modules.clv import calculate_clv

# ------------------------------------------------
# Page config
# ------------------------------------------------

st.set_page_config(
    page_title="RFM Analytics Lab v6",
    layout="wide"
)

st.title("📊 RFM Analytics Lab v6")
st.caption("Customer Intelligence & CRM Analytics Platform")

# ------------------------------------------------
# Sidebar navigation
# ------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Generator",
        "Upload Data",
        "Data Explorer",
        "RFM Analysis",
        "Segmentation",
        "ML Clustering",
        "Cohort Retention",
        "Churn Prediction",
        "Customer Lifetime Value",
        "Next Best Offer Engine",
        "Customer Network Graph",
        "Campaign Simulator",
        "Executive Dashboard",
        "Automated Report"
    ]
)

# ------------------------------------------------
# Helper functions
# ------------------------------------------------

def get_data():

    if "data" in st.session_state:
        return st.session_state["data"]

    st.warning("Please generate or upload data first.")
    st.stop()


def get_rfm():

    if "rfm" in st.session_state:
        return st.session_state["rfm"]

    st.warning("Please run RFM Analysis first.")
    st.stop()

# ------------------------------------------------
# Dashboard
# ------------------------------------------------

if page == "Dashboard":

    st.header("CRM Analytics Overview")

    if "data" not in st.session_state:

        st.info("Generate or upload a dataset to begin.")

    else:

        df = st.session_state["data"]

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Transactions",len(df))
        col2.metric("Customers",df.CustomerID.nunique())
        col3.metric("Revenue",round(df.Sales.sum(),2))
        col4.metric("Average Order Value",round(df.Sales.mean(),2))

        st.subheader("Sales Distribution")

        fig = px.histogram(df,x="Sales")

        st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Data Generator
# ------------------------------------------------

elif page == "Data Generator":

    st.header("Synthetic Retail Data Generator")

    customers = st.slider("Customers",100,2000,500)
    transactions = st.slider("Transactions",1000,20000,5000)

    if st.button("Generate Dataset"):

        df = simulate_data(customers,transactions)

        st.session_state["data"] = df

        st.success("Dataset generated successfully")

        st.dataframe(df.head())

# ------------------------------------------------
# Upload Data
# ------------------------------------------------

elif page == "Upload Data":

    st.header("Upload Retail Dataset")

    file = st.file_uploader("Upload CSV")

    if file:

        df = pd.read_csv(file)

        st.session_state["data"] = df

        st.success("Dataset loaded")

        st.dataframe(df.head())

# ------------------------------------------------
# Data Explorer
# ------------------------------------------------

elif page == "Data Explorer":

    df = get_data()

    st.header("Dataset Explorer")

    st.dataframe(df.head())

    st.subheader("Sales Distribution")

    fig = px.histogram(df,x="Sales")

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# RFM Analysis
# ------------------------------------------------

elif page == "RFM Analysis":

    df = get_data()

    st.header("RFM Analysis")

    rfm = compute_rfm(df)

    st.session_state["rfm"] = rfm

    st.dataframe(rfm.head())

    fig = px.scatter(
        rfm,
        x="Recency",
        y="Frequency",
        size="Monetary"
    )

    st.plotly_chart(fig)

# ------------------------------------------------
# Segmentation
# ------------------------------------------------

elif page == "Segmentation":

    rfm = get_rfm()

    rfm = segment_customers(rfm)

    st.session_state["rfm"] = rfm

    st.header("Customer Segmentation")

    seg = rfm.Segment.value_counts().reset_index()

    seg.columns=["Segment","Customers"]

    fig = px.pie(seg,values="Customers",names="Segment")

    st.plotly_chart(fig)

# ------------------------------------------------
# ML Clustering
# ------------------------------------------------

elif page == "ML Clustering":

    rfm = get_rfm()

    st.header("Machine Learning Clustering")

    X = rfm[["Recency","Frequency","Monetary"]]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    k = st.slider("Clusters",2,8,4)

    model = KMeans(n_clusters=k)

    rfm["Cluster"] = model.fit_predict(X_scaled)

    fig = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        color=rfm.Cluster.astype(str),
        size="Monetary"
    )

    st.plotly_chart(fig)

# ------------------------------------------------
# Cohort Retention
# ------------------------------------------------

elif page == "Cohort Retention":

    df = get_data()

    st.header("Customer Cohort Retention")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["OrderMonth"] = df.InvoiceDate.dt.to_period("M")

    cohort = df.groupby("CustomerID")["OrderMonth"].min()

    df["Cohort"] = df.CustomerID.map(cohort)

    cohort_data = df.groupby(["Cohort","OrderMonth"])["CustomerID"].nunique()

    pivot = cohort_data.reset_index().pivot(index="Cohort",columns="OrderMonth",values="CustomerID")

    fig,ax = plt.subplots()

    sns.heatmap(pivot,cmap="Blues")

    st.pyplot(fig)

# ------------------------------------------------
# Churn Prediction
# ------------------------------------------------

elif page == "Churn Prediction":

    rfm = get_rfm()

    st.header("Churn Prediction")

    rfm = predict_churn(rfm)

    st.dataframe(
        rfm.sort_values("ChurnProbability",ascending=False).head(20)
    )

# ------------------------------------------------
# CLV
# ------------------------------------------------

elif page == "Customer Lifetime Value":

    rfm = get_rfm()

    st.header("Customer Lifetime Value")

    rfm = calculate_clv(rfm)

    fig = px.histogram(rfm,x="CLV")

    st.plotly_chart(fig)

# ------------------------------------------------
# Next Best Offer
# ------------------------------------------------

elif page == "Next Best Offer Engine":

    st.header("Next Best Offer")

    segment = st.selectbox(
        "Customer Segment",
        ["Champions","Loyal","Potential","At Risk","Lost"]
    )

    offers = {

        "Champions":"Premium loyalty rewards",
        "Loyal":"Cross-sell complementary products",
        "Potential":"Welcome discount",
        "At Risk":"Win-back campaign",
        "Lost":"Reactivation offer"

    }

    st.success(offers.get(segment))

# ------------------------------------------------
# Customer Network Graph
# ------------------------------------------------

elif page == "Customer Network Graph":

    st.header("Customer Influence Network")

    G = nx.erdos_renyi_graph(40,0.05)

    pos = nx.spring_layout(G)

    fig,ax = plt.subplots()

    nx.draw(G,pos,node_size=100)

    st.pyplot(fig)

# ------------------------------------------------
# Campaign Simulator
# ------------------------------------------------

elif page == "Campaign Simulator":

    rfm = get_rfm()

    st.header("Campaign ROI Simulator")

    seg = st.selectbox("Target Segment",rfm.Segment.unique())

    discount = st.slider("Discount %",5,50,10)

    response = st.slider("Response Rate %",1,60,15)

    avg = rfm.Monetary.mean()

    customers = rfm[rfm.Segment==seg].shape[0]

    buyers = customers*(response/100)

    revenue = buyers*avg*(1-discount/100)

    st.metric("Projected Revenue",round(revenue,2))

# ------------------------------------------------
# Executive Dashboard
# ------------------------------------------------

elif page == "Executive Dashboard":

    rfm = get_rfm()

    st.header("Executive CRM Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Customers",len(rfm))
    col2.metric("Avg Value",round(rfm.Monetary.mean(),2))
    col3.metric("Total Revenue",round(rfm.Monetary.sum(),2))

# ------------------------------------------------
# Automated Report
# ------------------------------------------------

elif page == "Automated Report":

    rfm = get_rfm()

    report = f"""

CRM ANALYTICS REPORT

Customers: {len(rfm)}

Average Customer Value: {rfm.Monetary.mean():.2f}

Total Revenue: {rfm.Monetary.sum():.2f}

"""

    st.download_button(
        "Download Report",
        report,
        "crm_report.txt"
    )
