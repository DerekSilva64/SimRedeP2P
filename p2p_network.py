
import json
from node import Node


class P2PNetwork:
    
    def __init__(self):
        
        self.nodes = {}
        self.name = ""
        self.description = ""
    
    def load_from_json(self, filename):

        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Carrega informações da rede
        network_info = config.get('network', {})
        self.name = network_info.get('name', 'Unnamed Network')
        self.description = network_info.get('description', '')
        
        # Cria os nós
        for node_data in config['nodes']:
            node = Node(
                node_id=node_data['id'],
                name=node_data['name'],
                resources=node_data.get('resources', [])
            )
            self.nodes[node.node_id] = node
        
        # Cria as conexões (bidirecional)
        for conn in config['connections']:
            from_node = self.nodes[conn['from']]
            to_node = self.nodes[conn['to']]
            from_node.add_neighbor(to_node)
            to_node.add_neighbor(from_node)
    
    def get_node(self, node_id):
        return self.nodes.get(node_id)
    
    def get_all_nodes(self):
        return list(self.nodes.values())
    
    def print_network_info(self):
        print(f"\n{'='*60}")
        print(f"Rede: {self.name}")
        if self.description:
            print(f"Descrição: {self.description}")
        print(f"Total de nós: {len(self.nodes)}")
        print(f"{'='*60}\n")
        
        print("Nós e suas conexões:")
        for node_id, node in self.nodes.items():
            neighbors = ', '.join([n.node_id for n in node.neighbors])
            resources = ', '.join(node.resources) if node.resources else 'nenhum'
            print(f"\n  {node.name} ({node_id})")
            print(f"    Recursos: {resources}")
            print(f"    Vizinhos: {neighbors if neighbors else 'nenhum'}")
        print(f"\n{'='*60}\n")
    
    def print_search_result(self, result, algorithm_name):
        print(f"\n{'='*60}")
        print(f"Algoritmo: {algorithm_name}")
        print(f"{'='*60}")
        print(f"Recurso procurado: {result['resource']}")
        print(f"Nó de origem: {result['origin']}")
        
        if result['found']:
            print(f"\n✓ RECURSO ENCONTRADO!")
            print(f"  Encontrado em: {result['found_at']}")
            print(f"  Caminho percorrido: {' -> '.join(result['path'])}")
            print(f"  Número de saltos: {len(result['path']) - 1}")
        else:
            print(f"\n✗ RECURSO NÃO ENCONTRADO")
            if result['path']:
                print(f"  Nós visitados: {' -> '.join(result['path'])}")
        
        print(f"  Total de nós visitados: {result['nodes_visited']}")
        print(f"  Mensagens enviadas: {result['messages_sent']}")
        print(f"{'='*60}\n")
