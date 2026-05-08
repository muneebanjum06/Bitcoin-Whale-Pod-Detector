import requests

def fetch_btc_transactions(limit_blocks=3):

    txs_all = []

    try:
        blocks_url = "https://blockstream.info/api/blocks"
        blocks = requests.get(blocks_url).json()

        count = 0

        for block in blocks:

            if count >= limit_blocks:
                break

            block_hash = block["id"]

            url = f"https://blockstream.info/api/block/{block_hash}/txs"
            txs = requests.get(url).json()

            txs_all.extend(txs)
            count += 1

        return txs_all

    except Exception as e:
        return {"error": str(e)}