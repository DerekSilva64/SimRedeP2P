
class Node:
    
    def __init__(self, node_id, name, resources=None):

        self.node_id = node_id
        self.name = name
        self.resources = resources if resources else []
        self.neighbors = []
        self.success_count = {}  # Para busca informada
    
    def add_neighbor(self, neighbor): # Adiciona um vizinho ao nó

        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            self.success_count[neighbor.node_id] = 0
    

    def has_resource(self, resource_name): # Olha se o nó tem o recurso
        return resource_name in self.resources
    
    def increment_success(self, neighbor_id): # Contador de sucesso (busca informada)

        if neighbor_id in self.success_count:
            self.success_count[neighbor_id] += 1
    
    def get_best_neighbors(self): # Retorna vizinhos ordenados por sucesso (busca informada)

        return sorted(self.neighbors, 
                     key=lambda n: self.success_count.get(n.node_id, 0), 
                     reverse=True)
    
    def __str__(self):
        return f"{self.name} ({self.node_id})"
    
    def __repr__(self):
        return f"Node({self.node_id})"
