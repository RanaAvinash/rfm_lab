def calculate_clv(rfm,lifespan=3):

    rfm["CLV"] = rfm["Monetary"] * rfm["Frequency"] * lifespan / 10

    return rfm
