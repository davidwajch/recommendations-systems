# Desenho Técnico da Arquitetura - Sistema de Recomendação Open Finance

## 🏗️ Visão Geral da Arquitetura

### Arquitetura em Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                    │
│  (APIs REST, Interface Web, Aplicativo Mobile)              │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  CAMADA DE APLICAÇÃO                         │
│  (Orquestração, Validação, Transformação de Dados)           │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│              CAMADA DE RECOMENDAÇÃO                          │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ User-Based CF   │  │ Content-Based   │                  │
│  │ (Implementado)  │  │ (Futuro)        │                  │
│  └─────────────────┘  └─────────────────┘                  │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ Hybrid Approach │  │ Deep Learning   │                  │
│  │ (Futuro)        │  │ (Futuro)        │                  │
│  └─────────────────┘  └─────────────────┘                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  CAMADA DE DADOS                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Open Finance │  │ Data Warehouse│  │ Cache Layer │      │
│  │ API Gateway  │  │ (Histórico)   │  │ (Redis)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Componentes Principais

### 1. Camada de Dados

#### 1.1 Open Finance API Gateway
- **Função**: Integração com APIs do Open Finance
- **Responsabilidades**:
  - Autenticação OAuth 2.0
  - Coleta de dados consensuais
  - Normalização de dados de diferentes IFs
  - Cache de respostas

#### 1.2 Data Warehouse
- **Função**: Armazenamento histórico de dados
- **Estrutura**:
  - Tabela de Clientes
  - Tabela de Produtos
  - Tabela de Interações (ratings/uso)
  - Tabela de Recomendações
  - Tabela de Feedback

#### 1.3 Cache Layer (Redis)
- **Função**: Otimização de performance
- **Uso**:
  - Cache de matrizes de similaridade
  - Cache de recomendações pré-calculadas
  - Cache de perfis de clientes

---

### 2. Camada de Recomendação

#### 2.1 User-Based Collaborative Filtering (Implementado)

**Justificativa da Escolha:**
- ✅ **Eficácia comprovada**: Técnica amplamente validada em sistemas de recomendação
- ✅ **Adequação ao contexto**: Ideal quando há sobreposição de produtos entre clientes
- ✅ **Simplicidade**: Fácil implementação e manutenção
- ✅ **Interpretabilidade**: Resultados fáceis de explicar para stakeholders
- ✅ **Baixo custo computacional**: Eficiente para provas de conceito

**Algoritmo:**
```
1. Construir Matriz de Utilidade (Clientes × Produtos)
2. Calcular Similaridade entre Clientes
   - Similaridade de Cosseno
   - Correlação de Pearson
3. Identificar K Clientes Mais Similares
4. Gerar Recomendações
   - Score = Σ(similaridade × rating) / Σ(similaridade)
   - Filtrar produtos já possuídos
   - Ordenar por score
```

**Fluxo de Processamento:**
```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Matriz de Utilidade │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Cálculo Similaridade│
│  (Cosseno/Pearson)  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ K Clientes Similares│
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Geração Recomendações│
│  (Score Ponderado)   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Top N Produtos     │
└─────────────────────┘
```

#### 2.2 Técnicas Futuras (Roadmap)

**Content-Based Filtering:**
- Recomendações baseadas em características dos produtos
- Útil para cold-start problem (clientes novos)

**Hybrid Approach:**
- Combinação de múltiplas técnicas
- Melhor precisão e cobertura

**Deep Learning:**
- Neural Collaborative Filtering
- Autoencoders para embeddings
- Maior capacidade de capturar padrões complexos

---

### 3. Camada de Aplicação

#### 3.1 API de Recomendação
- **Endpoint**: `GET /api/recommendations/{cliente_id}`
- **Parâmetros**:
  - `n`: Número de recomendações (padrão: 5)
  - `metodo`: 'cosseno' ou 'pearson' (padrão: 'cosseno')
- **Resposta**:
  ```json
  {
    "cliente": "Ana",
    "recomendacoes": [
      {"produto": "Conta Corrente", "score": 3.531},
      {"produto": "Cartão de Crédito", "score": 2.531}
    ],
    "clientes_similares": [
      {"cliente": "Pedro", "similaridade": 0.827}
    ]
  }
  ```

#### 3.2 Serviço de Processamento
- **Função**: Processamento assíncrono de recomendações
- **Tecnologias**: Celery, RabbitMQ
- **Tarefas**:
  - Atualização periódica de matrizes de similaridade
  - Pré-cálculo de recomendações para clientes ativos
  - Processamento de feedback

---

### 4. Camada de Apresentação

#### 4.1 Interface Web
- Dashboard de recomendações
- Visualização de similaridades
- Histórico de recomendações

#### 4.2 API REST
- Integração com sistemas externos
- Aplicativos mobile
- Webhooks para notificações

---

## 📊 Fluxo de Dados Completo

```
┌──────────────┐
│ Open Finance │
│   APIs       │
└──────┬───────┘
       │ Dados Consensuais
       ▼
┌──────────────┐
│  ETL Process │
│ Normalização │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Data Warehouse│
│  (Histórico)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Matriz     │
│  Utilidade   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Algoritmo   │
│ Recomendação │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Cache Layer │
│   (Redis)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   API REST   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Cliente/App │
└──────────────┘
```

---

## 🔐 Segurança e Privacidade

### Medidas Implementadas
- ✅ Autenticação OAuth 2.0 para acesso a dados
- ✅ Criptografia de dados em trânsito (HTTPS/TLS)
- ✅ Criptografia de dados em repouso
- ✅ Logs de auditoria
- ✅ Anonimização de dados sensíveis
- ✅ Conformidade com LGPD

---

## ⚡ Performance e Escalabilidade

### Otimizações
- **Cache**: Matrizes de similaridade em cache
- **Pré-cálculo**: Recomendações calculadas periodicamente
- **Paralelização**: Processamento distribuído
- **Indexação**: Índices otimizados no banco de dados

### Métricas de Performance
- Tempo de resposta: < 2 segundos
- Throughput: 1000 requisições/segundo
- Disponibilidade: 99.9%

---

## 🧪 Ambiente de Desenvolvimento

### Stack Tecnológico (POC)
- **Linguagem**: Python 3.8+
- **Bibliotecas**:
  - NumPy: Cálculos numéricos
  - Pandas: Manipulação de dados
  - (Futuro) Scikit-learn: Machine Learning
  - (Futuro) TensorFlow/PyTorch: Deep Learning

### Stack Tecnológico (Produção - Futuro)
- **Backend**: Python (FastAPI/Django)
- **Banco de Dados**: PostgreSQL, Redis
- **Processamento**: Celery, RabbitMQ
- **Deploy**: Docker, Kubernetes
- **Monitoramento**: Prometheus, Grafana

---

## 📈 Evolução da Arquitetura

### Fase 1: Prova de Conceito (Atual)
- ✅ User-Based Collaborative Filtering
- ✅ Dataset reduzido
- ✅ Cálculo de similaridade (Cosseno e Pearson)
- ✅ Geração de recomendações básicas

### Fase 2: MVP
- ⏳ Integração com Open Finance APIs
- ⏳ Interface web básica
- ⏳ Sistema de feedback
- ⏳ Métricas de avaliação

### Fase 3: Produção
- ⏳ Content-Based Filtering
- ⏳ Hybrid Approach
- ⏳ Escalabilidade horizontal
- ⏳ A/B Testing
- ⏳ Monitoramento avançado

### Fase 4: Avançado
- ⏳ Deep Learning
- ⏳ Real-time recommendations
- ⏳ Explicabilidade (XAI)
- ⏳ Personalização contextual

---

## 📝 Decisões de Arquitetura

### Por que User-Based CF?
1. **Simplicidade**: Fácil de implementar e entender
2. **Eficácia**: Comprovada em diversos domínios
3. **Adequação**: Ideal para o contexto de Open Finance
4. **Base sólida**: Permite evolução para técnicas mais complexas

### Por que duas métricas de similaridade?
- **Cosseno**: Melhor para dados esparsos, não considera magnitude
- **Pearson**: Melhor para capturar correlações lineares, robusto a diferenças de escala
- **Flexibilidade**: Permite escolher a melhor métrica por contexto

### Por que cache?
- **Performance**: Reduz tempo de resposta
- **Custo**: Reduz carga computacional
- **Escalabilidade**: Permite atender mais requisições

---

*Arquitetura técnica do Sistema de Recomendação - QuantumFinance*

