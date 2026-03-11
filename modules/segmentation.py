def segment_customers(rfm):

    def segment(row):

        if row["Recency"] <= 30 and row["Frequency"] >= 5:
            return "Champions"

        if row["Frequency"] >= 5:
            return "Loyal"

        if row["Recency"] <= 60:
            return "Potential"

        if row["Recency"] > 120:
            return "Lost"

        return "Others"

    rfm["Segment"] = rfm.apply(segment,axis=1)

    return rfm
