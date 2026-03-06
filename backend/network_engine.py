import pandas as pd

# Load fraud accounts
fraud_accounts = pd.read_csv("data/fraud_accounts.csv")

fraud_list = fraud_accounts["account_id"].tolist()


def check_network_risk(receiver_account):

    # If applicant interacts with flagged account
    if receiver_account in fraud_list:
        return 80

    return 10