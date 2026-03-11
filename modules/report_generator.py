def generate_report(rfm):

    report = f"""

CRM ANALYTICS REPORT

Customers: {len(rfm)}

Average Customer Value: {rfm.Monetary.mean():.2f}

Total Revenue: {rfm.Monetary.sum():.2f}

"""

    return report
