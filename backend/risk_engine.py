from backend.anomaly_model import detect_anomaly
from backend.network_engine import check_network_risk
from backend.report_engine import generate_investigation_report


def calculate_risk(income, expenses, loan_amount, receiver_account):

    # Credit risk
    credit_ratio = loan_amount / (income + 1)

    if credit_ratio < 2:
        credit_risk = 20
    elif credit_ratio < 4:
        credit_risk = 50
    else:
        credit_risk = 80

    # Behaviour analysis
    behaviour_risk = detect_anomaly(income, expenses)

    # Fraud placeholder
    fraud_risk = 10

    # Network intelligence
    network_risk = check_network_risk(receiver_account)

    # Final score
    final_score = (
        0.4 * credit_risk +
        0.3 * behaviour_risk +
        0.1 * fraud_risk +
        0.2 * network_risk
    )

    if final_score < 35:
        decision = "APPROVE"
    elif final_score < 65:
        decision = "MANUAL REVIEW"
    else:
        decision = "REJECT"

    # Generate AI explanation
    investigation_report = generate_investigation_report(
        credit_risk,
        behaviour_risk,
        fraud_risk,
        network_risk,
        decision
    )

    return {
        "credit_risk": credit_risk,
        "behaviour_risk": behaviour_risk,
        "fraud_risk": fraud_risk,
        "network_risk": network_risk,
        "final_score": round(final_score, 2),
        "decision": decision,
        "ai_report": investigation_report
    }