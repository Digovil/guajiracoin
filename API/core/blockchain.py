import hashlib
import json
from time import time
from core.file_handling import *

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.miners = []  
        load_chain_from_disk(self.chain, self.current_transactions)

        if not self.chain:
            self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else "1",
        }

        self.current_transactions = []
        self.chain.append(block)
        save_chain_to_disk(self.chain, self.current_transactions)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block.index + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        return hashlib.sha1(json.dumps(block, sort_keys=True).encode()).hexdigest()


    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not self.valid_proof(block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
    
    @staticmethod
    def valid_proof(proof):
        if proof == 100: return True
        
        return proof[:4] == "0000"