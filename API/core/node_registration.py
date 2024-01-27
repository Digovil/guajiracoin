from urllib.parse import urlparse
import requests
from core.file_handling import *
from core.blockchain import Blockchain
import socket

class NodeRegistration:
    def __init__(self):
        self.nodes = set()
        self.ip_address = socket.gethostbyname(socket.gethostname())

                
        
    def get_connected_nodes(self):
        return list(self.nodes)
    
    @staticmethod
    def register_node_sender(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(f"https://{parsed_url.scheme}:{parsed_url.path}")

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
                    if length > max_length and Blockchain.valid_chain(chain):
                        max_length = length
                        new_chain = chain
                    elif length < max_length and Blockchain.valid_chain(chain):
                        requests.post(f'{node}/update_chain', json={'chain': self.chain})

        except Exception as e:
            print(f"Se produjo el error {e}")

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            save_chain_to_disk()  # Save the updated chain to disk
            return True

        return False