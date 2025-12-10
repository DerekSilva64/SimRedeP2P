
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
        
        # Flooding: propaga para todos os nós até TTL, não para ao encontrar
        visited = set()
        visited_list = []  # Mantém ordem de visitação
        queue = deque([(origin_node, 0, [origin_id])])  # (nó, profundidade, caminho)
        visited.add(origin_id)
        visited_list.append(origin_id)
        messages_sent = 0
        found_at = None
        found_path = None
        
        while queue:
            current_node, depth, path = queue.popleft()
            
            # Verifica TTL
            if depth >= ttl:
                continue
            
            # Explora TODOS os vizinhos (flooding continua mesmo após encontrar)
            for neighbor in current_node.neighbors:
                messages_sent += 1
                
                if neighbor.node_id not in visited:
                    visited.add(neighbor.node_id)
                    visited_list.append(neighbor.node_id)
                    new_path = path + [neighbor.node_id]
                    
                    # Verifica se encontrou o recurso (mas continua propagando)
                    if neighbor.has_resource(resource_name) and found_at is None:
                        found_at = neighbor.node_id
                        found_path = new_path
                    
                    # Continua propagando independentemente de ter encontrado
                    queue.append((neighbor, depth + 1, new_path))
        
        # Retorna resultado
        if found_at:
            return {
                'found': True,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': found_at,
                'path': found_path,
                'visited_nodes': visited_list,  # Todos os nós visitados
                'nodes_visited': len(visited),
                'messages_sent': messages_sent
            }
        else:
            return {
                'found': False,
                'resource': resource_name,
                'origin': origin_id,
                'found_at': None,
                'path': visited_list,
                'visited_nodes': visited_list,
                'nodes_visited': len(visited),
                'messages_sent': messages_sent
            }
    
    @staticmethod
    def caminho_aleatorio_search(network, origin_id, resource_name, ttl=10):

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
        
        # Random Walk: cada tentativa caminha por até TTL passos
        # Tenta múltiplos caminhos aleatórios até encontrar ou esgotar tentativas
        visited_global = set([origin_id])
        messages_sent = 0
        max_attempts = 10  # Número máximo de caminhos diferentes a tentar
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            # Inicia um novo caminho da origem (cada um com TTL próprio)
            current_node = origin_node
            previous_node = None
            local_visited = set([origin_id])
            current_path = [origin_id]
            steps = 0
            
            # Caminha aleatoriamente por até TTL passos
            while steps < ttl:
                # Filtra vizinhos (não volta pro anterior e não revisita neste caminho)
                available = [n for n in current_node.neighbors 
                            if n.node_id not in local_visited and 
                            (previous_node is None or n.node_id != previous_node.node_id)]
                
                if not available:
                    # Sem vizinhos disponíveis, reinicia da origem com novo caminho
                    break
                
                # Escolhe um vizinho aleatório
                chosen_node = random.choice(available)
                messages_sent += 1
                steps += 1
                
                # Marca como visitado
                local_visited.add(chosen_node.node_id)
                visited_global.add(chosen_node.node_id)
                current_path.append(chosen_node.node_id)
                
                # Verifica se encontrou
                if chosen_node.has_resource(resource_name):
                    return {
                        'found': True,
                        'resource': resource_name,
                        'origin': origin_id,
                        'found_at': chosen_node.node_id,
                        'path': current_path,
                        'visited_nodes': list(visited_global),
                        'nodes_visited': len(visited_global),
                        'messages_sent': messages_sent
                    }
                
                # Avança
                previous_node = current_node
                current_node = chosen_node
            
            # TTL esgotado neste caminho, tenta outro
        
        # Não encontrou
        return {
            'found': False,
            'resource': resource_name,
            'origin': origin_id,
            'found_at': None,
            'path': [origin_id],
            'visited_nodes': list(visited_global),
            'nodes_visited': len(visited_global),
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
                            'visited_nodes': list(visited),
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
            'visited_nodes': list(visited),
            'nodes_visited': len(visited),
            'messages_sent': messages_sent
        }
