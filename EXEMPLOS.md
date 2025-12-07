# Exemplos de Uso - Simulador P2P

## 1. Executar uma busca simples

```bash
python main.py config-menor.json
```

No menu, escolha a opção 1, 2 ou 3 e forneça:
- Nó de origem: `node1`
- Recurso: `video3.mp4`

## 2. Comparar algoritmos com texto

```bash
python main.py config-menor.json
```

Escolha a opção 4 para ver uma comparação textual dos três algoritmos.

## 3. Gerar gráfico de comparação

```bash
python main.py config-menor.json
```

Escolha a opção 5 para gerar:
- Gráfico de barras comparativo com 4 métricas
- Tabela comparativa textual

O gráfico é salvo na pasta `graphs/` com timestamp único.

## 4. Executar testes automatizados

```bash
python test_simulator.py
```

Este script executa:
- Testes de busca básica
- Validações de rede
- Geração de todas as visualizações

Os gráficos de teste são salvos em `test_graphs/`.

## 5. Visualizar informações da rede

```bash
python main.py config.json
```

Escolha a opção 6 para ver:
- Nome e descrição da rede
- Total de nós
- Lista de nós com seus recursos e vizinhos

## 6. Listar todos os recursos

```bash
python main.py config.json
```

Escolha a opção 7 para ver uma lista completa de:
- Todos os recursos disponíveis na rede
- Em quais nós cada recurso está localizado

## Exemplo de Saída - Comparação com Gráfico

```
COMPARAÇÃO COM GRÁFICOS
============================================================
Origem: node1
Recurso: video3.mp4
============================================================

Executando buscas...

TABELA COMPARATIVA DE RESULTADOS
================================================================================
Algoritmo                 Sucesso    Nós        Mensagens    Saltos    
--------------------------------------------------------------------------------
Inundação                 ✓ Sim      7          15           3         
Passeio Aleatório         ✓ Sim      5          5            4         
Busca Informada           ✓ Sim      6          10           3         
================================================================================

Gerando gráfico de barras comparativo...
✓ Gráfico salvo em: graphs/comparison_20231207_143025.png

============================================================
✓ Gráfico gerado com sucesso!
  Verifique o arquivo: graphs/comparison_20231207_143025.png
============================================================
```

## Interpretação dos Gráficos

### Gráfico de Barras - Nós Visitados
- **Menor é melhor**: Indica eficiência na exploração da rede
- Inundação geralmente visita mais nós (busca exaustiva)
- Passeio Aleatório pode visitar menos nós mas com menor garantia de sucesso

### Gráfico de Barras - Mensagens Enviadas
- **Menor é melhor**: Indica menor overhead de comunicação
- Importante para avaliar o custo de rede do algoritmo
- Busca Informada tende a ser mais eficiente após aprendizado

### Gráfico de Barras - Taxa de Sucesso
- **Maior é melhor**: 100% indica que o recurso foi encontrado
- Inundação tem alta taxa de sucesso (explora exaustivamente)
- Passeio Aleatório pode falhar se o recurso estiver distante

### Gráfico de Barras - Número de Saltos
- **Menor é melhor**: Indica menor distância até o recurso
- Relevante apenas quando o recurso foi encontrado
- Mostra eficiência do caminho escolhido



## Dicas para Análise

1. **Compare com diferentes topologias**: Teste com redes pequenas e grandes
2. **Varie o recurso procurado**: Recursos próximos vs. distantes do nó origem
3. **Execute múltiplas vezes**: Especialmente para Passeio Aleatório (estocástico)
4. **Ajuste parâmetros**: TTL, max_steps, max_nodes para ver o impacto
5. **Observe padrões**: Como a estrutura da rede afeta cada algoritmo
