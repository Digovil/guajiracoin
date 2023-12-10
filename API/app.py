import hashlib
import json
import os
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

class Blockchain:
    def __init__(self, ip, port):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        self.miners = []  # Agrega una lista para almacenar información sobre los mineros
        self.ip = ip  # Nueva línea para almacenar la dirección IP del nodo
        self.port = port  # Nueva línea para almacenar el puerto del nodo
        self.load_chain_from_disk()

        # Genesis block
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

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        self.save_chain_to_disk()  # Save the chain to disk after adding a new block
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        # Añade el cálculo de la dificultad basada en la información recopilada
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        return hashlib.sha1(json.dumps(block, sort_keys=True).encode()).hexdigest()

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(f"{parsed_url.scheme}://{parsed_url.netloc}")
        _ip = parsed_url.netloc.split("")[0]
        _port = parsed_url.netloc.split(":")[1]
        connect_payload = {'nodes': f"{self.ip}:{self.port}"}
        requests.post(f'{parsed_url.scheme}://{_ip}:{_port}/connect', json=connect_payload)
            
    def register_node_sender(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(f"https://{parsed_url.scheme}:{parsed_url.path}")


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
    
    def get_connected_nodes(self):
        return list(self.nodes)

    def resolve_conflicts(self):
        neighbors = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        try:

            # Grab and verify the chains from all the nodes in our network
            for node in neighbors:
                response = requests.get(f'{node}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
        
                    # Check if the length is longer and the chain is valid
                    if length > max_length and self.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                    elif length < max_length and self.valid_chain(chain):
                        requests.post(f'{node}/update_chain', json={'chain': self.chain})

        except Exception as e:
            print(f"Se produjo el error {e}")

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            self.save_chain_to_disk()  # Save the updated chain to disk
            return True

        return False

    @staticmethod
    def valid_proof(proof):
        if proof == 100: return True
        
        return proof[:4] == "0000"

    def load_chain_from_disk(self):
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as f:
                data = json.load(f)
                self.chain = data['chain']
                self.current_transactions = data['current_transactions']
        else:
            # Create the blockchain.json file if it doesn't exist
            self.save_chain_to_disk()

    def save_chain_to_disk(self):
        data = {
            'chain': self.chain,
            'current_transactions': self.current_transactions,
        }
        with open('blockchain.json', 'w') as f:
            json.dump(data, f, indent=4)
            
# Instantiate the Node
app = Flask(__name__)

CORS(app)

# Configurar CORS para permitir solicitudes solo desde ciertos orígenes
CORS(app, origins='*')

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain("nodo1-waycoin.onrender.com", 443)
blockchain.nodes.add(f"https://nodo2-waycoin.onrender.com:443")

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def mine():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['proof', 'miner_address']
    if not all(k in values for k in required):
        return 'Missing values', 400

    proof = values['proof']
    miner_address = values['miner_address']

    # Validate the proof of work
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    if blockchain.valid_proof(proof):
        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        # Resuelve conflictos para sincronizar con la cadena más larga entre los nodos conectados
        if blockchain.resolve_conflicts():
            print('Conexión exitosa y sincronización realizada.')
        else:
            print('Conexión exitosa, pero no se encontraron conflictos. La cadena actual es la más larga.')

        # Reward the miner
        blockchain.new_transaction(
            sender="0",
            recipient=miner_address,
            amount=1,
        )

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    else:
        return 'Invalid proof', 400

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    response = {
        'transactions': blockchain.current_transactions,
    }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def get_connected_nodes():
    connected_nodes = blockchain.get_connected_nodes()
    response = {
        'nodes': connected_nodes,
        'total_nodes': len(connected_nodes)
    }
    return jsonify(response), 200

@app.route('/connect', methods=['POST'])
def connect_to_nodes():
    values = request.get_json()
    nodes_to_connect = values.get('nodes', [])
    blockchain.register_node_sender(nodes_to_connect)

    # Resuelve conflictos para sincronizar con la cadena más larga entre los nodos conectados
    if blockchain.resolve_conflicts():
        return jsonify({'message': 'Conexión exitosa y sincronización realizada.'}), 200
    else:
        return jsonify({'message': 'Conexión exitosa, pero no se encontraron conflictos. La cadena actual es la más larga.'}), 200


@app.route('/update_chain', methods=['POST'])
def update_chain():
    values = request.get_json()
    chain = values.get('chain', [])

    is_valid_chain = blockchain.valid_chain(chain)
    if is_valid_chain:
        if len(chain)>len(blockchain.chain):
            blockchain.chain = chain
            blockchain.save_chain_to_disk()
        return jsonify({'message': 'Actualizacion de cadena'}), 200
    else:
        return jsonify({'message': 'La cadena actual esta bien.'}), 200


if __name__ == '__main__':
    app.run()
