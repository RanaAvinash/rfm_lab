import pandas as pd

def compute_cohort(df):

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["OrderMonth"] = df.InvoiceDate.dt.to_period("M")

    cohort = df.groupby("CustomerID")["OrderMonth"].min()

    df["Cohort"] = df.CustomerID.map(cohort)

    cohort_data = df.groupby(["Cohort","OrderMonth"])["CustomerID"].nunique()

    pivot = cohort_data.reset_index().pivot(
        index="Cohort",
        columns="OrderMonth",
        values="CustomerID"
    )

    return pivot
