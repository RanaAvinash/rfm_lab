def campaign_roi(rfm, segment, discount, response):

    avg = rfm.Monetary.mean()

    customers = rfm[rfm.Segment == segment].shape[0]

    buyers = customers * (response/100)

    revenue = buyers * avg * (1 - discount/100)

    return revenue
