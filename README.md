# Sistema de Recomendação - Open Finance

Sistema de recomendação de produtos financeiros usando filtragem colaborativa baseada em usuários. Implementado como prova de conceito para análise de dados do Open Finance.

## O que é

Este projeto implementa um sistema de recomendação que analisa o histórico de produtos financeiros utilizados por clientes e sugere novos produtos com base em padrões de comportamento de usuários similares.

**Contexto**: A QuantumFinance é uma fintech que utiliza dados consensuais do Open Finance para entender o perfil financeiro completo de seus clientes. O sistema identifica oportunidades de cross-sell e personaliza ofertas de produtos.

## Abordagem

### Algoritmo

Filtragem colaborativa baseada em usuários (User-Based Collaborative Filtering):

1. Cria matriz de utilidade (clientes × produtos)
2. Calcula similaridade entre usuários usando:
   - **Similaridade de cosseno**: mede o ângulo entre vetores de produtos, ideal para dados esparsos
   - **Correlação de Pearson**: mede relação linear entre perfis, robusta a diferenças de escala
3. Identifica os N usuários mais similares ao cliente alvo
4. Recomenda produtos que usuários similares possuem, ponderando por score de similaridade
5. Filtra produtos que o cliente já possui ou tem alta interação

### Por que esta abordagem

- Não exige features dos produtos (item-cold-start)
- Funciona bem com dados esparsos
- Implementação direta e interpretável
- Adequada para PoC com poucos dados

### Limitações conhecidas

- User cold-start: clientes novos sem histórico não recebem recomendações relevantes
- Escalabilidade: calcular similaridades entre todos os pares de usuários não escala para bases grandes
- Bolha de filtro: tende a recomendar apenas o que usuários similares já conhecem

## Stack

- Python 3.8+
- NumPy: operações vetoriais e cálculo de similaridades
- Pandas: manipulação da matriz de utilidade
- Matplotlib: geração de visualizações (heatmaps, gráficos de barras)

## Como rodar

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Executar análise completa

```bash
python analise.py
```

Exibe no terminal:
- Matriz de utilidade (clientes × produtos)
- Matrizes de similaridade (cosseno e Pearson)
- Recomendações para todos os clientes usando ambos os métodos

### Demonstrar cenários de uso

```bash
python demonstracao_cenarios.py
```

Simula 4 cenários fictícios (Ana, Marcos, Pedro, Claudia) e compara os métodos de similaridade.

### Gerar visualizações

```bash
python interface_grafica.py
```

Gera arquivos PNG:
- `matriz_utilidade.png`: heatmap da matriz de utilidade
- `similaridades_cosseno.png`, `similaridades_pearson.png`: matrizes de similaridade
- `recomendacoes_*.png`: gráficos de recomendação por cliente
- `comparacao_metodos_ana.png`: comparação dos dois métodos
- `dashboard_completo.png`: visão consolidada

## Estrutura do projeto

```
.
├── analise.py                         # Implementação do sistema de recomendação
├── demonstracao_cenarios.py           # Cenários de uso simulados
├── interface_grafica.py               # Geração de visualizações
├── requirements.txt                   # Dependências
├── 01_Contexto_Fintech_Objetivo.md    # Contexto de negócio e objetivos
├── 02_Arquitetura_Tecnica.md          # Detalhes da arquitetura
├── 03_Cenarios_Uso.md                 # Descrição dos cenários
└── 00_Verificacao_Entregaveis.md      # Checklist de entregáveis
```

## Dataset

Dataset sintético com 4 clientes e 6 produtos financeiros:

| Cliente | Produtos |
|---------|----------|
| Ana | Cartão de Crédito (1), Conta Corrente (2), Poupança (3), Renda Fixa (4), Crédito Pessoal (5) |
| Marcos | Cartão de Crédito (2), Conta Corrente (3), Poupança (4), Renda Fixa (5), Renda Variável (0.6) |
| Pedro | Cartão de Crédito (3), Conta Corrente (4), Poupança (5), Crédito Pessoal (7) |
| Claudia | Cartão de Crédito (4), Conta Corrente (5), Poupança (6) |

Os valores representam nível de interação ou rating do cliente com cada produto.

## Uso programático

```python
from analise import SistemaRecomendacaoOpenFinance, clientes

sistema = SistemaRecomendacaoOpenFinance(clientes)

# Gerar recomendações para um cliente
recomendacoes = sistema.gerar_recomendacoes('Ana', n=3, metodo='cosseno')
for produto, score in recomendacoes:
    print(f"{produto}: {score:.3f}")

# Encontrar clientes similares
similares = sistema.encontrar_clientes_similares('Ana', n=2, metodo='cosseno')
for cliente, score in similares:
    print(f"{cliente}: {score:.3f}")
```

## Próximos passos

- Integrar com APIs reais do Open Finance (OAuth 2.0, endpoints de consentimento e dados)
- Implementar content-based filtering para mitigar cold-start
- Testar abordagem híbrida (colaborativa + conteúdo)
- Criar API REST para servir recomendações
- Adicionar pipeline de feedback para aprendizado contínuo
- Implementar testes automatizados e métricas offline (precision@k, recall@k, NDCG)

## Referências

- [Open Finance Brasil - Documentação](https://openfinancebrasil.atlassian.net/wiki/spaces/OF/overview)
- [Open Finance - Diretório de participantes](https://data.directory.openbankingbrasil.org.br/participants)
- Ricci, F., Rokach, L., & Shapira, B. (2015). Recommender Systems Handbook

## Licença

Projeto desenvolvido para fins de estudo e demonstração.
