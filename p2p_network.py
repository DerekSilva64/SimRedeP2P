
import json
from node import Node


class P2PNetwork:
    
    def __init__(self):
        
        self.nodes = {}
        self.name = ""
        self.description = ""
        self.min_neighbors = None
        self.max_neighbors = None
    
    def load_from_json(self, filename):

        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Carrega informações da rede
        network_info = config.get('network', {})
        self.name = network_info.get('name', 'Unnamed Network')
        self.description = network_info.get('description', '')
        self.min_neighbors = network_info.get('min_neighbors')
        self.max_neighbors = network_info.get('max_neighbors')
        
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
    
    def _is_connected_bfs(self):
        """Verifica se a rede está conectada usando BFS."""
        if not self.nodes:
            return True
        
        # Começa de um nó qualquer
        start_node = next(iter(self.nodes.values()))
        visited = set()
        queue = [start_node]
        visited.add(start_node.node_id)
        
        while queue:
            current = queue.pop(0)
            for neighbor in current.neighbors:
                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    queue.append(neighbor)
        
        # Se visitou todos os nós, a rede está conectada
        return len(visited) == len(self.nodes)
    
    def validate_network(self):
        """Valida a rede de acordo com as regras especificadas.
        
        Retorna:
            tuple: (is_valid, errors) onde is_valid é um booleano e errors é uma lista de erros.
        """
        errors = []
        
        # 1. Verifica se a rede está conectada (não particionada)
        if not self._is_connected_bfs():
            errors.append("A rede está particionada. Existem nós que não podem ser alcançados a partir de outros nós.")
        
        # 2. Verifica os limites de vizinhos (se especificados)
        if self.min_neighbors is not None or self.max_neighbors is not None:
            for node_id, node in self.nodes.items():
                num_neighbors = len(node.neighbors)
                
                if self.min_neighbors is not None and num_neighbors < self.min_neighbors:
                    errors.append(f"O nó '{node_id}' tem {num_neighbors} vizinhos, mas o mínimo é {self.min_neighbors}.")
                
                if self.max_neighbors is not None and num_neighbors > self.max_neighbors:
                    errors.append(f"O nó '{node_id}' tem {num_neighbors} vizinhos, mas o máximo é {self.max_neighbors}.")
        
        # 3. Verifica se há nós sem recursos
        for node_id, node in self.nodes.items():
            if not node.resources or len(node.resources) == 0:
                errors.append(f"O nó '{node_id}' não possui recursos.")
        
        # 4. Verifica se há arestas de um nó para ele mesmo
        for node_id, node in self.nodes.items():
            for neighbor in node.neighbors:
                if neighbor.node_id == node_id:
                    errors.append(f"O nó '{node_id}' possui uma aresta para ele mesmo (self-loop).")
        
        return len(errors) == 0, errors
    
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
