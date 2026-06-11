import streamlit as st
from datetime import datetime
from calculos import processar_rescisao, calcular_seguro_desemprego

# Configuração da página limpa e correta
st.set_page_config(
    page_title="Calculadora de Rescisão CLT",
    page_icon="📊",
    layout="centered"
)

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stAppDeployButton {display:none;}
        .block-container {padding-bottom: 1rem;}
    </style>
    """,
    unsafe_allow_html=True
)


# --- BARRA LATERAL (Apenas Navegação e Anúncio Fixo) ---
with st.sidebar:
    st.title("⚙️ Painel")

    # Sistema de navegação
    aba_selecionada = st.radio(
        "Navegação",
        ["🧮 Calculadora", "💰 Seguro-Desemprego", "📄 Política de Privacidade"]
    )
    st.write("---")

    # Bloco reservado para monetização lateral
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
    st.title("📊 Calculadora de Rescisão Trabalhista (CLT)")
    st.write("Calcule rapidamente os valores estimados para a sua rescisão contratual de forma simples e precisa.")
    st.write("---")

    # CAMPOS DE ENTRADA NO CORPO PRINCIPAL (Não ficam mais escondidos na lateral)
    st.subheader("📋 Dados do Cálculo")

    # Organizando os campos em colunas para ocupar menos espaço vertical
    col_inputs1, col_inputs2 = st.columns(2)

    with col_inputs1:
        salario_bruto = st.number_input("Salário Bruto (R$)", min_value=0.0, value=2000.0, step=100.0)
        data_adm = st.date_input("Data de Admissão", value=datetime(2025, 8, 5), format="DD/MM/YYYY")

    with col_inputs2:
        saldo_fgts = st.number_input("Saldo do FGTS para Fins Rescisórios (R$)", min_value=0.0, value=3000.0,
                                     step=100.0)
        data_dem = st.date_input("Data de Demissão", value=datetime(2026, 4, 10), format="DD/MM/YYYY")

    tipo_desligamento = st.selectbox(
        "Tipo de Desligamento",
        options=["Sem Justa Causa", "Com Justa Causa", "Pedido de Demissao", "Acordo"]
    )

    st.write("---")

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

    # --- SEÇÃO FAQ PARA SEO ---
    st.write("---")
    st.subheader("❓ Dúvidas Frequentes sobre Rescisão Trabalhista")

    with st.expander("Como é calculado o Saldo de Salário?"):
        st.write("""
        O saldo de salário é calculado dividindo o valor do seu salário bruto por 30 
        (número padrão de dias do mês comercial) e multiplicando pelo número de dias efetivamente 
        trabalhados no mês da demissão.
        """)

    with st.expander("Quem tem direito ao Aviso Prévio Proporcional?"):
        st.write("""
        De acordo com a Lei 12.506/2011, o aviso prévio começa em 30 dias para quem tem até 1 ano de empresa. 
        A cada ano completo trabalhado na mesma empresa, são somados mais 3 dias, até o limite máximo de 90 dias (20 anos de trabalho).
        """)

    with st.expander("O que são os avos profissionais de 13º e Férias?"):
        st.write("""
        O trabalhador ganha o direito a 1/12 (um avo) de 13º salário e de férias para cada mês trabalhado. 
        Para que o mês corrente conte como um mês cheio (um avo), é necessário ter trabalhado pelo menos 15 dias dentro daquele mês civil.
        """)

# --- CONTEÚDO DA ABA: SEGURO-DESEMPREGO ---
elif aba_selecionada == "💰 Seguro-Desemprego":
    st.title("💰 Simulador de Seguro-Desemprego (Regras 2026)")
    st.write("Verifique se você cumpre os critérios de carência e descubra o valor estimado das suas parcelas.")
    st.write("---")

    # CAMPOS DE ENTRADA NO CORPO PRINCIPAL
    st.subheader("📋 Dados da Simulação")

    col_seg1, col_seg2 = st.columns(2)

    with col_seg1:
        solicitacao = st.selectbox(
            "Número da Solicitação",
            options=[1, 2, 3],
            format_func=lambda x: f"{x}ª vez que solicito"
        )
        media_salario = st.number_input("Salário Médio (R$)", min_value=0.0, value=2000.0, step=100.0)

    with col_seg2:
        meses = st.number_input(
            "Meses Trabalhados (Último Emprego)",
            min_value=1,
            max_value=360,
            value=12,
            step=1
        )

    st.write("---")

    if st.button("Simular Benefício", type="primary", use_container_width=True):
        resultado = calcular_seguro_desemprego(
            salario_medio=media_salario,
            meses_trabalhados=meses,
            numero_solicitacao=solicitacao
        )

        if resultado["elegivel"]:
            st.success("🎉 Você tem direito ao Seguro-Desemprego!")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Quantidade de Parcelas", value=f"{resultado['parcelas']} parcelas")
            with col2:
                st.metric(label="Valor de Cada Parcela", value=f"R$ {resultado['valor_parcela']:.2f}")

            total_estimado = resultado['parcelas'] * resultado['valor_parcela']
            st.info(f"**Valor total estimado a receber:** R$ {total_estimado:.2f}")
        else:
            st.error(f"❌ Não elegível: {resultado['motivo']}")

    # --- SEÇÃO FAQ PARA SEO ---
    st.write("---")
    st.subheader("❓ Dúvidas Frequentes sobre o Seguro-Desemprego")

    with st.expander("Qual o intervalo mínimo entre um pedido de Seguro-Desemprego e outro?"):
        st.write("""
        A legislação brasileira estabelece que o trabalhador deve respeitar um intervalo mínimo de 
        **16 meses** entre o início de uma solicitação do benefício e a data de dispensa do novo emprego para ter direito novamente.
        """)

    with st.expander("Quantos meses preciso trabalhar para pedir o seguro pela 1ª vez?"):
        st.write("""
        Para a **primeira solicitação**, você precisa ter trabalhado pelo menos **12 meses** com carteira assinada nos últimos 18 meses anteriores à data de demissão.
        """)

    with st.expander("Qual o valor máximo (teto) do Seguro-Desemprego em 2026?"):
        st.write("""
        Com os reajustes do Ministério do Trabalho para o ano de 2026, o valor máximo que um trabalhador pode receber por parcela é de **R$ 2.518,65**, mesmo que a média salarial dos últimos meses tenha sido muito maior.
        """)

# --- CONTEÚDO DA ABA: POLÍTICA DE PRIVACIDADE ---
elif aba_selecionada == "📄 Política de Privacidade":
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
