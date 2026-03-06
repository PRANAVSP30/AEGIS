import streamlit as st
import requests

st.set_page_config(page_title="AGEX Risk Intelligence Platform", layout="wide")

st.title("AGEX – AI Risk Intelligence Platform")
st.caption("AI-powered fraud detection and credit risk analysis for secure lending")

st.header("Step 1 — Customer Information")

customer_name = st.text_input("Customer Name")
pan = st.text_input("PAN Number")
account = st.text_input("Bank Account Number")
phone = st.text_input("Phone Number")
dob = st.text_input("Date of Birth")

loan_amount = st.number_input("Loan Amount Requested", min_value=0.0)

st.header("Step 2 — Upload Bank Statements")

statements = st.file_uploader(
    "Upload Bank Statements (CSV or PDF)",
    type=["csv", "pdf"],
    accept_multiple_files=True
)

if st.button("Run AI Analysis"):

    if not statements:
        st.error("Please upload at least one bank statement.")
    else:

        files = []

        for statement in statements:
            files.append(
                ("files", (statement.name, statement.getvalue()))
            )

        response = requests.post(
            "http://127.0.0.1:8000/analyze-statement",
            files=files,
            params={
                "loan_amount": loan_amount,
                "customer_name": customer_name,
                "pan": pan,
                "account": account
            }
        )

        data = response.json()

        if "error" in data:
            st.error(data["error"])

        else:

            financial = data["financial_analysis"]
            risk = data["risk_analysis"]

            st.header("Financial Behaviour Analysis")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Income", financial["income"])
            col2.metric("Total Expenses", financial["expenses"])
            col3.metric("Transactions", financial["transactions"])

            st.header("Risk Intelligence Report")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Credit Risk", risk["credit_risk"])
            col2.metric("Behaviour Risk", risk["behaviour_risk"])
            col3.metric("Fraud Risk", risk["fraud_risk"])
            col4.metric("Network Risk", risk["network_risk"])

            st.metric("Final Risk Score", risk["final_score"])

            decision = risk["decision"]

            if decision == "APPROVE":
                st.success("Loan Approved")

            elif decision == "MANUAL REVIEW":
                st.warning("Manual Investigation Required")

            else:
                st.error("Loan Rejected")

            st.subheader("AI Investigation Summary")

            st.info(risk["ai_report"])

            if "report_file" in data:

                with open(data["report_file"], "rb") as f:

                    st.download_button(
                        label="Download Risk Report (PDF)",
                        data=f,
                        file_name=data["report_file"],
                        mime="application/pdf"
                    )