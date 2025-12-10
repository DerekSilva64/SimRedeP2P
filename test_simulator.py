"""
Script de teste para demonstrar as funcionalidades do simulador P2P
"""

from p2p_network import P2PNetwork
from search_algorithms import SearchAlgorithms
from visualization import NetworkVisualizer
import os
from datetime import datetime


def test_basic_search():
    """Testa busca básica com todos os algoritmos."""
    print("\n" + "="*60)
    print("TESTE 1: BUSCA BÁSICA")
    print("="*60)
    
    # Carrega rede
    network = P2PNetwork()
    network.load_from_json('config-menor.json')
    
    # Valida rede
    is_valid, errors = network.validate_network()
    if not is_valid:
        print("Erros encontrados:")
        for error in errors:
            print(f"  - {error}")
        return
    
    print("✓ Rede carregada e validada com sucesso!")
    
    # Testa cada algoritmo
    origin = 'node1'
    resource = 'video3.mp4'
    
    print(f"\nBuscando '{resource}' a partir de '{origin}'...")
    
    result1 = SearchAlgorithms.inudacao_search(network, origin, resource)
    print(f"\nInundação: {'✓ Encontrado' if result1['found'] else '✗ Não encontrado'}")
    print(f"  Nós: {result1['nodes_visited']}, Mensagens: {result1['messages_sent']}")
    
    result2 = SearchAlgorithms.caminho_aleatorio_search(network, origin, resource)
    print(f"\nPasseio Aleatório: {'✓ Encontrado' if result2['found'] else '✗ Não encontrado'}")
    print(f"  Nós: {result2['nodes_visited']}, Mensagens: {result2['messages_sent']}")
    
    result3 = SearchAlgorithms.informada_search(network, origin, resource)
    print(f"\nBusca Informada: {'✓ Encontrado' if result3['found'] else '✗ Não encontrado'}")
    print(f"  Nós: {result3['nodes_visited']}, Mensagens: {result3['messages_sent']}")


def test_visualization():
    """Testa geração de gráficos."""
    print("\n" + "="*60)
    print("TESTE 2: VISUALIZAÇÃO GRÁFICA")
    print("="*60)
    
    # Carrega rede
    network = P2PNetwork()
    network.load_from_json('config-menor.json')
    
    # Executa buscas
    origin = 'node1'
    resource = 'video3.mp4'
    
    print(f"\nExecutando buscas para '{resource}'...")
    
    result1 = SearchAlgorithms.inudacao_search(network, origin, resource)
    result2 = SearchAlgorithms.caminho_aleatorio_search(network, origin, resource)
    result3 = SearchAlgorithms.informada_search(network, origin, resource)
    
    results_list = [
        {'name': 'Inundação', 'result': result1},
        {'name': 'Passeio Aleatório', 'result': result2},
        {'name': 'Busca Informada', 'result': result3}
    ]
    
    # Cria diretório
    if not os.path.exists('test_graphs'):
        os.makedirs('test_graphs')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gera visualizações
    print("\nGerando gráficos...")
    
    print("  1. Tabela comparativa")
    NetworkVisualizer.create_comparison_table(results_list)
    
    print("  2. Gráfico de barras comparativo")
    NetworkVisualizer.compare_algorithms_chart(
        results_list, 
        save_path=f'test_graphs/comparison_{timestamp}.png'
    )
    
    print("\n✓ Gráfico gerado em 'test_graphs/'")


def test_validation():
    """Testa validações da rede."""
    print("\n" + "="*60)
    print("TESTE 3: VALIDAÇÕES DA REDE")
    print("="*60)
    
    # Testa rede válida
    print("\nTestando rede válida (config-menor.json)...")
    network1 = P2PNetwork()
    network1.load_from_json('config-menor.json')
    is_valid, errors = network1.validate_network()
    
    if is_valid:
        print("✓ Rede válida!")
    else:
        print("✗ Rede inválida:")
        for error in errors:
            print(f"  - {error}")


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "="*70)
    print("EXECUTANDO TESTES DO SIMULADOR P2P")
    print("="*70)
    
    try:
        test_basic_search()
        test_validation()
        test_visualization()
        
        print("\n" + "="*70)
        print("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n✗ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
