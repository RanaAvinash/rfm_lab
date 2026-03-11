import numpy as np
from sklearn.ensemble import RandomForestClassifier

def predict_churn(rfm):

    rfm["Churn"] = np.where(
        rfm["Recency"] > rfm["Recency"].median(),1,0
    )

    X = rfm[["Recency","Frequency","Monetary"]]
    y = rfm["Churn"]

    model = RandomForestClassifier()

    model.fit(X,y)

    rfm["ChurnProbability"] = model.predict_proba(X)[:,1]

    return rfm
