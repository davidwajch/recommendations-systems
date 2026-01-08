"""
Sistema de Recomendação para Open Finance - QuantumFinance
Técnica: Filtragem Colaborativa Baseada em Usuários (User-Based Collaborative Filtering)

Este sistema analisa o histórico de produtos financeiros utilizados pelos clientes
e recomenda novos produtos baseado em padrões de comportamento de clientes similares.
"""

import numpy as np
from collections import defaultdict
from typing import Dict, List, Tuple
import pandas as pd

# Dataset de Open Finance
clientes = {
    'Ana': {
        'Cartão de Crédito': 1,
        'Conta Corrente': 2,
        'Poupança': 3,
        'Renda Fixa': 4,
        'Crédito Pessoal': 5
    },
    'Marcos': {
        'Cartão de Crédito': 2,
        'Conta Corrente': 3,
        'Poupança': 4,
        'Renda Fixa': 5,
        'Renda Variável': 0.6
    },
    'Pedro': {
        'Cartão de Crédito': 3,
        'Conta Corrente': 4,
        'Poupança': 5,
        'Crédito Pessoal': 7
    },
    'Claudia': {
        'Cartão de Crédito': 4,
        'Conta Corrente': 5,
        'Poupança': 6
    }
}


class SistemaRecomendacaoOpenFinance:
    """
    Sistema de Recomendação usando Filtragem Colaborativa Baseada em Usuários.
    
    A técnica escolhida é adequada porque:
    1. Identifica padrões de comportamento entre clientes similares
    2. Recomenda produtos que clientes com perfil similar já utilizam
    3. É eficaz quando há sobreposição de produtos entre usuários
    """
    
    def __init__(self, dados_clientes: Dict):
        """
        Inicializa o sistema com os dados dos clientes.
        
        Args:
            dados_clientes: Dicionário com clientes e seus produtos/ratings
        """
        self.dados_clientes = dados_clientes
        self.matriz_utilidade = self._criar_matriz_utilidade()
        self.similaridades = {}
        
    def _criar_matriz_utilidade(self) -> pd.DataFrame:
        """
        Cria uma matriz de utilidade (clientes x produtos).
        
        Returns:
            DataFrame com clientes nas linhas e produtos nas colunas
        """
        # Coletar todos os produtos únicos
        todos_produtos = set()
        for produtos in self.dados_clientes.values():
            todos_produtos.update(produtos.keys())
        todos_produtos = sorted(list(todos_produtos))
        
        # Criar matriz
        matriz = {}
        for cliente, produtos in self.dados_clientes.items():
            linha = {}
            for produto in todos_produtos:
                linha[produto] = produtos.get(produto, 0)
            matriz[cliente] = linha
        
        return pd.DataFrame(matriz).T
    
    def calcular_similaridade_cosseno(self, cliente1: str, cliente2: str) -> float:
        """
        Calcula a similaridade de cosseno entre dois clientes.
        
        Similaridade de cosseno mede o ângulo entre dois vetores,
        sendo ideal para comparar perfis de clientes.
        
        Args:
            cliente1: Nome do primeiro cliente
            cliente2: Nome do segundo cliente
            
        Returns:
            Valor de similaridade entre 0 e 1
        """
        vetor1 = self.matriz_utilidade.loc[cliente1].values
        vetor2 = self.matriz_utilidade.loc[cliente2].values
        
        # Calcular produto escalar
        produto_escalar = np.dot(vetor1, vetor2)
        
        # Calcular normas
        norma1 = np.linalg.norm(vetor1)
        norma2 = np.linalg.norm(vetor2)
        
        if norma1 == 0 or norma2 == 0:
            return 0.0
        
        return produto_escalar / (norma1 * norma2)
    
    def calcular_similaridade_pearson(self, cliente1: str, cliente2: str) -> float:
        """
        Calcula a correlação de Pearson entre dois clientes.
        
        A correlação de Pearson é robusta a diferenças de escala
        e mede a relação linear entre os perfis dos clientes.
        
        Args:
            cliente1: Nome do primeiro cliente
            cliente2: Nome do segundo cliente
            
        Returns:
            Valor de correlação entre -1 e 1
        """
        vetor1 = self.matriz_utilidade.loc[cliente1].values
        vetor2 = self.matriz_utilidade.loc[cliente2].values
        
        # Calcular médias
        media1 = np.mean(vetor1)
        media2 = np.mean(vetor2)
        
        # Calcular correlação
        numerador = np.sum((vetor1 - media1) * (vetor2 - media2))
        denominador1 = np.sqrt(np.sum((vetor1 - media1) ** 2))
        denominador2 = np.sqrt(np.sum((vetor2 - media2) ** 2))
        
        if denominador1 == 0 or denominador2 == 0:
            return 0.0
        
        return numerador / (denominador1 * denominador2)
    
    def encontrar_clientes_similares(self, cliente: str, n: int = 2, 
                                     metodo: str = 'cosseno') -> List[Tuple[str, float]]:
        """
        Encontra os N clientes mais similares a um cliente dado.
        
        Args:
            cliente: Nome do cliente
            n: Número de clientes similares a retornar
            metodo: 'cosseno' ou 'pearson'
            
        Returns:
            Lista de tuplas (cliente_similar, similaridade) ordenada por similaridade
        """
        similaridades = []
        
        for outro_cliente in self.dados_clientes.keys():
            if outro_cliente != cliente:
                if metodo == 'cosseno':
                    sim = self.calcular_similaridade_cosseno(cliente, outro_cliente)
                else:
                    sim = self.calcular_similaridade_pearson(cliente, outro_cliente)
                
                similaridades.append((outro_cliente, sim))
        
        # Ordenar por similaridade (maior primeiro)
        similaridades.sort(key=lambda x: x[1], reverse=True)
        
        return similaridades[:n]
    
    def gerar_recomendacoes(self, cliente: str, n: int = 3, 
                           metodo: str = 'cosseno') -> List[Tuple[str, float]]:
        """
        Gera recomendações de produtos para um cliente.
        
        A recomendação é baseada em produtos que clientes similares utilizam,
        mas que o cliente ainda não possui ou tem baixa interação.
        
        Args:
            cliente: Nome do cliente
            n: Número de recomendações a retornar
            metodo: 'cosseno' ou 'pearson'
            
        Returns:
            Lista de tuplas (produto, score) ordenada por score
        """
        # Encontrar clientes similares
        clientes_similares = self.encontrar_clientes_similares(cliente, n=2, metodo=metodo)
        
        # Produtos do cliente atual
        produtos_cliente = set(self.dados_clientes[cliente].keys())
        
        # Calcular scores de recomendação
        scores = defaultdict(float)
        soma_similaridades = defaultdict(float)
        
        for cliente_similar, similaridade in clientes_similares:
            if similaridade > 0:  # Apenas clientes com similaridade positiva
                produtos_similar = self.dados_clientes[cliente_similar]
                
                for produto, rating in produtos_similar.items():
                    # Se o cliente não tem o produto ou tem rating baixo
                    if produto not in produtos_cliente or self.dados_clientes[cliente].get(produto, 0) < 3:
                        # Score ponderado pela similaridade
                        scores[produto] += similaridade * rating
                        soma_similaridades[produto] += abs(similaridade)
        
        # Normalizar scores
        scores_normalizados = {}
        for produto, score in scores.items():
            if soma_similaridades[produto] > 0:
                scores_normalizados[produto] = score / soma_similaridades[produto]
            else:
                scores_normalizados[produto] = score
        
        # Ordenar por score
        recomendacoes = sorted(scores_normalizados.items(), key=lambda x: x[1], reverse=True)
        
        return recomendacoes[:n]
    
    def exibir_matriz_utilidade(self):
        """Exibe a matriz de utilidade formatada."""
        print("\n" + "="*80)
        print("MATRIZ DE UTILIDADE (Clientes x Produtos)")
        print("="*80)
        print(self.matriz_utilidade)
        print()
    
    def exibir_similaridades(self, metodo: str = 'cosseno'):
        """Exibe a matriz de similaridades entre todos os clientes."""
        print("\n" + "="*80)
        print(f"MATRIZ DE SIMILARIDADES ({metodo.upper()})")
        print("="*80)
        
        clientes_lista = list(self.dados_clientes.keys())
        n = len(clientes_lista)
        
        # Criar matriz de similaridades
        matriz_sim = np.zeros((n, n))
        for i, cliente1 in enumerate(clientes_lista):
            for j, cliente2 in enumerate(clientes_lista):
                if metodo == 'cosseno':
                    matriz_sim[i][j] = self.calcular_similaridade_cosseno(cliente1, cliente2)
                else:
                    matriz_sim[i][j] = self.calcular_similaridade_pearson(cliente1, cliente2)
        
        # Exibir como DataFrame
        df_sim = pd.DataFrame(matriz_sim, index=clientes_lista, columns=clientes_lista)
        print(df_sim.round(3))
        print()
    
    def exibir_recomendacoes_completas(self, metodo: str = 'cosseno'):
        """Exibe recomendações para todos os clientes."""
        print("\n" + "="*80)
        print(f"RECOMENDAÇÕES DE PRODUTOS FINANCEIROS ({metodo.upper()})")
        print("="*80)
        
        for cliente in self.dados_clientes.keys():
            print(f"\n📊 Cliente: {cliente}")
            print("-" * 60)
            
            # Produtos atuais
            produtos_atuais = self.dados_clientes[cliente]
            print("Produtos atuais:")
            for produto, rating in sorted(produtos_atuais.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {produto}: {rating}")
            
            # Clientes similares
            similares = self.encontrar_clientes_similares(cliente, n=2, metodo=metodo)
            print(f"\nClientes similares:")
            for cliente_sim, sim_score in similares:
                print(f"  • {cliente_sim}: {sim_score:.3f}")
            
            # Recomendações
            recomendacoes = self.gerar_recomendacoes(cliente, n=3, metodo=metodo)
            if recomendacoes:
                print(f"\n💡 Recomendações:")
                for i, (produto, score) in enumerate(recomendacoes, 1):
                    print(f"  {i}. {produto} (score: {score:.3f})")
            else:
                print("\n  Nenhuma recomendação disponível no momento.")
            
            print()


def main():
    """
    Função principal que demonstra o uso do sistema de recomendação.
    """
    print("="*80)
    print("SISTEMA DE RECOMENDAÇÃO - OPEN FINANCE - QUANTUMFINANCE")
    print("="*80)
    print("\nTécnica: Filtragem Colaborativa Baseada em Usuários")
    print("Dataset: Clientes e produtos financeiros via Open Finance")
    print()
    
    # Inicializar sistema
    sistema = SistemaRecomendacaoOpenFinance(clientes)
    
    # Exibir matriz de utilidade
    sistema.exibir_matriz_utilidade()
    
    # Exibir similaridades (cosseno)
    sistema.exibir_similaridades(metodo='cosseno')
    
    # Exibir recomendações usando similaridade de cosseno
    sistema.exibir_recomendacoes_completas(metodo='cosseno')
    
    # Exibir similaridades (pearson)
    sistema.exibir_similaridades(metodo='pearson')
    
    # Exibir recomendações usando correlação de Pearson
    sistema.exibir_recomendacoes_completas(metodo='pearson')
    
    # Exemplo de uso programático
    print("\n" + "="*80)
    print("EXEMPLO DE USO PROGRAMÁTICO")
    print("="*80)
    
    cliente_exemplo = 'Ana'
    print(f"\nRecomendações para {cliente_exemplo}:")
    recomendacoes = sistema.gerar_recomendacoes(cliente_exemplo, n=3)
    for produto, score in recomendacoes:
        print(f"  • {produto}: {score:.3f}")
    
    print("\n" + "="*80)
    print("Análise concluída!")
    print("="*80)


if __name__ == "__main__":
    main()

