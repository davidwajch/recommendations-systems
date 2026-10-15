"""
Demonstração de Cenários de Uso - Sistema de Recomendação Open Finance
Cenários fictícios simulados
"""

from analise import SistemaRecomendacaoOpenFinance, clientes


def exibir_cenario(cliente_nome: str, descricao: str, sistema):
    """Exibe um cenário de uso formatado."""
    print("\n" + "="*80)
    print(f"CENÁRIO: {cliente_nome}")
    print("="*80)
    print(f"\n{descricao}\n")
    print("-"*80)
    
    produtos_atuais = clientes[cliente_nome]
    print(f"\n📊 Perfil Atual de {cliente_nome}:")
    for produto, rating in sorted(produtos_atuais.items(), key=lambda x: x[1], reverse=True):
        estrelas = "⭐" * int(rating) if rating >= 1 else "☆"
        print(f"  • {produto}: {estrelas} (rating: {rating})")
    
    similares = sistema.encontrar_clientes_similares(cliente_nome, n=2)
    print(f"\n👥 Clientes com Perfil Similar:")
    for cliente_sim, sim_score in similares:
        porcentagem = sim_score * 100
        print(f"  • {cliente_sim}: {porcentagem:.1f}% de similaridade")
    
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
    """Cenário 1: Cliente com perfil de investimento."""
    descricao = """
CONTEXTO:
Ana é profissional liberal de 32 anos, cliente nova na QuantumFinance.
Tem preferência por produtos de investimento (Renda Fixa) e crédito,
mas baixa interação com produtos básicos.

OBJETIVO:
Identificar produtos que clientes similares utilizam para aumentar engajamento.
"""
    exibir_cenario("Ana", descricao, sistema)


def cenario_2_marcos(sistema):
    """Cenário 2: Cliente ativo com portfólio diversificado."""
    descricao = """
CONTEXTO:
Marcos é investidor de 45 anos com perfil conservador.
Forte presença em Renda Fixa e Poupança, recentemente demonstrou
interesse em Renda Variável.

OBJETIVO:
Recomendar produtos que complementem perfil de investidor.
"""
    exibir_cenario("Marcos", descricao, sistema)


def cenario_3_pedro(sistema):
    """Cenário 3: Cliente com alta interação em crédito."""
    descricao = """
CONTEXTO:
Pedro é empresário de 38 anos com alta interação em produtos de crédito.
Não possui produtos de investimento de renda fixa, possível oportunidade
de diversificação.

OBJETIVO:
Identificar oportunidades de cross-sell em produtos de investimento.
"""
    exibir_cenario("Pedro", descricao, sistema)


def cenario_4_claudia(sistema):
    """Cenário 4: Cliente com perfil conservador."""
    descricao = """
CONTEXTO:
Claudia, 62 anos, aposentada com perfil muito conservador.
Foco em produtos básicos e seguros, principalmente Poupança.

OBJETIVO:
Recomendar produtos que mantenham perfil conservador mas ofereçam
melhor retorno, como Renda Fixa.
"""
    exibir_cenario("Claudia", descricao, sistema)


def exibir_comparacao_metodos(sistema):
    """Compara recomendações usando cosseno vs Pearson."""
    print("\n" + "="*80)
    print("COMPARAÇÃO DE MÉTODOS DE SIMILARIDADE")
    print("="*80)
    
    cliente = "Ana"
    print(f"\nRecomendações para {cliente} usando diferentes métodos:\n")
    
    rec_cosseno = sistema.gerar_recomendacoes(cliente, n=3, metodo='cosseno')
    print("📐 Similaridade de Cosseno:")
    for produto, score in rec_cosseno:
        print(f"  • {produto}: {score:.3f}")
    
    rec_pearson = sistema.gerar_recomendacoes(cliente, n=3, metodo='pearson')
    print("\n📊 Correlação de Pearson:")
    for produto, score in rec_pearson:
        print(f"  • {produto}: {score:.3f}")
    
    print("\n" + "="*80)


def exibir_fluxo_completo(sistema):
    """Demonstra fluxo completo de recomendação."""
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
    """Executa todos os cenários de demonstração."""
    print("="*80)
    print("DEMONSTRAÇÃO DE CENÁRIOS DE USO")
    print("Sistema de Recomendação - Open Finance - QuantumFinance")
    print("="*80)
    
    sistema = SistemaRecomendacaoOpenFinance(clientes)
    
    cenario_1_ana(sistema)
    cenario_2_marcos(sistema)
    cenario_3_pedro(sistema)
    cenario_4_claudia(sistema)
    
    exibir_comparacao_metodos(sistema)
    exibir_fluxo_completo(sistema)
    
    print("\n" + "="*80)
    print("Demonstração concluída!")
    print("="*80)
    print("\n📝 Notas:")
    print("• Todos os cenários são fictícios para fins de demonstração")
    print("• Dados baseados no dataset fornecido do Open Finance")
    print("• Em produção, sistema utilizaria dados reais e atualizados")
    print("• Feedback dos clientes melhoraria recomendações ao longo do tempo")
    print("="*80)


if __name__ == "__main__":
    main()
