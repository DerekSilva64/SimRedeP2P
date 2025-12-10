"""
Teste completo da funcionalidade de visualização de grafos
"""

from p2p_network import P2PNetwork
from search_algorithms import SearchAlgorithms
from visualization import NetworkVisualizer
from datetime import datetime
import os

def test_complete_visualization():
    print("="*60)
    print("TESTE COMPLETO DE VISUALIZAÇÃO")
    print("="*60)
    
    # Carrega rede
    network = P2PNetwork()
    network.load_from_json('config-sala.json')
    print(f"\n✓ Rede carregada: {network.name}")
    
    # Executa buscas
    origin = 'n1'
    resource = 'r4'
    
    print(f"\nExecutando buscas para '{resource}' a partir de '{origin}'...")
    
    r1 = SearchAlgorithms.inudacao_search(network, origin, resource)
    r2 = SearchAlgorithms.caminho_aleatorio_search(network, origin, resource)
    r3 = SearchAlgorithms.informada_search(network, origin, resource)
    
    results = [
        {'name': 'Inundação', 'result': r1},
        {'name': 'Passeio Aleatório', 'result': r2},
        {'name': 'Busca Informada', 'result': r3}
    ]
    
    # Cria diretório
    os.makedirs('test_graphs', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Gera gráfico de barras
    print("\n1. Gerando gráfico de barras comparativo...")
    NetworkVisualizer.compare_algorithms_chart(results, f'test_graphs/comparison_{ts}.png')
    
    # Gera grafos da rede com caminhos
    print("\n2. Gerando grafos da rede com caminhos destacados...")
    for result_data in results:
        name = result_data['name'].lower().replace(' ', '_')
        NetworkVisualizer.plot_network_graph(
            network, 
            result_data['result'], 
            f'test_graphs/graph_{name}_{ts}.png'
        )
    
    # Gera grafo da rede sem busca
    print("\n3. Gerando grafo da rede (sem busca)...")
    NetworkVisualizer.plot_network_graph(
        network, 
        save_path=f'test_graphs/network_only_{ts}.png'
    )
    
    print("\n" + "="*60)
    print("✓ TESTE COMPLETO CONCLUÍDO COM SUCESSO!")
    print(f"  Todos os gráficos foram salvos em 'test_graphs/'")
    print("="*60)

if __name__ == "__main__":
    test_complete_visualization()
