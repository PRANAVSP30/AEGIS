import streamlit as st
import requests

st.set_page_config(page_title="AGEX Risk Intelligence Platform", layout="wide")

# -------------------------
# PROFESSIONAL CLEAN STYLE
# -------------------------

st.markdown("""
<style>

.stApp {
background-color: white;
color: black;
}

h1,h2,h3 {
color:#1f4fff;
}

button {
background-color:#1f4fff;
color:white;
border-radius:6px;
padding:10px 20px;
border:none;
}

button:hover {
background-color:#163ccc;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# PAGE STATE
# -------------------------

if "page" not in st.session_state:
    st.session_state.page = 1

# -------------------------
# PAGE 1 — CUSTOMER INFO
# -------------------------

if st.session_state.page == 1:

    st.title("AGEX – AI Risk Intelligence Platform")

    st.header("Step 1 — Customer Information")

    customer_name = st.text_input("Customer Name")
    pan = st.text_input("PAN Number")
    account = st.text_input("Bank Account Number")
    phone = st.text_input("Phone Number")
    dob = st.text_input("Date of Birth")

    loan_amount = st.number_input("Loan Amount Requested", min_value=0.0)

    if st.button("Next ➜"):

        st.session_state.customer_name = customer_name
        st.session_state.pan = pan
        st.session_state.account = account
        st.session_state.loan_amount = loan_amount

        st.session_state.page = 2
        st.rerun()

# -------------------------
# PAGE 2 — STATEMENT UPLOAD
# -------------------------

elif st.session_state.page == 2:

    st.title("AGEX – Financial Data Upload")

    st.header("Step 2 — Upload Bank Statements")

    statements = st.file_uploader(
        "Upload Bank Statements (CSV / PDF)",
        type=["csv","pdf"],
        accept_multiple_files=True
    )

    col1,col2 = st.columns(2)

    with col1:
        if st.button("⬅ Back"):
            st.session_state.page = 1
            st.rerun()

    with col2:
        if st.button("Run AI Analysis ➜"):

            if not statements:
                st.error("Please upload bank statements")

            else:

                files=[]

                for s in statements:
                    files.append(("files",(s.name,s.getvalue())))

                response=requests.post(
                    "http://127.0.0.1:8000/analyze-statement",
                    files=files,
                    params={
                        "loan_amount":st.session_state.loan_amount,
                        "customer_name":st.session_state.customer_name,
                        "pan":st.session_state.pan,
                        "account":st.session_state.account
                    }
                )

                data=response.json()

                st.session_state.result=data
                st.session_state.page=3
                st.rerun()

# -------------------------
# PAGE 3 — REPORT
# -------------------------

elif st.session_state.page == 3:

    data=st.session_state.result

    if "error" in data:
        st.error(data["error"])

    else:

        financial=data["financial_analysis"]
        risk=data["risk_analysis"]

        st.title("AGEX Risk Intelligence Report")

        st.header("Financial Behaviour Analysis")

        col1,col2,col3=st.columns(3)

        col1.metric("Income",financial["income"])
        col2.metric("Expenses",financial["expenses"])
        col3.metric("Transactions",financial["transactions"])

        st.header("Risk Intelligence")

        r1,r2,r3,r4=st.columns(4)

        r1.metric("Credit Risk",risk["credit_risk"])
        r2.metric("Behaviour Risk",risk["behaviour_risk"])
        r3.metric("Fraud Risk",risk["fraud_risk"])
        r4.metric("Network Risk",risk["network_risk"])

        st.metric("Final Risk Score",risk["final_score"])

        decision=risk["decision"]

        if decision=="APPROVE":
            st.success("Loan Approved")

        elif decision=="MANUAL REVIEW":
            st.warning("Manual Investigation Required")

        else:
            st.error("Loan Rejected")

        st.subheader("AI Investigation Summary")

        st.info(risk["ai_report"])

        if "report_file" in data:

            with open(data["report_file"],"rb") as f:

                st.download_button(
                    "Download Risk Report (PDF)",
                    data=f,
                    file_name=data["report_file"],
                    mime="application/pdf"
                )

        if st.button("Start New Analysis"):
            st.session_state.page=1
            st.rerun()