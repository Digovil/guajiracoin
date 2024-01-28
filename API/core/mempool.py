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
    
    def clean_mempool_transations(self):
        # Eliminar objetos
        if len(self.current_transactions) > 0 :
            lista_objetos = get_mempool()
            lista_objetos = [objeto for objeto in lista_objetos if objeto not in self.current_transactions]
            self.current_transactions = lista_objetos
            save_mempool_to_disk(lista_objetos)