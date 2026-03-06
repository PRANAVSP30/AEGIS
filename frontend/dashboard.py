import streamlit as st
import requests

st.set_page_config(page_title="AGEX Risk Intelligence Platform", layout="wide")

st.title("AGEX – AI Risk Intelligence Platform")
st.caption("AI-powered fraud detection and credit risk analysis for secure lending")

# -------------------------
# STEP 1 — CUSTOMER DETAILS
# -------------------------

st.header("Step 1 — Customer Information")

customer_name = st.text_input("Customer Name")
pan = st.text_input("PAN Number")
account = st.text_input("Bank Account Number")
phone = st.text_input("Phone Number")
dob = st.text_input("Date of Birth")

loan_amount = st.number_input("Loan Amount Requested", min_value=0.0)

# -------------------------
# STEP 2 — UPLOAD STATEMENT
# -------------------------

st.header("Step 2 — Upload Bank Statement")

statement = st.file_uploader(
    "Upload Bank Statement (CSV or PDF)",
    type=["csv", "pdf"]
)

# -------------------------
# RUN ANALYSIS
# -------------------------

if st.button("Run AI Analysis"):

    if statement is None:
        st.error("Please upload a bank statement first.")
    elif customer_name == "" or pan == "" or account == "":
        st.error("Please fill all customer information.")
    else:

        try:

            files = {
                "file": (statement.name, statement.getvalue())
            }

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

            if response.status_code != 200:
                st.error("Backend error occurred")
                st.text(response.text)

            else:

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:

                    financial = data["financial_analysis"]
                    risk = data["risk_analysis"]

                    # -------------------------
                    # FINANCIAL ANALYSIS
                    # -------------------------

                    st.header("Financial Behaviour Analysis")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Income Detected", financial["income"])

                    with col2:
                        st.metric("Expenses Detected", financial["expenses"])

                    with col3:
                        st.metric("Transactions", financial["transactions"])

                    # -------------------------
                    # RISK REPORT
                    # -------------------------

                    st.header("Risk Intelligence Report")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Credit Risk", risk["credit_risk"])

                    with col2:
                        st.metric("Behaviour Risk", risk["behaviour_risk"])

                    with col3:
                        st.metric("Fraud Risk", risk["fraud_risk"])

                    with col4:
                        st.metric("Network Risk", risk["network_risk"])

                    st.subheader("Final Risk Score")

                    st.metric("Final Risk Score", risk["final_score"])

                    # -------------------------
                    # DECISION
                    # -------------------------

                    decision = risk["decision"]

                    if decision == "APPROVE":
                        st.success("Loan Approved")

                    elif decision == "MANUAL REVIEW":
                        st.warning("Manual Investigation Required")

                    else:
                        st.error("Loan Rejected")

                    # -------------------------
                    # AI SUMMARY
                    # -------------------------

                    st.subheader("AI Investigation Summary")

                    st.info(risk["ai_report"])

                    # -------------------------
                    # DOWNLOAD REPORT
                    # -------------------------

                    if "report_file" in data:

                        with open(data["report_file"], "rb") as file:

                            st.download_button(
                                label="Download Risk Report (PDF)",
                                data=file,
                                file_name=data["report_file"],
                                mime="application/pdf"
                            )

        except Exception as e:
            st.error("Request Failed")
            st.text(e)