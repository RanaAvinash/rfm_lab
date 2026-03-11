from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def perform_kmeans(rfm, k=4):

    X = rfm[["Recency","Frequency","Monetary"]]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    model = KMeans(n_clusters=k, random_state=42)

    rfm["Cluster"] = model.fit_predict(X_scaled)

    return rfm
