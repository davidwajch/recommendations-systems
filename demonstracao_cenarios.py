"""
Demonstração de Cenários de Uso - Sistema de Recomendação Open Finance
Este script demonstra cenários fictícios de uso do sistema de recomendação.
"""

from analise import SistemaRecomendacaoOpenFinance, clientes
import json

def exibir_cenario(cliente_nome: str, descricao: str, sistema):
    """Exibe um cenário de uso formatado."""
    print("\n" + "="*80)
    print(f"CENÁRIO: {cliente_nome}")
    print("="*80)
    print(f"\n{descricao}\n")
    print("-"*80)
    
    # Produtos atuais
    produtos_atuais = clientes[cliente_nome]
    print(f"\n📊 Perfil Atual de {cliente_nome}:")
    for produto, rating in sorted(produtos_atuais.items(), key=lambda x: x[1], reverse=True):
        estrelas = "⭐" * int(rating) if rating >= 1 else "☆"
        print(f"  • {produto}: {estrelas} (rating: {rating})")
    
    # Clientes similares
    similares = sistema.encontrar_clientes_similares(cliente_nome, n=2)
    print(f"\n👥 Clientes com Perfil Similar:")
    for cliente_sim, sim_score in similares:
        porcentagem = sim_score * 100
        print(f"  • {cliente_sim}: {porcentagem:.1f}% de similaridade")
    
    # Recomendações
    recomendacoes = sistema.gerar_recomendacoes(cliente_nome, n=3)
    print(f"\n💡 Recomendações para {cliente_nome}:")
    if recomendacoes:
        for i, (produto, score) in enumerate(recomendacoes, 1):
            print(f"\n  {i}. {produto}")
            print(f"     Score: {score:.3f}")
            print(f"     Justificativa: Clientes similares utilizam este produto")
    else:
        print("  Nenhuma recomendação disponível no momento.")
    
    print("\n" + "="*80)


def cenario_1_ana(sistema):
    """Cenário 1: Cliente Novo - Ana"""
    descricao = """
CONTEXTO:
Ana é uma profissional liberal de 32 anos, cliente nova na QuantumFinance.
Ela demonstra preferência por produtos de investimento (Renda Fixa) e crédito 
(Crédito Pessoal), mas tem baixa interação com produtos básicos.

OBJETIVO:
Identificar produtos que clientes similares utilizam e que podem ser úteis 
para Ana, aumentando seu engajamento com a plataforma.
"""
    exibir_cenario("Ana", descricao, sistema)


def cenario_2_marcos(sistema):
    """Cenário 2: Cliente Ativo - Marcos"""
    descricao = """
CONTEXTO:
Marcos é um investidor de 45 anos, cliente ativo com portfólio diversificado.
Ele tem perfil conservador com forte presença em Renda Fixa e Poupança, e 
recentemente demonstrou interesse em Renda Variável.

OBJETIVO:
Recomendar produtos que complementem seu perfil de investidor e que clientes 
similares utilizam com sucesso.
"""
    exibir_cenario("Marcos", descricao, sistema)


def cenario_3_pedro(sistema):
    """Cenário 3: Cliente Premium - Pedro"""
    descricao = """
CONTEXTO:
Pedro é um empresário de 38 anos com alta interação com produtos de crédito.
Ele não possui produtos de investimento de renda fixa, indicando possível 
oportunidade de diversificação.

OBJETIVO:
Identificar oportunidades de cross-sell, especialmente produtos de investimento 
que podem balancear seu perfil financeiro.
"""
    exibir_cenario("Pedro", descricao, sistema)


def cenario_4_claudia(sistema):
    """Cenário 4: Cliente Conservador - Claudia"""
    descricao = """
CONTEXTO:
Claudia é uma aposentada de 62 anos com perfil muito conservador.
Ela foca em produtos básicos e seguros, principalmente Poupança.
Não possui produtos de crédito ou investimentos mais complexos.

OBJETIVO:
Recomendar produtos que mantenham o perfil conservador mas ofereçam melhor 
retorno, como Renda Fixa, que é mais segura que Renda Variável.
"""
    exibir_cenario("Claudia", descricao, sistema)


def exibir_comparacao_metodos(sistema):
    """Compara recomendações usando diferentes métodos de similaridade."""
    print("\n" + "="*80)
    print("COMPARAÇÃO DE MÉTODOS DE SIMILARIDADE")
    print("="*80)
    
    cliente = "Ana"
    print(f"\nRecomendações para {cliente} usando diferentes métodos:\n")
    
    # Método Cosseno
    rec_cosseno = sistema.gerar_recomendacoes(cliente, n=3, metodo='cosseno')
    print("📐 Similaridade de Cosseno:")
    for produto, score in rec_cosseno:
        print(f"  • {produto}: {score:.3f}")
    
    # Método Pearson
    rec_pearson = sistema.gerar_recomendacoes(cliente, n=3, metodo='pearson')
    print("\n📊 Correlação de Pearson:")
    for produto, score in rec_pearson:
        print(f"  • {produto}: {score:.3f}")
    
    print("\n" + "="*80)


def exibir_fluxo_completo(sistema):
    """Demonstra o fluxo completo de recomendação."""
    print("\n" + "="*80)
    print("FLUXO COMPLETO DE RECOMENDAÇÃO")
    print("="*80)
    
    cliente = "Ana"
    print(f"\n1️⃣ COLETA DE DADOS")
    print(f"   Cliente: {cliente}")
    print(f"   Dados coletados via Open Finance APIs")
    print(f"   Produtos identificados: {len(clientes[cliente])}")
    
    print(f"\n2️⃣ PROCESSAMENTO")
    print(f"   Matriz de utilidade criada")
    print(f"   Similaridades calculadas")
    
    similares = sistema.encontrar_clientes_similares(cliente, n=2)
    print(f"\n3️⃣ IDENTIFICAÇÃO DE CLIENTES SIMILARES")
    for cliente_sim, sim_score in similares:
        print(f"   • {cliente_sim}: {sim_score:.3f}")
    
    recomendacoes = sistema.gerar_recomendacoes(cliente, n=3)
    print(f"\n4️⃣ GERAÇÃO DE RECOMENDAÇÕES")
    for i, (produto, score) in enumerate(recomendacoes, 1):
        print(f"   {i}. {produto} (score: {score:.3f})")
    
    print(f"\n5️⃣ APRESENTAÇÃO")
    print(f"   Recomendações enviadas via:")
    print(f"   • App Mobile")
    print(f"   • Email personalizado")
    print(f"   • Dashboard Web")
    
    print(f"\n6️⃣ FEEDBACK (Simulado)")
    print(f"   Cliente visualiza recomendações")
    print(f"   Cliente interage (aceita/rejeita)")
    print(f"   Sistema aprende para próximas recomendações")
    
    print("\n" + "="*80)


def main():
    """Função principal que executa todos os cenários."""
    print("="*80)
    print("DEMONSTRAÇÃO DE CENÁRIOS DE USO")
    print("Sistema de Recomendação - Open Finance - QuantumFinance")
    print("="*80)
    
    # Inicializar sistema
    sistema = SistemaRecomendacaoOpenFinance(clientes)
    
    # Executar cenários
    cenario_1_ana(sistema)
    cenario_2_marcos(sistema)
    cenario_3_pedro(sistema)
    cenario_4_claudia(sistema)
    
    # Comparação de métodos
    exibir_comparacao_metodos(sistema)
    
    # Fluxo completo
    exibir_fluxo_completo(sistema)
    
    print("\n" + "="*80)
    print("Demonstração concluída!")
    print("="*80)
    print("\n📝 Notas:")
    print("• Todos os cenários são fictícios e para fins de demonstração")
    print("• Os dados são baseados no dataset fornecido do Open Finance")
    print("• Em produção, o sistema utilizaria dados reais e atualizados")
    print("• O feedback dos clientes melhoraria as recomendações ao longo do tempo")
    print("="*80)


if __name__ == "__main__":
    main()

