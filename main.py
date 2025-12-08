
import sys
import os
from datetime import datetime
from p2p_network import P2PNetwork
from search_algorithms import SearchAlgorithms
from visualization import NetworkVisualizer


def print_menu():
    """Imprime o menu principal."""
    print("\n" + "="*60)
    print("SIMULADOR DE REDE P2P - ALGORITMOS DE BUSCA")
    print("="*60)
    print("\nOpções:")
    print("  1 - Busca por Inundação (Flooding)")
    print("  2 - Busca por Passeio Aleatório (Random Walk)")
    print("  3 - Busca Informada (Informed Search)")
    print("  4 - Comparar todos os algoritmos")
    print("  5 - Comparar com gráficos")
    print("  6 - Visualizar grafo da rede")
    print("  7 - Mostrar informações da rede")
    print("  8 - Listar todos os recursos disponíveis")
    print("  0 - Sair")
    print("="*60)


def list_all_resources(network):
    """Lista todos os recursos disponíveis na rede."""
    print("\n" + "="*60)
    print("RECURSOS DISPONÍVEIS NA REDE")
    print("="*60)
    
    all_resources = {}
    for node in network.get_all_nodes():
        for resource in node.resources:
            if resource not in all_resources:
                all_resources[resource] = []
            all_resources[resource].append(node.node_id)
    
    for resource in sorted(all_resources.keys()):
        nodes = ", ".join(all_resources[resource])
        print(f"  • {resource}")
        print(f"    Localizado em: {nodes}")
    
    print("="*60 + "\n")


def compare_algorithms(network, origin_id, resource_name):
    """Compara todos os algoritmos de busca."""
    print("\n" + "="*60)
    print("COMPARAÇÃO DE ALGORITMOS")
    print("="*60)
    print(f"Origem: {origin_id}")
    print(f"Recurso: {resource_name}")
    print("="*60 + "\n")
    
    # Busca por Inundação
    result1 = SearchAlgorithms.inudacao_search(network, origin_id, resource_name)
    print(f"\n1. BUSCA POR INUNDAÇÃO")
    print(f"   Status: {'✓ Encontrado' if result1['found'] else '✗ Não encontrado'}")
    if result1['found']:
        print(f"   Encontrado em: {result1['found_at']}")
        print(f"   Saltos: {len(result1['path']) - 1}")
    print(f"   Nós visitados: {result1['nodes_visited']}")
    print(f"   Mensagens: {result1['messages_sent']}")
    
    # Busca por Passeio Aleatório
    result2 = SearchAlgorithms.caminho_aleatorio_search(network, origin_id, resource_name)
    print(f"\n2. BUSCA POR PASSEIO ALEATÓRIO")
    print(f"   Status: {'✓ Encontrado' if result2['found'] else '✗ Não encontrado'}")
    if result2['found']:
        print(f"   Encontrado em: {result2['found_at']}")
        print(f"   Saltos: {len(result2['path']) - 1}")
    print(f"   Nós visitados: {result2['nodes_visited']}")
    print(f"   Mensagens: {result2['messages_sent']}")
    
    # Busca Informada
    result3 = SearchAlgorithms.informada_search(network, origin_id, resource_name)
    print(f"\n3. BUSCA INFORMADA")
    print(f"   Status: {'✓ Encontrado' if result3['found'] else '✗ Não encontrado'}")
    if result3['found']:
        print(f"   Encontrado em: {result3['found_at']}")
        print(f"   Saltos: {len(result3['path']) - 1}")
    print(f"   Nós visitados: {result3['nodes_visited']}")
    print(f"   Mensagens: {result3['messages_sent']}")
    
    print("\n" + "="*60 + "\n")


def compare_algorithms_with_charts(network, origin_id, resource_name):
    """Compara algoritmos e gera gráfico de barras."""
    print("\n" + "="*60)
    print("COMPARAÇÃO COM GRÁFICOS")
    print("="*60)
    print(f"Origem: {origin_id}")
    print(f"Recurso: {resource_name}")
    print("="*60 + "\n")
    
    print("Executando buscas...")
    
    # Executa os três algoritmos
    result1 = SearchAlgorithms.inudacao_search(network, origin_id, resource_name)
    result2 = SearchAlgorithms.caminho_aleatorio_search(network, origin_id, resource_name)
    result3 = SearchAlgorithms.informada_search(network, origin_id, resource_name)
    
    # Prepara dados para visualização
    results_list = [
        {'name': 'Inundação', 'result': result1},
        {'name': 'Passeio Aleatório', 'result': result2},
        {'name': 'Busca Informada', 'result': result3}
    ]
    
    # Gera tabela comparativa
    NetworkVisualizer.create_comparison_table(results_list)
    
    # Cria diretório para gráficos se não existir
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Gera gráfico de barras
    print("Gerando gráfico de barras comparativo...")
    chart_path = f'graphs/comparison_{timestamp}.png'
    NetworkVisualizer.compare_algorithms_chart(results_list, save_path=chart_path)
    
    # Gera grafos para cada algoritmo
    print("\nGerando visualizações dos grafos...")
    for result_data in results_list:
        algo_name = result_data['name'].lower().replace(' ', '_')
        graph_path = f'graphs/graph_{algo_name}_{timestamp}.png'
        NetworkVisualizer.plot_network_graph(network, result_data['result'], save_path=graph_path)
    
    print("\n" + "="*60)
    print("✓ Todos os gráficos foram gerados com sucesso!")
    print(f"  Verifique a pasta 'graphs/' para visualizar os resultados.")
    print("="*60 + "\n")


def visualize_network_graph(network):
    """Visualiza o grafo da rede sem busca."""
    print("\n" + "="*60)
    print("VISUALIZAÇÃO DO GRAFO DA REDE")
    print("="*60)
    print(f"Rede: {network.name}")
    print(f"Total de nós: {len(network.nodes)}")
    print("="*60 + "\n")
    
    # Cria diretório para gráficos se não existir
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    graph_path = f'graphs/network_graph_{timestamp}.png'
    
    print("Gerando visualização do grafo...")
    NetworkVisualizer.plot_network_graph(network, save_path=graph_path)
    
    print("\n" + "="*60)
    print("✓ Grafo gerado com sucesso!")
    print(f"  Verifique o arquivo: {graph_path}")
    print("="*60 + "\n")


def main():
    """Função principal do programa."""
    print("\n" + "="*60)
    print("BEM-VINDO AO SIMULADOR DE REDE P2P")
    print("="*60)
    
    # Solicita o arquivo de configuração
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = input("\nDigite o caminho do arquivo de configuração JSON (padrão: config.json): ").strip()
        if not config_file:
            config_file = "config.json"
    
    # Carrega a rede
    print(f"\nCarregando rede a partir de: {config_file}")
    network = P2PNetwork()
    
    try:
        network.load_from_json(config_file)
        print("✓ Rede carregada com sucesso!")
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{config_file}' não encontrado.")
        return
    except Exception as e:
        print(f"✗ Erro ao carregar rede: {e}")
        return
    
    # Valida a rede
    print("\nValidando rede...")
    is_valid, errors = network.validate_network()
    
    if not is_valid:
        print("\n" + "="*60)
        print("✗ ERRO: A REDE NÃO É VÁLIDA")
        print("="*60)
        print("\nProblemas encontrados:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print("\n" + "="*60)
        print("\nPor favor, corrija o arquivo de configuração e tente novamente.")
        return
    else:
        print("✓ Rede validada com sucesso!")
    
    # Loop principal
    while True:
        print_menu()
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '0':
            print("\nEncerrando simulador. Até logo!")
            break
        
        elif choice == '6':
            visualize_network_graph(network)
        
        elif choice == '7':
            network.print_network_info()
        
        elif choice == '8':
            list_all_resources(network)
        
        elif choice in ['1', '2', '3', '4', '5']:
            # Solicita origem
            print(f"\nNós disponíveis: {', '.join(network.nodes.keys())}")
            origin_id = input("Digite o ID do nó de origem: ").strip()
            
            if origin_id not in network.nodes:
                print(f"✗ Erro: Nó '{origin_id}' não existe na rede.")
                continue
            
            # Solicita recurso
            resource_name = input("Digite o nome do recurso a buscar: ").strip()
            
            if not resource_name:
                print("✗ Erro: Nome do recurso não pode estar vazio.")
                continue
            
            # Executa busca
            if choice == '1':
                result = SearchAlgorithms.inudacao_search(network, origin_id, resource_name)
                network.print_search_result(result, "Busca por Inundação (Flooding)")
            
            elif choice == '2':
                result = SearchAlgorithms.caminho_aleatorio_search(network, origin_id, resource_name)
                network.print_search_result(result, "Busca por Passeio Aleatório (Random Walk)")
            
            elif choice == '3':
                result = SearchAlgorithms.informada_search(network, origin_id, resource_name)
                network.print_search_result(result, "Busca Informada (Informed Search)")
            
            elif choice == '4':
                compare_algorithms(network, origin_id, resource_name)
            
            elif choice == '5':
                compare_algorithms_with_charts(network, origin_id, resource_name)
        
        else:
            print("✗ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
