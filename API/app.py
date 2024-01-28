import os
from uuid import uuid4
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from os.path import join, dirname

from core.blockchain import Blockchain
from core.node_registration import NodeRegistration
from core.mempool import Mempool
from core.file_handling import save_chain_to_disk
          
app = Flask(__name__)

CORS(app)

# Configurar CORS para permitir solicitudes solo desde ciertos orígenes
CORS(app, origins='*')

# Genere una dirección global única para este nodo
node_identifier     = str(uuid4()).replace('-', '')
blockchain          = Blockchain()
mempool             = Mempool()
node_registration   = NodeRegistration()

# Cargando todas las transacciones que existen en la mempool
# print("Primera ejecucion")
mempool.get_transactions()

# Cargando la blockchain
# print("Segunda ejecucion")
blockchain.get_blockchain()

# Cargando el registro de nodos conectado
# print("Tercera ejecución")
aux = node_registration.get_connected_nodes()

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    response = {
        'transactions': mempool.current_transactions,
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Verifique que los campos obligatorios estén en los datos publicados
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Faltan campos', 400

    # Crear una nueva transacción
    # index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    index = mempool.new_transaction(sender=values['sender'], recipient=values['recipient'], amount=values['amount'], last_block=blockchain.last_block)
    response = {'message': f'La transacción se agregará al bloque {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['POST'])
def mine():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['proof', 'miner_address']
    if not all(k in values for k in required):
        return 'Faltan campos', 400

    proof = values['proof']
    miner_address = values['miner_address']

    last_block = blockchain.last_block
    last_proof = last_block['proof']
    # Validar la prueba de trabajo.
    if blockchain.valid_proof(proof):
        # Forja el nuevo bloque agregándolo a la cadena.
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, mempool.current_transactions, previous_hash)
        mempool.clean_mempool_transations()
        
        # Resuelve conflictos para sincronizar con la cadena más larga entre los nodos conectados
        if len(node_registration.nodes) > 0:
            if node_registration.resolve_conflicts(blockchain.chain):
                print('Conexión exitosa y sincronización realizada.')
            else:
                print('Conexión exitosa, pero no se encontraron conflictos. La cadena actual es la más larga.')

        # Recompensa al minero
        mempool.new_transaction(
            sender="0",
            recipient=miner_address,
            amount=1,
            last_block=blockchain.last_block
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
    node_registration.register_node_sender(f"{os.getenv('IP_NODE')}:{os.getenv('PORT')}", os.getenv('TYPE_NODE'), me_user=True)
    app.run(debug=os.getenv('FLASK_DEBUG'), host='0.0.0.0', port=os.getenv('PORT'), ssl_context="adhoc")

