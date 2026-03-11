import pandas as pd
import numpy as np

def simulate_data(customers,transactions):

    np.random.seed(42)

    df = pd.DataFrame({

        "CustomerID":np.random.randint(10000,10000+customers,transactions),

        "InvoiceNo":np.random.randint(100000,400000,transactions),

        "InvoiceDate":pd.date_range("2024-01-01",periods=transactions),

        "Quantity":np.random.randint(1,5,transactions),

        "UnitPrice":np.random.uniform(5,50,transactions)

    })

    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    return df
