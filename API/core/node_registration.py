from urllib.parse import urlparse
import requests
from core.file_handling import *
from core.blockchain import Blockchain

class NodeRegistration:
    def __init__(self):
        self.nodes = []
        load_nodes_from_disk(self.nodes)

    def get_connected_nodes(self):
        return self.nodes
    
    def register_node_sender(self, address, type_node):
        parsed_url = urlparse(address)
        self.nodes.append({"address": parsed_url.path, "type_node": type_node})
        save_nodes_to_disk(self.nodes) 

    def resolve_conflicts(self, chain):
        neighbors = self.nodes
        new_chain = None

        # Sólo buscamos cadenas más largas que las nuestras.
        max_length = len(chain)

        try:

            # Toma y verifica las cadenas de todos los nodos de nuestra red.
            for node in neighbors:
                response = requests.get(f'{node["address"]}/chain')
                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']
        
                    # Comprueba si la longitud es más larga y la cadena es válida.
                    if length > max_length and Blockchain.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                    elif length < max_length and Blockchain.valid_chain(chain):
                        requests.post(f'{node["address"]}/update_chain', json={'chain': chain})

        except Exception as e:
            print(f"Se produjo el error {e}")

        # Reemplazar nuestra cadena si descubrimos una cadena nueva y válida más larga que la nuestra.
        if new_chain:
            chain = new_chain
            save_chain_to_disk(chain)  # Guarde la cadena actualizada en el disco
            return True

        return False