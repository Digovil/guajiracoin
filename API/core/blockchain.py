import hashlib
import json
from time import time
from core.file_handling import *

class Blockchain:
    def __init__(self):
        self.chain = []
        self.miners = []  
        self.targetPrefix = "0000"
        
        if not get_chain():
            self.new_block(previous_hash="1", current_transactions=None, proof=100)

    def new_block(self, proof, current_transactions, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else "1",
        }

        self.chain.append(block)
        save_chain_to_disk(self.chain)
        return block

    # def new_transaction(self, sender, recipient, amount):
    #     self.current_transactions.append({
    #         'sender': sender,
    #         'recipient': recipient,
    #         'amount': amount,
    #     })
    #     save_chain_to_disk(self.chain, self.current_transactions)
    #     return self.last_block["index"] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        return hashlib.sha1(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def get_blockchain(self):
        self.chain  = get_chain()
        return self.chain 
    
    def calcular_saldo(self, direccion):
        saldo = 0

        for bloque in self.chain:
            transacciones = bloque.get("transactions")

            # Verificar si hay transacciones en el bloque
            if transacciones is not None:
                for transaccion in transacciones:
                    remitente = transaccion.get("sender", "")
                    destinatario = transaccion.get("recipient", "")
                    cantidad = transaccion.get("amount", 0)

                    # Si la dirección es el destinatario, agrega la cantidad al saldo
                    if destinatario == direccion:
                        saldo += cantidad

                    # Si la dirección es el remitente, resta la cantidad del saldo
                    if remitente == direccion:
                        saldo -= cantidad

        return saldo

# Resto del código sigue igual...


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
    
    def valid_proof(self, proof):
        if proof == 100: return True
        
        return proof[:4] == self.targetPrefix