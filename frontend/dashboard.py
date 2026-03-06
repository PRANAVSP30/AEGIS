import streamlit as st
import requests

st.title("AGEX – AI Risk Intelligence Platform")
st.caption("AI-powered fraud detection and credit risk analysis")

st.header("Step 1 — Customer Information")

customer_name = st.text_input("Customer Name")
pan = st.text_input("PAN Number")
account = st.text_input("Bank Account Number")

loan_amount = st.number_input("Loan Amount Requested")

st.header("Step 2 — Upload Bank Statement")

statement = st.file_uploader(
    "Upload Bank Statement (CSV or PDF)",
    type=["csv", "pdf"]
)

if st.button("Run AI Analysis"):

    if statement is None:
        st.error("Please upload a bank statement first.")
    else:

        files = {
            "file": (statement.name, statement.getvalue())
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze-statement",
                files=files,
                params={"loan_amount": loan_amount}
            )

            if response.status_code != 200:
                st.error("Backend error occurred.")
                st.text(response.text)
            else:

                data = response.json()

                st.header("Financial Behaviour Analysis")

                financial = data["financial_analysis"]

                st.write("Income Detected:", financial["income"])
                st.write("Expenses Detected:", financial["expenses"])
                st.write("Total Transactions:", financial["transactions"])

                st.header("Risk Intelligence Report")

                risk = data["risk_analysis"]

                st.write("Credit Risk:", risk["credit_risk"])
                st.write("Behaviour Risk:", risk["behaviour_risk"])
                st.write("Fraud Risk:", risk["fraud_risk"])
                st.write("Network Risk:", risk["network_risk"])
                st.write("Final Risk Score:", risk["final_score"])

                decision = risk["decision"]

                if decision == "APPROVE":
                    st.success("Loan Approved")
                elif decision == "MANUAL REVIEW":
                    st.warning("Manual Investigation Required")
                else:
                    st.error("Loan Rejected")

                st.subheader("AI Investigation Summary")

                st.info(risk["ai_report"])

        except Exception as e:
            st.error("Request failed")
            st.text(e)