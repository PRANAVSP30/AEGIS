def detect_anomaly(income, expenses):

    # spending ratio
    spending_ratio = expenses / (income + 1)

    # normal behaviour
    if spending_ratio < 0.7:
        return 20

    # moderate risk
    elif spending_ratio < 1:
        return 50

    # suspicious behaviour
    else:
        return 80