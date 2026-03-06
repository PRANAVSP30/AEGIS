from backend.anomaly_model import detect_anomaly
from backend.fraud_database import is_account_flagged, add_flagged_account


def calculate_risk(income, expenses, loan_amount, receiver_account):

    spending_ratio = expenses / (income + 1)

    # ---------------------
    # CREDIT RISK
    # ---------------------

    loan_income_ratio = loan_amount / (income + 1)

    if loan_income_ratio < 2:
        credit_risk = 20
    elif loan_income_ratio < 4:
        credit_risk = 50
    else:
        credit_risk = 80

    # ---------------------
    # BEHAVIOUR RISK
    # ---------------------

    behaviour_risk = detect_anomaly(income, expenses)

    # ---------------------
    # FRAUD RISK
    # ---------------------

    fraud_risk = 10

    if receiver_account.startswith("AC999"):
        fraud_risk = 80
        add_flagged_account(receiver_account)

    # ---------------------
    # NETWORK RISK
    # ---------------------

    network_risk = 10

    if receiver_account != "":
        if is_account_flagged(receiver_account):
            network_risk = 80

    # ---------------------
    # FINAL SCORE
    # ---------------------

    final_score = (
        credit_risk * 0.35
        + behaviour_risk * 0.25
        + fraud_risk * 0.20
        + network_risk * 0.20
    )

    # ---------------------
    # DECISION
    # ---------------------

    if final_score < 35:
        decision = "APPROVE"
    elif final_score < 60:
        decision = "MANUAL REVIEW"
    else:
        decision = "REJECT"

    # ---------------------
    # AI SUMMARY
    # ---------------------

    ai_report = generate_ai_summary(
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
        "ai_report": ai_report
    }


def generate_ai_summary(credit_risk, behaviour_risk, fraud_risk, network_risk, decision):

    summary = ""

    if behaviour_risk < 40:
        summary += "The applicant shows stable financial behaviour. "
    else:
        summary += "Financial behaviour indicates irregular spending patterns. "

    if fraud_risk > 50:
        summary += "Fraud pattern signals were detected in recent transactions. "
    else:
        summary += "No direct fraud transaction patterns were detected. "

    if network_risk > 50:
        summary += "The applicant interacted with accounts previously flagged in fraud investigations. "

    summary += f"Final system recommendation: {decision}."

    return summary