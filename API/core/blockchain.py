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
            self.new_block(previous_hash="1", current_transactions=None, proof="0000e0350306b01614d5e0a0e2ee468621ba475f")

    def new_block(self, proof, current_transactions, previous_hash, nonce):
        block = {
            'index': len(self.chain) + 1,
            'nonce': nonce,
            'timestamp': time(),
            'transactions': current_transactions,
            'proof': proof,
            'previous_hash': previous_hash,
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


    def get_received_transactions(self, address):
        received_transactions = []

        for bloque in self.chain:
            transacciones = bloque.get("transactions")

            if transacciones is not None: 
                for transaccion in transacciones:
                    destinatario = transaccion.get("recipient", "")
                    cantidad = transaccion.get("amount", 0)
                    timestamp = bloque.get("timestamp", 0)

                    if destinatario == address:
                        received_transactions.append({
                            'sender': transaccion.get("sender", ""),
                            'recipient': destinatario,
                            'amount': cantidad,
                            'timestamp': timestamp
                        })

        return received_transactions

    def get_sent_transactions(self, address):
        sent_transactions = []

        for bloque in self.chain:
            transacciones = bloque.get("transactions")

            if transacciones is not None:
                for transaccion in transacciones:
                    remitente = transaccion.get("sender", "")
                    cantidad = transaccion.get("amount", 0)
                    timestamp = bloque.get("timestamp", 0)

                    if remitente == address:
                        sent_transactions.append({
                            'sender': remitente,
                            'recipient': transaccion.get("recipient", ""),
                            'amount': cantidad,
                            'timestamp': timestamp
                        })

        return sent_transactions

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
    
    def valid_proof(self, data_to_hash):
        hashed_data = hashlib.sha1(data_to_hash.encode()).hexdigest()
        if(hashed_data[:len(self.targetPrefix)] == self.targetPrefix):
            return hashed_data
        return -1