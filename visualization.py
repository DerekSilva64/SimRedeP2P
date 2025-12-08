import matplotlib.pyplot as plt
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False


class NetworkVisualizer:
    """Classe para criar visualizações comparativas dos algoritmos de busca."""
    
    @staticmethod
    def compare_algorithms_chart(results_list, save_path=None):
        """
        Cria gráficos de barras comparativos entre os algoritmos.
        
        Args:
            results_list: Lista de dicionários com resultados dos algoritmos
                         Cada item deve ter: 'name', 'result' (resultado da busca)
            save_path: Caminho opcional para salvar o gráfico
        """
        if not results_list:
            print("Nenhum resultado para visualizar.")
            return
        
        # Extrai dados
        algorithm_names = [r['name'] for r in results_list]
        nodes_visited = [r['result']['nodes_visited'] for r in results_list]
        messages_sent = [r['result']['messages_sent'] for r in results_list]
        found = [r['result']['found'] for r in results_list]
        hops = [len(r['result']['path']) - 1 if r['result']['found'] else 0 for r in results_list]
        
        # Configura o layout dos subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Comparação de Algoritmos de Busca P2P', fontsize=16, fontweight='bold')
        
        colors = ['#3498db', '#e74c3c', '#2ecc71']
        
        # Gráfico 1: Nós Visitados
        bars1 = ax1.bar(algorithm_names, nodes_visited, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Quantidade', fontsize=11, fontweight='bold')
        ax1.set_title('Nós Visitados', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Adiciona valores nas barras
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 2: Mensagens Enviadas
        bars2 = ax2.bar(algorithm_names, messages_sent, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('Quantidade', fontsize=11, fontweight='bold')
        ax2.set_title('Mensagens Enviadas', fontsize=12, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 3: Taxa de Sucesso
        success_rate = [100 if f else 0 for f in found]
        bars3 = ax3.bar(algorithm_names, success_rate, color=colors, alpha=0.7, edgecolor='black')
        ax3.set_ylabel('Porcentagem (%)', fontsize=11, fontweight='bold')
        ax3.set_title('Taxa de Sucesso', fontsize=12, fontweight='bold')
        ax3.set_ylim(0, 110)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}%',
                    ha='center', va='bottom', fontweight='bold')
        
        # Gráfico 4: Número de Saltos (apenas para algoritmos que encontraram)
        bars4 = ax4.bar(algorithm_names, hops, color=colors, alpha=0.7, edgecolor='black')
        ax4.set_ylabel('Quantidade', fontsize=11, fontweight='bold')
        ax4.set_title('Número de Saltos (quando encontrado)', fontsize=12, fontweight='bold')
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars4:
            height = bar.get_height()
            if height > 0:
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Salva ou exibe
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"\n✓ Gráfico salvo em: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    @staticmethod
    def create_comparison_table(results_list):
        """
        Cria uma tabela formatada comparando os resultados.
        
        Args:
            results_list: Lista de dicionários com resultados dos algoritmos
        """
        print("\n" + "="*80)
        print("TABELA COMPARATIVA DE RESULTADOS")
        print("="*80)
        
        # Cabeçalho
        print(f"{'Algoritmo':<25} {'Sucesso':<10} {'Nós':<10} {'Mensagens':<12} {'Saltos':<10}")
        print("-"*80)
        
        # Dados
        for result in results_list:
            name = result['name']
            r = result['result']
            success = "✓ Sim" if r['found'] else "✗ Não"
            nodes = r['nodes_visited']
            messages = r['messages_sent']
            hops = len(r['path']) - 1 if r['found'] else "-"
            
            print(f"{name:<25} {success:<10} {nodes:<10} {messages:<12} {hops:<10}")
        
        print("="*80 + "\n")
    
    @staticmethod
    def plot_network_graph(network, result=None, save_path=None):
        """
        Cria uma visualização do grafo da rede.
        
        Args:
            network: Objeto P2PNetwork
            result: Resultado da busca (opcional, para destacar caminho)
            save_path: Caminho opcional para salvar o gráfico
        """
        if not HAS_NETWORKX:
            print("\n⚠ NetworkX não está instalado. Visualização do grafo não disponível.")
            print("  Instale com: pip install networkx")
            return
        
        # Cria grafo
        G = nx.Graph()
        
        # Adiciona nós
        for node_id in network.nodes:
            G.add_node(node_id)
        
        # Adiciona arestas (evita duplicatas)
        edges_added = set()
        for node_id, node in network.nodes.items():
            for neighbor in node.neighbors:
                edge = tuple(sorted([node_id, neighbor.node_id]))
                if edge not in edges_added:
                    G.add_edge(node_id, neighbor.node_id)
                    edges_added.add(edge)
        
        # Layout
        pos = nx.spring_layout(G, seed=42, k=1.5, iterations=50)
        
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Define cores e tamanhos dos nós
        if result:
            # Com resultado de busca - destaca caminho
            node_colors = []
            node_sizes = []
            
            for node_id in G.nodes():
                if node_id == result['origin']:
                    node_colors.append('#2ecc71')  # Verde - origem
                    node_sizes.append(700)
                elif result['found'] and node_id == result['found_at']:
                    node_colors.append('#e74c3c')  # Vermelho - encontrado
                    node_sizes.append(700)
                elif node_id in result['path']:
                    node_colors.append('#3498db')  # Azul - visitado
                    node_sizes.append(500)
                else:
                    node_colors.append('#95a5a6')  # Cinza - não visitado
                    node_sizes.append(300)
            
            # Desenha arestas
            nx.draw_networkx_edges(G, pos, alpha=0.2, width=1.5, ax=ax)
            
            # Destaca arestas no caminho
            if len(result['path']) > 1:
                path_edges = [(result['path'][i], result['path'][i+1]) 
                             for i in range(len(result['path'])-1) 
                             if G.has_edge(result['path'][i], result['path'][i+1])]
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                                      edge_color='#e74c3c', width=3, 
                                      alpha=0.7, ax=ax)
            
            # Título com informações da busca
            status = "ENCONTRADO" if result['found'] else "NÃO ENCONTRADO"
            title = f"Grafo da Rede P2P - Busca: {result['resource']} - Status: {status}"
            
            # Legenda
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ecc71', 
                          markersize=12, label='Nó Origem'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
                          markersize=12, label='Nós Visitados'),
            ]
            
            if result['found']:
                legend_elements.append(
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', 
                              markersize=12, label='Recurso Encontrado')
                )
            
            legend_elements.append(
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#95a5a6', 
                          markersize=12, label='Nós Não Visitados')
            )
            
            ax.legend(handles=legend_elements, loc='upper left', fontsize=11, 
                     framealpha=0.9, edgecolor='black')
        else:
            # Sem resultado - visualização simples da rede
            node_colors = '#3498db'
            node_sizes = 500
            
            # Desenha arestas
            nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.5, ax=ax)
            
            title = f"Grafo da Rede P2P - {network.name}"
        
        # Desenha nós
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.9, 
                              edgecolors='black', linewidths=2, ax=ax)
        
        # Desenha labels
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', 
                               font_color='white', ax=ax)
        
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Salva ou exibe
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Grafo salvo em: {save_path}")
        else:
            plt.show()
        
        plt.close()
