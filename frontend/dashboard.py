import streamlit as st
import requests

st.title("AGEX – AI Risk Intelligence Platform")
st.caption("AI-powered fraud detection and credit risk analysis for secure lending")

name = st.text_input("Customer Name")
income = st.number_input("Monthly Income")
expenses = st.number_input("Monthly Expenses")
loan = st.number_input("Loan Amount Requested")
receiver_account = st.text_input("Recent Transfer Account ID")

if st.button("Analyze Loan"):

    response = requests.post(
        "http://127.0.0.1:8000/analyze-loan",
        json={
            "name": name,
            "income": income,
            "expenses": expenses,
            "loan_amount": loan,
            "receiver_account": receiver_account
        }
    )

    data = response.json()

    st.subheader("Risk Intelligence Report")

    analysis = data["analysis"]

    st.write("Credit Risk:", analysis["credit_risk"])
    st.write("Behaviour Risk:", analysis["behaviour_risk"])
    st.write("Fraud Risk:", analysis["fraud_risk"])
    st.write("Network Risk:", analysis["network_risk"])
    st.write("Final Risk Score:", analysis["final_score"])

    decision = analysis["decision"]

    if decision == "APPROVE":
        st.success("Decision: APPROVE LOAN")
    elif decision == "MANUAL REVIEW":
        st.warning("Decision: MANUAL REVIEW REQUIRED")
    else:
        st.error("Decision: REJECT LOAN")

    st.subheader("AI Investigation Report")

    st.info(analysis["ai_report"])