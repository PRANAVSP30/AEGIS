def generate_investigation_report(credit_risk, behaviour_risk, fraud_risk, network_risk, decision):

    report = []

    # Behaviour analysis
    if behaviour_risk < 30:
        report.append("The applicant demonstrates stable financial behaviour.")
    elif behaviour_risk < 60:
        report.append("The applicant shows moderate financial instability in spending patterns.")
    else:
        report.append("The applicant shows abnormal financial behaviour with expenses exceeding safe limits.")

    # Credit risk analysis
    if credit_risk < 30:
        report.append("Credit risk is low based on income and loan ratio.")
    elif credit_risk < 60:
        report.append("Credit risk is moderate due to higher loan-to-income ratio.")
    else:
        report.append("Credit risk is high because the requested loan significantly exceeds income capacity.")

    # Fraud network analysis
    if network_risk > 50:
        report.append("The applicant has interacted with accounts flagged in fraud monitoring systems.")
    else:
        report.append("No interaction with known fraudulent accounts was detected.")

    # Final decision explanation
    if decision == "APPROVE":
        report.append("Overall risk remains low and the loan can be safely approved.")
    elif decision == "MANUAL REVIEW":
        report.append("The case requires manual investigation by a credit officer.")
    else:
        report.append("The risk indicators suggest a high probability of default or fraud. Loan rejection is recommended.")

    return " ".join(report)