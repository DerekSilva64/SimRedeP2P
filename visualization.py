import matplotlib.pyplot as plt


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
