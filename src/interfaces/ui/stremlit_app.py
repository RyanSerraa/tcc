import streamlit as st

from src.application.query_manager import QueryManager


class Index:

    def __init__(self, query_manager: QueryManager, schema_text: str):
        self.query_manager = query_manager
        self.schema_text = schema_text

    def render(self):
        schema_text = self.schema_text
        st.set_page_config(
            page_title="Text-to-SQL Converter",
            page_icon=":database:",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.markdown(
            """
            <style>
                :root {
                    --primary-color: #6c8ae4;
                    --secondary-color: #ff6b6b;
                    --accent-color: #4fd1c5;
                    --text-color: #f8f9fa;
                    --dark-text: #2c3e50;
                    --card-bg: rgba(30, 41, 59, 0.8);
                    --card-hover: rgba(30, 41, 59, 1);
                    --shadow-color: rgba(0,0,0,0.3);
                    --transition-speed: 0.4s;
                    --background-dark: #0f172a;
                    --background-darker: #0b1120;
                }

                .stApp {
                    background: var(--background-dark);
                    color: var(--text-color);
                }

                .header-title {
                    color: var(--text-color);
                    text-align: center;
                    margin-bottom: 1.5rem;
                    position: relative;
                    padding-bottom: 15px;
                }

                .header-title::after {
                    content: '';
                    position: absolute;
                    bottom: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 80px;
                    height: 4px;
                    background: var(--accent-color);
                    border-radius: 2px;
                }

                .card {
                    background: var(--card-bg);
                    border-radius: 15px;
                    padding: 1.5rem;
                    transition: all var(--transition-speed) ease;
                    box-shadow: 0 10px 25px var(--shadow-color);
                    border: 1px solid rgba(255,255,255,0.1);
                    min-height: 321.93px;
                    height: 100%;
                    position: relative;
                    overflow: hidden;
                }

                .card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 5px;
                    background: var(--accent-color);
                    transform: scaleX(0);
                    transform-origin: left;
                    transition: transform var(--transition-speed) ease;
                }

                .card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
                    background: var(--card-hover);
                }

                .card:hover::before {
                    transform: scaleX(1);
                }

                .card-icon {
                    font-size: 2.5rem;
                    color: var(--accent-color);
                    margin-bottom: 1rem;
                    transition: all var(--transition-speed) ease;
                }

                .card:hover .card-icon {
                    transform: scale(1.1);
                }

                .card h3 {
                    color: var(--text-color);
                    margin-bottom: 0.5rem;
                }

                .card p {
                    color: var(--text-color);
                    opacity: 0.8;
                    font-size: 0.95rem;
                }

                .info-box {
                    background-color: rgba(79, 209, 197, 0.1);
                    border-left: 4px solid var(--accent-color);
                    padding: 1.25rem;
                    margin-bottom: 1.5rem;
                    border-radius: 0 8px 8px 0;
                    color: var(--text-color);
                }

                .stTextArea textarea {
                    min-height: 150px !important;
                    border-radius: 8px !important;
                    border: 1px solid #374151 !important;
                    background-color: #1e293b !important;
                    color: var(--text-color) !important;
                }

                .stButton button {
                    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
                    color: var(--dark-text) !important;
                    border: none;
                    padding: 10px 24px;
                    border-radius: 8px;
                    font-size: 16px;
                    transition: all 0.3s;
                    width: 100%;
                    font-weight: bold;
                }

                .stButton button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
                }

                .stCodeBlock {
                    border-radius: 8px;
                    border: 1px solid #374151;
                    padding: 1rem;
                    background-color: #1e293b;
                }

                .schema-container {
                    max-height: 300px;
                    overflow-y: auto;
                    border-radius: 8px;
                    padding: 1rem;
                    background-color: #1e293b;
                    border: 1px solid #374151;
                }

                .feature-card {
                    background: rgba(30, 41, 59, 0.8);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                    border-left: 4px solid var(--accent-color);
                }

                .feature-card h4 {
                    color: var(--accent-color);
                }

                .feature-card p {
                    color: var(--text-color);
                    opacity: 0.8;
                }

                /* Estilos para os elementos do Streamlit */
                .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                    color: var(--text-color) !important;
                }

                .stAlert {
                    background-color: rgba(255, 107, 107, 0.1) !important;
                    border-left: 4px solid var(--secondary-color) !important;
                }

                .stSpinner > div {
                    color: var(--accent-color) !important;
                }

                .st-expander {
                    background-color: #1e293b;
                    border: 1px solid #374151;
                    border-radius: 8px;
                }

                .st-expander .st-expanderHeader {
                    color: var(--text-color);
                }

                @media (max-width: 768px) {
                    .card {
                        padding: 1.25rem;
                    }

                    .card-icon {
                        font-size: 2rem;
                    }
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # Layout principal
        st.markdown(
            """
            <div class="header-title">
                <h1>Crime Flow</h1>
                <p>Descubra padrões e estatísticas sobre violência nos EUA.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        # Seção de cards de recursos
        st.markdown("### Principais Painéis Interativos")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(
                """
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
                <a href="http://161.35.61.141:3000/public/dashboard/95ac4087-b5b8-45af-9a87-668741ffa295" class="card" style="display: block; text-decoration: none;">
                    <div class="card-icon"><i class="fas fa-handcuffs card-icon"></i></div>
                    <h3>Prisões</h3>
                    <p>Visualize dados detalhados de prisões com análises temporais e geográficas</p>
                </a>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                """
                <a href="http://161.35.61.141:3000/public/dashboard/af56ff3c-24f0-409f-b3f1-5a6c2bf4dddc" class="card" style="display: block; text-decoration: none;">
                    <div class="card-icon"><i class="fas fa-gavel card-icon"></i></div>
                    <h3>Crimes</h3>
                    <p>Análise completa de registros criminais com tendências e padrões</p>
                </a>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                """
                <a href="http://161.35.61.141:3000/public/dashboard/7c38c974-4ee2-43df-895c-d44bbd701ed9" class="card" style="display: block; text-decoration: none;">
                    <div class="card-icon"><i class="fas fa-skull card-icon"></i></div>
                    <h3>Confrontos Fatais</h3>
                    <p>Casos sobre confrontos fatais e análises de circunstâncias</p>
                </a>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                """
                <a href="http://161.35.61.141:3000/public/dashboard/a81a61ba-5c63-4e3f-b6a0-e3efba33feae" class="card" style="display: block; text-decoration: none;">
                    <div class="card-icon"><i class="fas fa-heart-broken card-icon"></i></div>
                    <h3>Óbitos Policiais</h3>
                    <p>Óbitos policiais registrados com análises de causas e prevenção</p>
                </a>
                """,
                unsafe_allow_html=True,
            )

        with col5:
            st.markdown(
                """
                <a href="http://161.35.61.141:3000/public/dashboard/18d44459-68c1-4f5a-af24-0a05711bdc62" class="card" style="display: block; text-decoration: none;">
                    <div class="card-icon"><i class="fas fa-crosshairs card-icon"></i></div>
                    <h3>Tiroteios</h3>
                    <p>Incidentes com arma de fogo e estatísticas de ocorrências</p>
                </a>
                """,
                unsafe_allow_html=True,
            )

        # Layout da interface de conversão
        st.markdown("---")
        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("### 📋 Schema Atual")
            with st.expander("Visualizar Schema", expanded=True):
                st.code(schema_text, language="sql")

            st.markdown("### 📌 Dicas")
            st.markdown(
                """
                <div class="feature-card">
                    <h4>Seja específico</h4>
                    <p>Você pode pedir para que a resposta seja textual, em gráfico ou em tabela</p>
                </div>

                <div class="feature-card">
                    <h4>Exemplo de consulta</h4>
                    <p>"Qual é a principal causa de morte na Califórnia em confrontos fatais?"</p>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with col_right:
            st.markdown(
                """
                <div class="info-box">
                    💡 Descreva em linguagem natural quais dados que você precisa sobre violência nos EUA.
                </div>
            """,
                unsafe_allow_html=True,
            )

            query = st.text_area(
                "Descreva sua necessidade de dados:",
                placeholder="Ex: Qual é a principal causa de morte na Califórnia em confrontos fatais?",
                label_visibility="collapsed",
            )

            if st.button("Gerar resposta", type="primary"):
                if not query:
                    st.warning("Por favor, insira uma pergunta aqui.")
                else:
                    with st.spinner("🧠 Processando sua solicitação..."):
                        try:
                            # 🚀 Chamada ao backend (AgentManager)
                            result = self.query_manager.consultar_dados(query)

                            # Pega a resposta
                            answer = result.get("answer") or result.get("result")

                            st.markdown("### 🔍 Resultado")
                            st.write(answer)

                            # Botões de ação
                            col1, col2 = st.columns([1, 1])
                            with col1:
                                st.download_button(
                                    label="📥 Baixar Resposta",
                                    data=str(answer),
                                    file_name="response_generated.txt",
                                    mime="text/plain",
                                )
                            with col2:
                                if st.button("🔄 Gerar Novamente"):
                                    st.experimental_rerun()

                        except Exception as e:
                            st.error(f"⚠️ Ocorreu um erro ao gerar a resposta: {str(e)}")

        # Rodapé
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #94a3b8; font-size: 14px; margin-top: 2rem;">
                <p>Text-to-SQL Converter v2.0 • Desenvolvido com I.A. e LangChain</p>
                <p style="font-size: 0.8rem;">© 2023 Todos os direitos reservados</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
