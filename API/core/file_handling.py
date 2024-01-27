import json
import os

def load_chain_from_disk(chain, current_transactions):
    if os.path.exists('blockchain.json'):
        with open('blockchain.json', 'r') as f:
            data = json.load(f)
            chain = data['chain']
            current_transactions = data['current_transactions']
    else:
        # Create the blockchain.json file if it doesn't exist
        save_chain_to_disk(chain, current_transactions)

def save_chain_to_disk(chain, current_transactions):
    data = {
        'chain': chain,
        'current_transactions': current_transactions,
    }
    with open('blockchain.json', 'w') as f:
        json.dump(data, f, indent=4)
