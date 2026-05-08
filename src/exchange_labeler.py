def label_exchange(address, degree=0):

    # Heuristic 1: high activity wallets = likely exchange
    if degree > 100:
        return "Exchange (High Activity)"

    # Heuristic 2: fallback
    return "Unknown"