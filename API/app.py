import os
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from os.path import join, dirname

from core.blockchain import Blockchain
from core.node_registration import NodeRegistration
from core.file_handling import save_chain_to_disk
          
app = Flask(__name__)

CORS(app)

# Configurar CORS para permitir solicitudes solo desde ciertos orígenes
CORS(app, origins='*')

# Genere una dirección global única para este nodo
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

node_registration = NodeRegistration()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'La transacción se agregará al bloque {index}'}
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
        if node_registration.resolve_conflicts():
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
            'message': "Nuevo bloque forjado",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    else:
        return 'Prueba no valida', 400

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
    connected_nodes = node_registration.get_connected_nodes()
    response = {
        'nodes': connected_nodes,
        'total_nodes': len(connected_nodes)
    }
    return jsonify(response), 200

@app.route('/connect', methods=['POST'])
def connect_to_nodes():
    values = request.get_json()
    node_registration.register_node_sender(values.get('address', []), values.get('type_node', []))

    # Resuelve conflictos para sincronizar con la cadena más larga entre los nodos conectados
    if node_registration.resolve_conflicts(blockchain.chain):
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
            save_chain_to_disk(chain, blockchain.current_transactions)
        return jsonify({'message': 'Actualizacion de cadena'}), 200
    else:
        return jsonify({'message': 'La cadena actual esta bien.'}), 200


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')

    load_dotenv(dotenv_path)
    node_registration.register_node_sender(f"{os.getenv('IP_NODE')}:{os.getenv('PORT')}", os.getenv('TYPE_NODE'))
    app.run(debug=os.getenv('FLASK_DEBUG'), port=os.getenv('PORT'))

