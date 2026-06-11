from datetime import datetime


def calcular_meses_proporcionais(data_inicio: datetime, data_fim: datetime) -> int:
    """Calcula frações de meses trabalhados superiores ou iguais a 15 dias."""
    # Se a demissão ocorrer antes do dia 15 no primeiro mês incompleto (caso mude de ano rápido)
    # Mas a lógica padrão avalia os avos do ano corrente
    meses_avos = 0

    # Lógica simplificada para avos proporcionais do ano da demissão (13º e Férias)
    # Para o 13º, contam-se os meses trabalhados no ano civil da demissão com >= 15 dias
    # Para simplificação de escopo inicial, faremos o cálculo do ano corrente:
    ano_demissao = data_fim.year

    # Se começou e terminou no mesmo ano
    if data_inicio.year == ano_demissao:
        mes_inicial = data_inicio.month
        # Verifica se o primeiro mês teve 15 dias ou mais trabalhados
        if (30 - data_inicio.day + 1) < 15:
            mes_inicial += 1
    else:
        mes_inicial = 1

    mes_final = data_fim.month
    if data_fim.day < 15:
        mes_final -= 1

    meses_avos = max(0, mes_final - mes_inicial + 1)
    return min(12, meses_avos)


def calcular_anos_completos(data_inicio: datetime, data_fim: datetime) -> int:
    """Calcula a quantidade de anos completos para o cálculo do aviso prévio."""
    diferenca = data_fim - data_inicio
    return int(diferenca.days // 365.25)


def processar_rescisao(
        salario_bruto: float,
        data_admissao: str,
        data_demissao: str,
        tipo_desligamento: str,
        saldo_fgts_atual: float = 0.0
) -> dict:
    """
    Executa os cálculos rescisórios com base na CLT.
    Tipos: 'Sem Justa Causa', 'Com Justa Causa', 'Pedido de Demissao', 'Acordo'
    """
    fmt = "%Y-%m-%d"
    dt_adm = datetime.strptime(data_admissao, fmt)
    dt_dem = datetime.strptime(data_demissao, fmt)

    dias_mes_demissao = dt_dem.day
    anos_trabalhados = calcular_anos_completos(dt_adm, dt_dem)

    # 1. Saldo de Salário
    saldo_salario = (salario_bruto / 30) * dias_mes_demissao

    # 2. Aviso Prévio Proporcional (Lei 12.506/2011)
    dias_aviso = 30 + (3 * anos_trabalhados) if anos_trabalhados > 0 else 30
    dias_aviso = min(90, dias_aviso)
    valor_aviso_previo = (salario_bruto / 30) * dias_aviso

    # 3. Décimo Terceiro Proporcional
    avos_13 = calcular_meses_proporcionais(dt_adm, dt_dem)
    decimo_terceiro = (salario_bruto / 12) * avos_13

    # 4. Férias Proporcionais + 1/3 (Simplificado para o ciclo proporcional)
    # Em um sistema real, avalia-se o período aquisitivo aberto. Aqui pegamos os avos proporcionais.
    avos_ferias = calcular_meses_proporcionais(dt_adm, dt_dem)
    ferias_proporcionais = (salario_bruto / 12) * avos_ferias
    terco_ferias = ferias_proporcionais / 3

    # 5. Regras de Negócio por Tipo de Desligamento
    multa_fgts = 0.0
    pagar_aviso = False

    if tipo_desligamento == 'Sem Justa Causa':
        multa_fgts = saldo_fgts_atual * 0.40
        pagar_aviso = True
    elif tipo_desligamento == 'Com Justa Causa':
        valor_aviso_previo = 0.0
        decimo_terceiro = 0.0
        ferias_proporcionais = 0.0
        terco_ferias = 0.0
    elif tipo_desligamento == 'Pedido de Demissao':
        valor_aviso_previo = 0.0  # Empregado que paga ou trabalha (não recebe na rescisão líquida)
    elif tipo_desligamento == 'Acordo':
        multa_fgts = saldo_fgts_atual * 0.20
        valor_aviso_previo = valor_aviso_previo * 0.50  # Metade do aviso prévio indenizado

    total_rescindido = saldo_salario + (
        valor_aviso_previo if pagar_aviso or tipo_desligamento == 'Acordo' else 0) + decimo_terceiro + ferias_proporcionais + terco_ferias + multa_fgts

    return {
        "saldo_salario": round(saldo_salario, 2),
        "dias_aviso": dias_aviso,
        "valor_aviso": round(valor_aviso_previo, 2) if (pagar_aviso or tipo_desligamento == 'Acordo') else 0.0,
        "decimo_terceiro": round(decimo_terceiro, 2),
        "ferias_proporcionais": round(ferias_proporcionais, 2),
        "terco_ferias": round(terco_ferias, 2),
        "multa_fgts": round(multa_fgts, 2),
        "total_geral": round(total_rescindido, 2)
    }


def calcular_seguro_desemprego(salario_medio: float, meses_trabalhados: int, numero_solicitacao: int) -> dict:
    """
    Calcula a elegibilidade, quantidade de parcelas e valor do seguro-desemprego
    com base nas regras vigentes e tabela oficial de 2026.
    """
    # 1. Verificação de Carência (Elegibilidade)
    if numero_solicitacao == 1 and meses_trabalhados < 12:
        return {"elegivel": False,
                "motivo": "Exige no mínimo 12 meses trabalhados nos últimos 18 meses para a 1ª solicitação."}
    elif numero_solicitacao == 2 and meses_trabalhados < 9:
        return {"elegivel": False,
                "motivo": "Exige no mínimo 9 meses trabalhados nos últimos 12 meses para a 2ª solicitação."}
    elif numero_solicitacao >= 3 and meses_trabalhados < 6:
        return {"elegivel": False,
                "motivo": "Exige no mínimo 6 meses trabalhados imediatamente anteriores à demissão para a 3ª solicitação ou mais."}

    # 2. Definição da Quantidade de Parcelas
    if 6 <= meses_trabalhados <= 11:
        parcelas = 3
    elif 12 <= meses_trabalhados <= 23:
        parcelas = 4
    else:
        parcelas = 5

    # 3. Cálculo do Valor da Parcela (Tabela Oficial de 2026)
    if salario_medio <= 2222.17:
        valor = salario_medio * 0.8
    elif salario_medio <= 3703.99:
        valor = ((salario_medio - 2222.17) * 0.5) + 1777.74
    else:
        valor = 2518.65

    # Garante o piso do salário mínimo vigente em 2026 (R$ 1.621,00)
    if valor < 1621.00:
        valor = 1621.00

    return {"elegivel": True, "parcelas": parcelas, "valor_parcela": round(valor, 2)}

