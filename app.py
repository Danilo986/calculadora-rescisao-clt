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
    st.title("⚙️ Painel")

    # Sistema de navegação para alternar entre a calculadora e a política
    aba_selecionada = st.radio("Navegação", ["🧮 Calculadora", "📄 Política de Privacidade"])
    st.write("---")

    # Bloco reservado para monetização (Simulação de Banner Lateral)
    anuncio_sidebar = st.container()
    with anuncio_sidebar:
        st.caption("⚡ Patrocínio / Espaço AdSense")
        st.markdown(
            """
            <div style="background-color: #f9f9f9; border: 2px dashed #cccccc; padding: 40px 10px; text-align: center; border-radius: 5px;">
                <span style="color: #666666; font-weight: bold; font-size: 14px;">ANÚNCIO ADSENSE</span><br>
                <span style="color: #999999; font-size: 11px;">[ Bloco Display Vertical ]</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("---")

# --- CONTEÚDO DA ABA: CALCULADORA ---
if aba_selecionada == "🧮 Calculadora":
    with st.sidebar:
        st.subheader("Dados do Cálculo")
        salario_bruto = st.number_input("Salário Bruto (R$)", min_value=0.0, value=2000.0, step=100.0)

        # Mantendo as datas exatamente como você configurou e organizou
        data_adm = st.date_input("Data de Admissão", value=datetime(2025, 8, 5), format="DD/MM/YYYY")
        data_dem = st.date_input("Data de Demissão", value=datetime(2026, 4, 10), format="DD/MM/YYYY")

        tipo_desligamento = st.selectbox(
            "Tipo de Desligamento",
            options=["Sem Justa Causa", "Com Justa Causa", "Pedido de Demissao", "Acordo"]
        )
        saldo_fgts = st.number_input("Saldo do FGTS para Fins Rescisórios (R$)", min_value=0.0, value=3000.0,
                                     step=100.0)

    st.title("📊 Calculadora de Rescisão Trabalhista (CLT)")
    st.write("Calcule rapidamente os valores estimados para a sua rescisão contratual de forma simples e precisa.")

    if data_dem < data_adm:
        st.error("Erro: A data de demissão não pode ser anterior à data de admissão.")
    else:
        if st.button("Calcular Rescisão", type="primary", use_container_width=True):
            resultados = processar_rescisao(
                salario_bruto=salario_bruto,
                data_admissao=data_adm.strftime("%Y-%m-%d"),
                data_demissao=data_dem.strftime("%Y-%m-%d"),
                tipo_desligamento=tipo_desligamento,
                saldo_fgts_atual=saldo_fgts
            )

            st.success("Cálculo realizado com sucesso!")
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
                "*Nota: Este cálculo é uma estimativa e não substitui o documento oficial de rescisão da empresa (TRCT).")

# --- CONTEÚDO DA ABA: POLÍTICA DE PRIVACIDADE (GOOGLE) ---
else:
    st.title("📄 Política de Privacidade")
    st.write(f"Atualizado em: {datetime.now().strftime('%d/%m/%Y')}")

    st.markdown(
        """
        Esta política de privacidade descreve como tratamos as suas informações ao utilizar o site **calculadoraderesvisao.com.br**.

        ### 1. Coleta de Dados e Privacidade
        Nossa ferramenta realiza cálculos matemáticos de forma estritamente local e baseada nas informações inseridas por você. **Não coletamos, armazenamos ou compartilhamos nenhum dado pessoal**, financeiro, salarial ou de períodos contratuais informados nesta plataforma.

        ### 2. Cookies e Anúncios (Google AdSense)
        * Fornecedores terceiros, incluindo o Google, utilizam cookies para veicular anúncios com base em visitas anteriores do usuário a este ou a outros sites.
        * Com o uso de cookies de publicidade, o Google e os parceiros dele podem veicular anúncios para os usuários com base nas visitas a este site e/ou a outros sites na Internet.
        * Os usuários podem desativar a publicidade personalizada acessando as Configurações de anúncios do Google.

        ### 3. Consentimento
        Ao utilizar nossa calculadora, você concorda com os termos dispostos nesta política de privacidade.
        """
    )

# --- ESPAÇO PARA ANÚNCIO 2 (Rodapé) ---
st.write("---")
anuncio_rodape = st.container()
with anuncio_rodape:
    st.caption("📢 Links Patrocinados")
    st.markdown(
        """
        <div style="background-color: #f9f9f9; border: 2px dashed #cccccc; padding: 20px; text-align: center; border-radius: 5px; width: 100%;">
            <span style="color: #666666; font-weight: bold; font-size: 14px;">ANÚNCIO ADSENSE</span><br>
            <span style="color: #999999; font-size: 11px;">[ Bloco Horizontal Responsivo ]</span>
        </div>
        """,
        unsafe_allow_html=True
    )

