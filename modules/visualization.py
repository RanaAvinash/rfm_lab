import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx


# -------------------------------------------------
# Sales Distribution
# -------------------------------------------------

def sales_distribution(df):

    fig = px.histogram(
        df,
        x="Sales",
        title="Sales Distribution"
    )

    return fig


# -------------------------------------------------
# RFM Scatter Plot
# -------------------------------------------------

def rfm_scatter(rfm):

    fig = px.scatter(
        rfm,
        x="Recency",
        y="Frequency",
        size="Monetary",
        title="RFM Customer Distribution"
    )

    return fig


# -------------------------------------------------
# Segment Pie Chart
# -------------------------------------------------

def segment_pie_chart(rfm):

    seg = rfm["Segment"].value_counts().reset_index()

    seg.columns = ["Segment","Customers"]

    fig = px.pie(
        seg,
        values="Customers",
        names="Segment",
        title="Customer Segment Distribution"
    )

    return fig


# -------------------------------------------------
# ML Cluster Visualization
# -------------------------------------------------

def cluster_scatter(rfm):

    fig = px.scatter(
        rfm,
        x="Frequency",
        y="Monetary",
        color=rfm["Cluster"].astype(str),
        size="Monetary",
        title="Customer Clusters"
    )

    return fig


# -------------------------------------------------
# Cohort Heatmap
# -------------------------------------------------

def cohort_heatmap(cohort_pivot):

    fig, ax = plt.subplots()

    sns.heatmap(
        cohort_pivot,
        cmap="Blues",
        ax=ax
    )

    ax.set_title("Customer Cohort Retention")

    return fig


# -------------------------------------------------
# CLV Distribution
# -------------------------------------------------

def clv_distribution(rfm):

    fig = px.histogram(
        rfm,
        x="CLV",
        title="Customer Lifetime Value Distribution"
    )

    return fig


# -------------------------------------------------
# Customer Network Graph
# -------------------------------------------------

def customer_network():

    G = nx.erdos_renyi_graph(40,0.05)

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()

    nx.draw(
        G,
        pos,
        node_size=100,
        ax=ax
    )

    ax.set_title("Customer Influence Network")

    return fig
