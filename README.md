# Simulador de Rede P2P - Algoritmos de Busca

Este projeto implementa um simulador de rede P2P (Peer-to-Peer) não estruturada com três diferentes algoritmos de busca por recursos.

## 📋 Descrição

O simulador permite criar uma rede P2P a partir de um arquivo de configuração JSON e realizar buscas por recursos utilizando diferentes estratégias:

1. **Busca por Inundação (Flooding)** - Propaga a consulta para todos os vizinhos
2. **Busca por Passeio Aleatório (Random Walk)** - Escolhe aleatoriamente o próximo nó
3. **Busca Informada (Informed Search)** - Utiliza heurísticas baseadas em histórico de sucesso

## 🏗️ Estrutura do Projeto

```
RedeP2P/
├── main.py                 # Programa principal com interface CLI
├── node.py                 # Classe Node - representa um nó da rede
├── p2p_network.py          # Classe P2PNetwork - gerencia a rede
├── search_algorithms.py    # Implementação dos algoritmos de busca
├── config.json             # Arquivo de configuração de exemplo
└── README.md               # Este arquivo
```

## 📦 Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (usa apenas bibliotecas padrão do Python)

## 🚀 Como Usar

### 1. Executar o programa

```bash
python main.py
```

Ou especifique um arquivo de configuração:

```bash
python main.py config.json
```

### 2. Formato do arquivo JSON

O arquivo de configuração deve ter a seguinte estrutura:

```json
{
  "network": {
    "name": "Nome da Rede",
    "description": "Descrição da rede"
  },
  "nodes": [
    {
      "id": "node1",
      "name": "Node 1",
      "resources": ["file1.txt", "video1.mp4"]
    }
  ],
  "connections": [
    {"from": "node1", "to": "node2"}
  ]
}
```

**Campos:**
- `network`: Informações gerais da rede (opcional)
- `nodes`: Lista de nós, cada um com:
  - `id`: Identificador único (obrigatório)
  - `name`: Nome do nó (obrigatório)
  - `resources`: Lista de recursos mantidos pelo nó (opcional)
- `connections`: Lista de conexões entre nós (bidirecionais)
  - `from`: ID do nó de origem
  - `to`: ID do nó de destino

### 3. Menu do Programa

O programa oferece as seguintes opções:

1. **Busca por Inundação** - Execute busca usando flooding
2. **Busca por Passeio Aleatório** - Execute busca usando random walk
3. **Busca Informada** - Execute busca usando heurísticas
4. **Comparar todos os algoritmos** - Compare os três algoritmos lado a lado
5. **Mostrar informações da rede** - Visualize a topologia completa
6. **Listar todos os recursos** - Veja todos os recursos disponíveis
0. **Sair** - Encerra o programa

## 🔍 Algoritmos de Busca

### 1. Busca por Inundação (Flooding)

**Como funciona:**
- A consulta é propagada para todos os vizinhos do nó de origem
- Cada nó que recebe a consulta verifica se possui o recurso
- Se não possui, propaga para seus vizinhos (exceto quem enviou)
- Continua até encontrar o recurso ou atingir o TTL (Time To Live)

**Parâmetros:**
- `ttl`: Profundidade máxima de busca (padrão: 10)

**Vantagens:**
- Alta probabilidade de encontrar o recurso se ele existir
- Simples de implementar

**Desvantagens:**
- Gera muito tráfego na rede (muitas mensagens)
- Pode sobrecarregar a rede em redes grandes

### 2. Busca por Passeio Aleatório (Random Walk)

**Como funciona:**
- Escolhe aleatoriamente um vizinho em cada passo
- Continua até encontrar o recurso ou atingir o número máximo de passos
- Pode visitar o mesmo nó múltiplas vezes

**Parâmetros:**
- `max_steps`: Número máximo de passos (padrão: 50)

**Vantagens:**
- Gera menos tráfego que flooding
- Baixo uso de recursos computacionais

**Desvantagens:**
- Menor probabilidade de encontrar o recurso
- Pode levar mais tempo para encontrar
- Comportamento não determinístico

### 3. Busca Informada (Informed Search)

**Como funciona:**
- Utiliza heurísticas baseadas no histórico de sucesso dos vizinhos
- Prioriza vizinhos que tiveram mais sucessos em buscas anteriores
- Aprende com buscas passadas para melhorar o desempenho

**Parâmetros:**
- `max_nodes`: Número máximo de nós a visitar (padrão: 20)

**Vantagens:**
- Mais eficiente que random walk após aprendizado
- Balanceia tráfego e taxa de sucesso
- Melhora com o uso

**Desvantagens:**
- Depende de histórico para ser eficiente
- Pode ter viés baseado em buscas anteriores

## 📊 Exemplo de Uso

```
BEM-VINDO AO SIMULADOR DE REDE P2P

Digite o caminho do arquivo de configuração JSON (padrão: config.json): 

Carregando rede a partir de: config.json
✓ Rede carregada com sucesso!

SIMULADOR DE REDE P2P - ALGORITMOS DE BUSCA

Opções:
  1 - Busca por Inundação (Flooding)
  2 - Busca por Passeio Aleatório (Random Walk)
  3 - Busca Informada (Informed Search)
  4 - Comparar todos os algoritmos
  5 - Mostrar informações da rede
  6 - Listar todos os recursos disponíveis
  0 - Sair

Escolha uma opção: 1

Nós disponíveis: node1, node2, node3, node4, node5, node6, node7, node8
Digite o ID do nó de origem: node1
Digite o nome do recurso a buscar: video3.mp4

============================================================
Algoritmo: Busca por Inundação (Flooding)
============================================================
Recurso procurado: video3.mp4
Nó de origem: node1

✓ RECURSO ENCONTRADO!
  Encontrado em: node7
  Caminho percorrido: node1 -> node2 -> node4 -> node7
  Número de saltos: 3
  Total de nós visitados: 7
  Mensagens enviadas: 11
============================================================
```

## 📈 Métricas Coletadas

Para cada busca, o simulador coleta:

- **Status**: Recurso encontrado ou não
- **Nó onde foi encontrado**: ID do nó que possui o recurso
- **Caminho percorrido**: Sequência de nós visitados
- **Número de saltos**: Distância até o recurso
- **Total de nós visitados**: Quantidade de nós únicos explorados
- **Mensagens enviadas**: Número de mensagens de consulta enviadas

## 🎯 Casos de Uso

1. **Estudo de algoritmos de busca distribuída**
2. **Análise de desempenho de redes P2P**
3. **Comparação de estratégias de busca**
4. **Simulação de redes de compartilhamento de arquivos**
5. **Pesquisa em sistemas distribuídos**

## 🛠️ Personalização

### Modificar parâmetros dos algoritmos

Edite `main.py` e ajuste os valores padrão nas chamadas:

```python
# Flooding com TTL maior
result = SearchAlgorithms.flooding_search(network, origin_id, resource_name, ttl=15)

# Random Walk com mais passos
result = SearchAlgorithms.random_walk_search(network, origin_id, resource_name, max_steps=100)

# Informed Search visitando mais nós
result = SearchAlgorithms.informed_search(network, origin_id, resource_name, max_nodes=30)
```

### Criar sua própria topologia

Modifique ou crie um novo arquivo JSON seguindo o formato especificado.

## 📝 Licença

Este projeto é de código aberto e está disponível para uso educacional.

## 👥 Contribuições

Sugestões e melhorias são bem-vindas!

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.
