import json
import os

# Blockchain
def get_chain():
    lista_objetos = []
    if os.path.exists('./data/blockchain.json'):
        with open('./data/blockchain.json', 'r') as f:
            lista_objetos = json.load(f)
    return lista_objetos

def load_chain_from_disk(chain):
    if os.path.exists('./data/blockchain.json'):
        with open('./data/blockchain.json', 'r') as f:
            chain = json.load(f)
    else:
        # Create the blockchain.json file if it doesn't exist
        save_chain_to_disk(chain)

def save_chain_to_disk(chain):
    data = chain
    with open('./data/blockchain.json', 'w') as f:
        json.dump(data, f, indent=4)

# Nodos

def get_nodes():
    lista_objetos = []
    if os.path.exists('./data/nodes.json'):
        with open('./data/nodes.json', 'r') as f:
            lista_objetos = json.load(f)
    return lista_objetos

def load_nodes_from_disk(nodes):
    if os.path.exists('./data/nodes.json'):
        with open('./data/nodes.json', 'r') as f:
            nodes = json.load(f)
    else:
        # Create the nodes.json file if it doesn't exist
        save_nodes_to_disk(nodes)
        
def save_nodes_to_disk(nodes):
    with open('./data/nodes.json', 'w') as f:
        json.dump(nodes, f, indent=4)
        
def delete_nodes_transations(objetos_a_eliminar):
    # Eliminar objetos
    if objetos_a_eliminar:
        lista_objetos = get_nodes()
        lista_objetos = [objeto for objeto in lista_objetos if objeto not in objetos_a_eliminar]
        save_nodes_to_disk(lista_objetos)
        
# Mempool

def get_mempool():
    lista_objetos = []
    if os.path.exists('./data/mempool.json'):
        with open('./data/mempool.json', 'r') as f:
            lista_objetos = json.load(f)
    return lista_objetos

def load_mempool_from_disk(mempool):
    mempool = get_mempool()
    
    if len(mempool) == 0:        
        save_mempool_to_disk(mempool)
        
def save_mempool_to_disk(mempool):
    with open('./data/mempool.json', 'w') as f:
        json.dump(mempool, f, indent=4)
        

