# Sistema de Recomendação - Open Finance - QuantumFinance

## 📋 Visão Geral

Este projeto implementa um **Sistema de Recomendação (SR)** para a fintech QuantumFinance, utilizando dados do Open Finance para sugerir produtos e serviços financeiros relevantes aos clientes.

### Técnica Implementada
- **Filtragem Colaborativa Baseada em Usuários (User-Based Collaborative Filtering)**
- Similaridade de Cosseno
- Correlação de Pearson

---

## 📁 Estrutura do Projeto

```
recommendations systems/
│
├── analise.py                    # Código principal do sistema de recomendação
├── demonstracao_cenarios.py      # Script de demonstração de cenários de uso
├── interface_grafica.py          # Interface gráfica para visualizações
├── requirements.txt              # Dependências do projeto
│
├── 01_Contexto_Fintech_Objetivo.md    # Entregável 1: Contexto e objetivo
├── 02_Arquitetura_Tecnica.md          # Entregável 2: Arquitetura técnica
├── 03_Cenarios_Uso.md                 # Entregável 3: Cenários de uso
│
└── README.md                     # Este arquivo
```

---

## 🚀 Como Usar

### 1. Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar Análise Principal

```bash
python analise.py
```

Este script executa:
- Criação da matriz de utilidade
- Cálculo de similaridades (Cosseno e Pearson)
- Geração de recomendações para todos os clientes
- Exibição de resultados formatados

### 3. Executar Demonstração de Cenários

```bash
python demonstracao_cenarios.py
```

Este script demonstra:
- 4 cenários fictícios de uso
- Comparação de métodos de similaridade
- Fluxo completo de recomendação

### 4. Gerar Visualizações Gráficas

```bash
python interface_grafica.py
```

Este script gera:
- Matriz de utilidade (heatmap)
- Matrizes de similaridade
- Gráficos de recomendações por cliente
- Comparação de métodos
- Dashboard completo

**Arquivos gerados:**
- `matriz_utilidade.png`
- `similaridades_cosseno.png`
- `similaridades_pearson.png`
- `recomendacoes_[cliente].png` (para cada cliente)
- `comparacao_metodos_ana.png`
- `dashboard_completo.png`

---

## 📊 Dataset

O dataset utilizado contém dados de 4 clientes e seus produtos financeiros:

- **Ana**: Cartão de Crédito, Conta Corrente, Poupança, Renda Fixa, Crédito Pessoal
- **Marcos**: Cartão de Crédito, Conta Corrente, Poupança, Renda Fixa, Renda Variável
- **Pedro**: Cartão de Crédito, Conta Corrente, Poupança, Crédito Pessoal
- **Claudia**: Cartão de Crédito, Conta Corrente, Poupança

Os valores numéricos representam o nível de interação/uso de cada produto.

---

## 🎯 Entregáveis

### ✅ Entregável 1: Contexto da Fintech e Objetivo
**Arquivo**: `01_Contexto_Fintech_Objetivo.md`

- Contexto da QuantumFinance
- Oportunidades do Open Finance
- Objetivos do Sistema de Recomendação
- Valor de negócio
- Métricas de sucesso

### ✅ Entregável 2: Arquitetura Técnica
**Arquivo**: `02_Arquitetura_Tecnica.md`

- Visão geral da arquitetura
- Componentes principais
- Justificativa da técnica escolhida
- Fluxo de dados
- Segurança e privacidade
- Performance e escalabilidade
- Evolução da arquitetura

### ✅ Entregável 3: Protótipo Operacional
**Arquivos**: 
- `03_Cenarios_Uso.md` - Documentação de cenários
- `demonstracao_cenarios.py` - Script de demonstração
- `interface_grafica.py` - Interface gráfica

- 4 cenários fictícios detalhados
- Fluxo de interação completo
- Interface gráfica com visualizações
- Demonstração prática do sistema

### ✅ Entregável 4: Código-Fonte
**Arquivo**: `analise.py`

- Implementação completa do sistema de recomendação
- Classe `SistemaRecomendacaoOpenFinance`
- Métodos de similaridade (Cosseno e Pearson)
- Geração de recomendações
- Visualizações e relatórios

---

## 🔧 Funcionalidades

### Sistema de Recomendação

#### Métodos de Similaridade
1. **Similaridade de Cosseno**
   - Mede o ângulo entre vetores de produtos
   - Ideal para dados esparsos
   - Range: 0 a 1

2. **Correlação de Pearson**
   - Mede relação linear entre perfis
   - Robusta a diferenças de escala
   - Range: -1 a 1

#### Geração de Recomendações
- Identifica clientes similares
- Calcula scores ponderados por similaridade
- Filtra produtos já possuídos
- Ordena por relevância

---

## 📈 Exemplo de Uso Programático

```python
from analise import SistemaRecomendacaoOpenFinance, clientes

# Inicializar sistema
sistema = SistemaRecomendacaoOpenFinance(clientes)

# Obter recomendações para um cliente
recomendacoes = sistema.gerar_recomendacoes('Ana', n=3)

# Exibir resultados
for produto, score in recomendacoes:
    print(f"{produto}: {score:.3f}")

# Encontrar clientes similares
similares = sistema.encontrar_clientes_similares('Ana', n=2)
for cliente, similaridade in similares:
    print(f"{cliente}: {similaridade:.3f}")
```

---

## 📊 Resultados Esperados

### Exemplo de Saída

```
📊 Cliente: Ana
------------------------------------------------------------
Produtos atuais:
  • Crédito Pessoal: 5
  • Renda Fixa: 4
  • Poupança: 3
  • Conta Corrente: 2
  • Cartão de Crédito: 1

Clientes similares:
  • Pedro: 0.827
  • Marcos: 0.732

💡 Recomendações:
  1. Conta Corrente (score: 3.531)
  2. Cartão de Crédito (score: 2.531)
  3. Renda Variável (score: 0.600)
```

---

## 🎓 Justificativa da Técnica

### Por que User-Based Collaborative Filtering?

1. **Eficácia Comprovada**: Técnica amplamente validada em sistemas de recomendação
2. **Adequação ao Contexto**: Ideal quando há sobreposição de produtos entre clientes
3. **Simplicidade**: Fácil implementação e manutenção
4. **Interpretabilidade**: Resultados fáceis de explicar para stakeholders
5. **Baixo Custo Computacional**: Eficiente para provas de conceito

### Vantagens
- ✅ Não requer características dos produtos
- ✅ Captura padrões de comportamento implícitos
- ✅ Funciona bem com dados esparsos
- ✅ Base sólida para evolução

### Limitações e Melhorias Futuras
- ⚠️ Cold-start problem (clientes novos)
- ⚠️ Escalabilidade com muitos clientes
- 🔄 **Futuro**: Content-Based Filtering
- 🔄 **Futuro**: Hybrid Approach
- 🔄 **Futuro**: Deep Learning

---

## 🔐 Segurança e Privacidade

- Dados consensuais do Open Finance
- Conformidade com LGPD
- Anonimização de dados sensíveis
- Logs de auditoria

---

## 📝 Dependências

- **Python**: 3.8+
- **NumPy**: Cálculos numéricos
- **Pandas**: Manipulação de dados
- **Matplotlib**: Visualizações gráficas

---

## 🚧 Próximos Passos

1. **Integração com Open Finance APIs**
   - Autenticação OAuth 2.0
   - Coleta de dados em tempo real

2. **Melhorias no Algoritmo**
   - Content-Based Filtering
   - Hybrid Approach
   - Deep Learning

3. **Interface de Produção**
   - API REST
   - Dashboard web
   - Integração com CRM

4. **Monitoramento**
   - Métricas de performance
   - A/B Testing
   - Feedback loop

---

## 📚 Referências

- [Open Finance Brasil - Documentação](https://openfinancebrasil.atlassian.net/wiki/spaces/OF/overview)
- [Open Finance - Diretório de URLs](https://data.directory.openbankingbrasil.org.br/participants)
- Ricci, F., Rokach, L., & Shapira, B. (2015). Recommender Systems Handbook

---

## 👥 Autores

Projeto desenvolvido para o Case Open Finance - QuantumFinance

---

## 📄 Licença

Este projeto é uma prova de conceito desenvolvida para fins acadêmicos.

---

*Sistema de Recomendação - Open Finance - QuantumFinance*

