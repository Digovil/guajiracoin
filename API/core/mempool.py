from core.file_handling import *

class Mempool:
    def __init__(self):
        self.current_transactions = []
        
    def new_transaction(self, sender, recipient, amount, last_block):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        save_mempool_to_disk(self.current_transactions)
        return last_block["index"] + 1
    
    def get_transactions(self):
        self.current_transactions = get_mempool()
        return self.current_transactions