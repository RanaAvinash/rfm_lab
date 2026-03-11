from datetime import timedelta

def compute_rfm(df):

    snapshot = df["InvoiceDate"].max() + timedelta(days=1)

    rfm = df.groupby("CustomerID").agg({

        "InvoiceDate":lambda x:(snapshot-x.max()).days,

        "InvoiceNo":"count",

        "Sales":"sum"

    })

    rfm.columns = ["Recency","Frequency","Monetary"]

    return rfm.reset_index()
