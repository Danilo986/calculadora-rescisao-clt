import streamlit as st
from datetime import datetime
from calculos import processar_rescisao

# Configuração da página para alta performance e responsividade
st.set_page_config(
    page_title="Calculadora de Rescisão CLT",
    page_icon="📊",
    layout="centered"
)

# --- ESPAÇO PARA ANÚNCIO 1 (Barra Lateral) ---
with st.sidebar:
    st.title("Configurações")

    # Bloco reservado para monetização
    anuncio_sidebar = st.container()
    with anuncio_sidebar:
        st.caption("⚡ Patrocínio / Espaço AdSense")
        # Futuro código do AdSense entra aqui: st.components.v1.html("scripts")
        st.write("---")

    # Entradas de dados do usuário
    salario_bruto = st.number_input("Salário Bruto (R$)", min_value=0.0, value=2000.0, step=100.0)

    data_adm = st.date_input("Data de Admissão", value=datetime(2023, 1, 1))
    data_dem = st.date_input("Data de Demissão", value=datetime(2024, 6, 1))

    tipo_desligamento = st.selectbox(
        "Tipo de Desligamento",
        options=["Sem Justa Causa", "Com Justa Causa", "Pedido de Demissao", "Acordo"]
    )

    saldo_fgts = st.number_input("Saldo do FGTS para Fins Rescisórios (R$)", min_value=0.0, value=3000.0, step=100.0)

# --- CORPO PRINCIPAL DO APLICATIVO ---
st.title("📊 Calculadora de Rescisão Trabalhista (CLT)")
st.write("Calcule rapidamente os valores estimados para a sua rescisão contratual de forma simples e precisa.")

# Validação simples de segurança nas datas
if data_dem < data_adm:
    st.error("Erro: A data de demissão não pode ser anterior à data de admissão.")
else:
    # Botão de execução do cálculo
    if st.button("Calcular Rescisão", type="primary", use_container_width=True):
        # Chamada da nossa Inteligência (calculos.py)
        resultados = processar_rescisao(
            salario_bruto=salario_bruto,
            data_admissao=data_adm.strftime("%Y-%m-%d"),
            data_demissao=data_dem.strftime("%Y-%m-%d"),
            tipo_desligamento=tipo_desligamento,
            saldo_fgts_atual=saldo_fgts
        )

        st.success("Cálculo realizado com sucesso!")

        # Exibição dos resultados em métricas e tabelas limpas
        st.subheader("📋 Resumo dos Valores")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Saldo de Salário", value=f"R$ {resultados['saldo_salario']:.2f}")
            st.metric(label="13º Proporcional", value=f"R$ {resultados['decimo_terceiro']:.2f}")
            st.metric(label="Multa FGTS", value=f"R$ {resultados['multa_fgts']:.2f}")
        with col2:
            st.metric(label=f"Aviso Prévio ({resultados['dias_aviso']} dias)",
                      value=f"R$ {resultados['valor_aviso']:.2f}")
            st.metric(label="Férias Proporcionais", value=f"R$ {resultados['ferias_proporcionais']:.2f}")
            st.metric(label="Terço de Férias (1/3)", value=f"R$ {resultados['terco_ferias']:.2f}")

        st.write("---")
        st.metric(label="💰 TOTAL GERAL BRUTO", value=f"R$ {resultados['total_geral']:.2f}")
        st.caption(
            "*Nota: Este cálculo é uma estimativa e não substitui o documento oficial de rescisão da empresa (TRCT), pois não considera descontos de INSS, IRRF ou faltas.")

# --- ESPAÇO PARA ANÚNCIO 2 (Rodapé) ---
st.write("---")
anuncio_rodape = st.container()
with anuncio_rodape:
    st.caption("📢 Links Patrocinados")
    # Futuro código do AdSense entra aqui
