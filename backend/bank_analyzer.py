import pandas as pd
import pdfplumber


def analyze_csv(file):

    df = pd.read_csv(file)

    total_credit = float(df["Credit"].sum())
    total_debit = float(df["Debit"].sum())

    income = float(total_credit)
    expenses = float(total_debit)

    transactions = int(len(df))

    # detect suspicious withdrawals
    large_withdrawals = df[df["Debit"] > 50000]

    suspicious = bool(len(large_withdrawals) > 0)

    # detect receiver accounts
    if "Account_ID" in df.columns:
        receiver_accounts = df["Account_ID"].dropna().astype(str).unique().tolist()
    else:
        receiver_accounts = []

    return {
        "income": income,
        "expenses": expenses,
        "transactions": transactions,
        "suspicious": suspicious,
        "receivers": receiver_accounts
    }


def analyze_pdf(file):

    income = 0.0
    expenses = 0.0
    transactions = 0

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:
            tables = page.extract_tables()

            for table in tables:
                for row in table:

                    try:
                        debit = float(row[2])
                        credit = float(row[3])

                        expenses += debit
                        income += credit
                        transactions += 1

                    except:
                        continue

    return {
        "income": float(income),
        "expenses": float(expenses),
        "transactions": int(transactions),
        "suspicious": False,
        "receivers": []
    }