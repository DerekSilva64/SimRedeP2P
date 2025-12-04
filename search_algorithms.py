
from collections import deque
import random


class SearchAlgorithms:
    
    @staticmethod
    def inudacao_search(network, origin_id, resource_name, ttl=10):
        
        origin_node = network.get_node(origin_id)
        if not origin_node:
            return {
                'found': False,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': None,
                'path': [],
                'nodes_visited': 0,
                'messages_sent': 0
            }
        
        # Verifica se o nó de origem tem o recurso
        if origin_node.has_resource(resource_name):
            return {
                'found': True,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': origin_id,
                'path': [origin_id],
                'nodes_visited': 1,
                'messages_sent': 0
            }
        
        # BFS com controle de TTL
        visited = set()
        queue = deque([(origin_node, 0, [origin_id])])  # (nó, profundidade, caminho)
        visited.add(origin_id)
        messages_sent = 0
        
        while queue:
            current_node, depth, path = queue.popleft()
            
            # Verifica TTL
            if depth >= ttl:
                continue
            
            # Explora vizinhos
            for neighbor in current_node.neighbors:
                messages_sent += 1
                
                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    new_path = path + [neighbor.node_id]
                    
                    # Verifica se encontrou o recurso
                    if neighbor.has_resource(resource_name):
                        return {
                            'found': True,
                            'resource': resource_name,
                            'origin': origin_id,
                            'found_at': neighbor.node_id,
                            'path': new_path,
                            'nodes_visited': len(visited),
                            'messages_sent': messages_sent
                        }
                    
                    queue.append((neighbor, depth + 1, new_path))
        
        # Recurso não encontrado
        return {
            'found': False,
            'resource': resource_name,
            'origin': origin_id,
            'found_at': None,
            'path': list(visited),
            'nodes_visited': len(visited),
            'messages_sent': messages_sent
        }
    
    @staticmethod
    def caminho_aleatorio_search(network, origin_id, resource_name, max_steps=50):
        origin_node = network.get_node(origin_id)
        if not origin_node:
            return {
                'found': False,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': None,
                'path': [],
                'nodes_visited': 0,
                'messages_sent': 0
            }
        
        # Verifica se o nó de origem tem o recurso
        if origin_node.has_resource(resource_name):
            return {
                'found': True,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': origin_id,
                'path': [origin_id],
                'nodes_visited': 1,
                'messages_sent': 0
            }
        
        current_node = origin_node
        path = [origin_id]
        visited = {origin_id}
        messages_sent = 0
        
        for step in range(max_steps):
            # Se não há vizinhos, termina
            if not current_node.neighbors:
                break
            
            # Escolhe um vizinho aleatório
            next_node = random.choice(current_node.neighbors)
            messages_sent += 1
            path.append(next_node.node_id)
            visited.add(next_node.node_id)
            
            # Verifica se encontrou o recurso
            if next_node.has_resource(resource_name):
                return {
                    'found': True,
                    'resource': resource_name,
                    'origin': origin_id,
                    'found_at': next_node.node_id,
                    'path': path,
                    'nodes_visited': len(visited),
                    'messages_sent': messages_sent
                }
            
            current_node = next_node
        
        # Recurso não encontrado
        return {
            'found': False,
            'resource': resource_name,
            'origin': origin_id,
            'found_at': None,
            'path': path,
            'nodes_visited': len(visited),
            'messages_sent': messages_sent
        }
    
    @staticmethod
    def informada_search(network, origin_id, resource_name, max_nodes=20):

        origin_node = network.get_node(origin_id)
        if not origin_node:
            return {
                'found': False,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': None,
                'path': [],
                'nodes_visited': 0,
                'messages_sent': 0
            }
        
        # Verifica se o nó de origem tem o recurso
        if origin_node.has_resource(resource_name):
            return {
                'found': True,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': origin_id,
                'path': [origin_id],
                'nodes_visited': 1,
                'messages_sent': 0
            }
        
        # Busca em largura informada (prioriza vizinhos com mais sucessos)
        visited = set()
        # Fila de prioridade: (nó, caminho)
        queue = deque([(origin_node, [origin_id])])
        visited.add(origin_id)
        messages_sent = 0
        path_to_found = []
        
        while queue and len(visited) < max_nodes:
            current_node, path = queue.popleft()
            
            # Ordena vizinhos por taxa de sucesso (busca informada)
            sorted_neighbors = current_node.get_best_neighbors()
            
            for neighbor in sorted_neighbors:
                messages_sent += 1
                
                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    new_path = path + [neighbor.node_id]
                    
                    # Verifica se encontrou o recurso
                    if neighbor.has_resource(resource_name):
                        # Atualiza contadores de sucesso ao longo do caminho
                        for i in range(len(new_path) - 1):
                            node = network.get_node(new_path[i])
                            if node and i + 1 < len(new_path):
                                node.increment_success(new_path[i + 1])
                        
                        return {
                            'found': True,
                            'resource': resource_name,
                            'origin': origin_id,
                            'found_at': neighbor.node_id,
                            'path': new_path,
                            'nodes_visited': len(visited),
                            'messages_sent': messages_sent
                        }
                    
                    queue.append((neighbor, new_path))
                    
                if len(visited) >= max_nodes:
                    break
        
        # Recurso não encontrado
        return {
            'found': False,
            'resource': resource_name,
            'origin': origin_id,
            'found_at': None,
            'path': list(visited),
            'nodes_visited': len(visited),
            'messages_sent': messages_sent
        }
