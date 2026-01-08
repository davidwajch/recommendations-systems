"""
Interface Gráfica para Visualização de Recomendações
Sistema de Recomendação - Open Finance - QuantumFinance
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from analise import SistemaRecomendacaoOpenFinance, clientes
import numpy as np

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

def visualizar_matriz_utilidade(sistema):
    """Visualiza a matriz de utilidade como heatmap."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    matriz = sistema.matriz_utilidade
    im = ax.imshow(matriz.values, cmap='YlOrRd', aspect='auto')
    
    # Configurar eixos
    ax.set_xticks(np.arange(len(matriz.columns)))
    ax.set_yticks(np.arange(len(matriz.index)))
    ax.set_xticklabels(matriz.columns, rotation=45, ha='right')
    ax.set_yticklabels(matriz.index)
    
    # Adicionar valores nas células
    for i in range(len(matriz.index)):
        for j in range(len(matriz.columns)):
            valor = matriz.iloc[i, j]
            if valor > 0:
                text = ax.text(j, i, f'{valor:.1f}',
                             ha="center", va="center", color="black", fontweight='bold')
    
    ax.set_title('Matriz de Utilidade - Clientes x Produtos Financeiros', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Produtos Financeiros', fontsize=12)
    ax.set_ylabel('Clientes', fontsize=12)
    
    # Adicionar colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Nível de Interação', rotation=270, labelpad=20)
    
    plt.tight_layout()
    plt.savefig('matriz_utilidade.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfico salvo: matriz_utilidade.png")
    plt.close()


def visualizar_similaridades(sistema, metodo='cosseno'):
    """Visualiza a matriz de similaridades como heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    clientes_lista = list(clientes.keys())
    n = len(clientes_lista)
    
    # Criar matriz de similaridades
    matriz_sim = np.zeros((n, n))
    for i, cliente1 in enumerate(clientes_lista):
        for j, cliente2 in enumerate(clientes_lista):
            if metodo == 'cosseno':
                matriz_sim[i][j] = sistema.calcular_similaridade_cosseno(cliente1, cliente2)
            else:
                matriz_sim[i][j] = sistema.calcular_similaridade_pearson(cliente1, cliente2)
    
    im = ax.imshow(matriz_sim, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
    
    # Configurar eixos
    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels(clientes_lista)
    ax.set_yticklabels(clientes_lista)
    
    # Adicionar valores nas células
    for i in range(n):
        for j in range(n):
            valor = matriz_sim[i, j]
            text = ax.text(j, i, f'{valor:.3f}',
                         ha="center", va="center", color="black", fontweight='bold')
    
    metodo_nome = 'Cosseno' if metodo == 'cosseno' else 'Pearson'
    ax.set_title(f'Matriz de Similaridades ({metodo_nome})', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Clientes', fontsize=12)
    ax.set_ylabel('Clientes', fontsize=12)
    
    # Adicionar colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Similaridade', rotation=270, labelpad=20)
    
    plt.tight_layout()
    nome_arquivo = f'similaridades_{metodo}.png'
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {nome_arquivo}")
    plt.close()


def visualizar_recomendacoes_cliente(sistema, cliente, metodo='cosseno'):
    """Visualiza recomendações para um cliente específico."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Produtos Atuais vs Recomendações
    produtos_atuais = clientes[cliente]
    recomendacoes = sistema.gerar_recomendacoes(cliente, n=5, metodo=metodo)
    
    # Preparar dados
    produtos = list(produtos_atuais.keys())
    ratings = list(produtos_atuais.values())
    cores_atuais = ['#2ecc71'] * len(produtos)
    
    # Adicionar recomendações
    produtos_rec = [r[0] for r in recomendacoes]
    scores_rec = [r[1] for r in recomendacoes]
    cores_rec = ['#e74c3c'] * len(produtos_rec)
    
    # Gráfico de barras
    x_pos_atuais = np.arange(len(produtos))
    x_pos_rec = np.arange(len(produtos), len(produtos) + len(produtos_rec))
    
    ax1.bar(x_pos_atuais, ratings, color=cores_atuais, alpha=0.7, label='Produtos Atuais')
    ax1.bar(x_pos_rec, scores_rec, color=cores_rec, alpha=0.7, label='Recomendações')
    
    # Configurar eixos
    todos_produtos = produtos + produtos_rec
    ax1.set_xticks(np.arange(len(todos_produtos)))
    ax1.set_xticklabels(todos_produtos, rotation=45, ha='right')
    ax1.set_ylabel('Score/Rating', fontsize=12)
    ax1.set_title(f'Perfil e Recomendações - {cliente}', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Top Recomendações
    if recomendacoes:
        produtos_top = [r[0] for r in recomendacoes[:5]]
        scores_top = [r[1] for r in recomendacoes[:5]]
        
        cores = plt.cm.Reds(np.linspace(0.4, 0.9, len(produtos_top)))
        bars = ax2.barh(produtos_top, scores_top, color=cores)
        
        # Adicionar valores nas barras
        for i, (bar, score) in enumerate(zip(bars, scores_top)):
            ax2.text(score, i, f' {score:.3f}', va='center', fontweight='bold')
        
        ax2.set_xlabel('Score de Recomendação', fontsize=12)
        ax2.set_title(f'Top 5 Recomendações - {cliente}', fontsize=14, fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    nome_arquivo = f'recomendacoes_{cliente.lower()}.png'
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {nome_arquivo}")
    plt.close()


def visualizar_comparacao_metodos(sistema, cliente='Ana'):
    """Compara recomendações usando diferentes métodos."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Método Cosseno
    rec_cosseno = sistema.gerar_recomendacoes(cliente, n=5, metodo='cosseno')
    produtos_cos = [r[0] for r in rec_cosseno]
    scores_cos = [r[1] for r in rec_cosseno]
    
    ax1.barh(produtos_cos, scores_cos, color='#3498db', alpha=0.7)
    for i, score in enumerate(scores_cos):
        ax1.text(score, i, f' {score:.3f}', va='center', fontweight='bold')
    ax1.set_xlabel('Score', fontsize=12)
    ax1.set_title('Similaridade de Cosseno', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Método Pearson
    rec_pearson = sistema.gerar_recomendacoes(cliente, n=5, metodo='pearson')
    produtos_pear = [r[0] for r in rec_pearson]
    scores_pear = [r[1] for r in rec_pearson]
    
    ax2.barh(produtos_pear, scores_pear, color='#9b59b6', alpha=0.7)
    for i, score in enumerate(scores_pear):
        ax2.text(score, i, f' {score:.3f}', va='center', fontweight='bold')
    ax2.set_xlabel('Score', fontsize=12)
    ax2.set_title('Correlação de Pearson', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    
    fig.suptitle(f'Comparação de Métodos - {cliente}', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    nome_arquivo = f'comparacao_metodos_{cliente.lower()}.png'
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico salvo: {nome_arquivo}")
    plt.close()


def visualizar_dashboard_completo(sistema):
    """Cria um dashboard completo com múltiplas visualizações."""
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Matriz de Utilidade
    ax1 = fig.add_subplot(gs[0, :2])
    matriz = sistema.matriz_utilidade
    im1 = ax1.imshow(matriz.values, cmap='YlOrRd', aspect='auto')
    ax1.set_xticks(np.arange(len(matriz.columns)))
    ax1.set_yticks(np.arange(len(matriz.index)))
    ax1.set_xticklabels(matriz.columns, rotation=45, ha='right', fontsize=9)
    ax1.set_yticklabels(matriz.index, fontsize=9)
    ax1.set_title('Matriz de Utilidade', fontsize=12, fontweight='bold')
    plt.colorbar(im1, ax=ax1)
    
    # 2. Similaridades (Cosseno)
    ax2 = fig.add_subplot(gs[0, 2])
    clientes_lista = list(clientes.keys())
    n = len(clientes_lista)
    matriz_sim = np.zeros((n, n))
    for i, c1 in enumerate(clientes_lista):
        for j, c2 in enumerate(clientes_lista):
            matriz_sim[i][j] = sistema.calcular_similaridade_cosseno(c1, c2)
    im2 = ax2.imshow(matriz_sim, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax2.set_xticks(np.arange(n))
    ax2.set_yticks(np.arange(n))
    ax2.set_xticklabels(clientes_lista, fontsize=8)
    ax2.set_yticklabels(clientes_lista, fontsize=8)
    ax2.set_title('Similaridades (Cosseno)', fontsize=12, fontweight='bold')
    plt.colorbar(im2, ax=ax2)
    
    # 3-6. Recomendações por cliente
    for idx, cliente in enumerate(clientes_lista[:4]):
        row = 1 + (idx // 2)
        col = (idx % 2)
        ax = fig.add_subplot(gs[row, col])
        
        recomendacoes = sistema.gerar_recomendacoes(cliente, n=3, metodo='cosseno')
        if recomendacoes:
            produtos = [r[0][:15] + '...' if len(r[0]) > 15 else r[0] for r in recomendacoes]
            scores = [r[1] for r in recomendacoes]
            ax.barh(produtos, scores, color=plt.cm.viridis(np.linspace(0.3, 0.9, len(produtos))))
            ax.set_title(f'{cliente}', fontsize=11, fontweight='bold')
            ax.set_xlabel('Score', fontsize=9)
            ax.tick_params(labelsize=8)
            ax.grid(axis='x', alpha=0.3)
    
    fig.suptitle('Dashboard Completo - Sistema de Recomendação Open Finance', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig('dashboard_completo.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard completo salvo: dashboard_completo.png")
    plt.close()


def main():
    """Função principal que gera todas as visualizações."""
    print("="*80)
    print("GERANDO INTERFACE GRÁFICA - SISTEMA DE RECOMENDAÇÃO")
    print("="*80)
    
    # Inicializar sistema
    sistema = SistemaRecomendacaoOpenFinance(clientes)
    
    print("\n📊 Gerando visualizações...\n")
    
    # Gerar todas as visualizações
    visualizar_matriz_utilidade(sistema)
    visualizar_similaridades(sistema, metodo='cosseno')
    visualizar_similaridades(sistema, metodo='pearson')
    
    for cliente in clientes.keys():
        visualizar_recomendacoes_cliente(sistema, cliente)
    
    visualizar_comparacao_metodos(sistema, cliente='Ana')
    visualizar_dashboard_completo(sistema)
    
    print("\n" + "="*80)
    print("✅ Todas as visualizações foram geradas com sucesso!")
    print("="*80)
    print("\n📁 Arquivos gerados:")
    print("  • matriz_utilidade.png")
    print("  • similaridades_cosseno.png")
    print("  • similaridades_pearson.png")
    print("  • recomendacoes_ana.png")
    print("  • recomendacoes_marcos.png")
    print("  • recomendacoes_pedro.png")
    print("  • recomendacoes_claudia.png")
    print("  • comparacao_metodos_ana.png")
    print("  • dashboard_completo.png")
    print("\n💡 Abra os arquivos PNG para visualizar os gráficos!")
    print("="*80)


if __name__ == "__main__":
    main()

