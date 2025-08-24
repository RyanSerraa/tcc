import re
import os
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Configuração inicial
load_dotenv()
st.set_page_config(
    page_title="Text-to-SQL Converter",
    page_icon=":database:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Carrega o conteúdo do schema externo
@st.cache_resource
def load_schema():
    with open("schema.txt", "r") as f:
        return f.read()


schema_text = load_schema()

prompt = """
You are an SQL query generator for PostgreSQL.

You must use exclusively the following views to answer all questions:

VIEW VFatalEncountersDetails (
    date_of_death DATE,
    cause_of_death TEXT,             -- possible values: 'UNKNOWN', other short cause of death names
    weapon_used TEXT,                -- possible values: 'UNKNOWN', other short weapon names
    police_department TEXT,
    threat_status TEXT,              -- 'ATTACK', 'OTHER', 'UNKNOWN'
    flee_status TEXT,                -- 'VEHICLE', 'FOOT', 'UNKNOWN', 'NOT FLEEING'
    is_police_wearing_camera BOOLEAN,
    victim_gender TEXT,              -- 'MALE', 'FEMALE', 'UNKNOWN', 'OTHERS'
    victim_race TEXT,                -- 'WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS'
    victim_type TEXT,                -- 'POLICE', 'VICTIM', 'CRIMINAL'
    victim_age_range TEXT,
    state TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)

VIEW VShootingDetails (
    date_of_shooting DATE,
    cause_of_death TEXT,             -- possible values: 'UNKNOWN', other short cause of death names
    weapon_used TEXT,                -- possible values: 'UNKNOWN', other short weapon names
    threat_status TEXT,              -- 'ATTACK', 'OTHER', 'UNKNOWN'
    flee_status TEXT,                -- 'VEHICLE', 'FOOT', 'UNKNOWN', 'NOT FLEEING'
    is_police_wearing_camera BOOLEAN,
    victim_gender TEXT,              -- 'MALE', 'FEMALE', 'UNKNOWN', 'OTHERS'
    victim_race TEXT,                -- 'WHITE', 'BLACK', 'ASIAN', 'UNKNOWN', 'HISPANIC', 'OTHERS'
    victim_type TEXT,                -- 'POLICE', 'VICTIM', 'CRIMINAL'
    victim_age_range TEXT,
    state TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)

VIEW VDeathPoliceDetails (
    date_of_death DATE,
    cause_of_death TEXT,             -- possible values: 'UNKNOWN', other short cause of death names
    police_department TEXT,
    police_type TEXT,                -- possible value: 'POLICE'
    state TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)

VIEW VCrimeDetails (
    date_of_crime DATE,
    crime_name TEXT,
    weapon_used TEXT,
    criminal_gender TEXT,
    criminal_race TEXT,
    criminal_type TEXT,
    criminal_age_range TEXT,
    state TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)

VIEW VArrestDetails (
    date_of_arrest DATE,
    crime_name TEXT,
    drug_name TEXT,
    weapon_used TEXT,
    criminal_gender TEXT,
    criminal_race TEXT,
    criminal_type TEXT,
    criminal_age_range TEXT,
    state TEXT,
    city TEXT,
    latitude NUMERIC,
    longitude NUMERIC
)

Mandatory rules:
1. Always return only valid PostgreSQL SQL code, with no extra text, explanations, or comments.
2. Do not use SELECT * — always specify the exact columns needed.
3. Use clear aliases for tables or columns when needed.
4. For date filters, use the 'YYYY-MM-DD' format or PostgreSQL date functions.
5. When filtering by categorical values (such as gender, race, threat_status, police_type), use the exact values listed in the schema.
6. You may use CTEs (Common Table Expressions) when needed to improve query readability.

Examples:
Question: "List the 10 cities with the highest number of female victims in fatal encounters."
Answer:
SELECT city, COUNT(*) AS total_cases
FROM VFatalEncountersDetails
WHERE victim_gender = 'FEMALE'
GROUP BY city
ORDER BY total_cases DESC
LIMIT 10;

Question: "Show the number of cases of victims fleeing on foot by state in fatal encounters."
Answer:
SELECT state, COUNT(*) AS total_cases
FROM VFatalEncountersDetails
WHERE flee_status = 'FOOT'
GROUP BY state
ORDER BY total_cases DESC;

Question: "List the top 5 cities with the most shootings involving male victims."
Answer:
SELECT city, COUNT(*) AS total_shootings
FROM VShootingDetails
WHERE victim_gender = 'MALE'
GROUP BY city
ORDER BY total_shootings DESC
LIMIT 5;

Question: "Count the number of shootings where police were wearing body cameras."
Answer:
SELECT COUNT(*) AS total_shootings_with_cameras
FROM VShootingDetails
WHERE is_police_wearing_camera = TRUE;

Question: "List police departments with more than 10 deaths of police officers."
Answer:
SELECT police_department, COUNT(*) AS total_deaths
FROM VDeathPoliceDetails
GROUP BY police_department
HAVING COUNT(*) > 10
ORDER BY total_deaths DESC;

Question: "Show the number of police deaths by state."
Answer:
SELECT state, COUNT(*) AS total_deaths
FROM VDeathPoliceDetails
GROUP BY state
ORDER BY total_deaths DESC;

Question: "Tell me the main crime by state."
Answer:
WITH RankedCrimes AS (
    SELECT
        state,
        crime_name,
        COUNT(*) AS total_crimes,
        ROW_NUMBER() OVER(PARTITION BY state ORDER BY COUNT(*) DESC) AS rn
    FROM
        VCrimeDetails
    WHERE
        state IS NOT NULL AND crime_name IS NOT NULL
    GROUP BY
        state,
        crime_name
)
SELECT
    state,
    crime_name,
    total_crimes
FROM
    RankedCrimes
WHERE
    rn = 1
ORDER BY
    state;

Question: "What are the top 5 crimes by race in arrests?"
Answer:
WITH RankedArrests AS (
    SELECT
        criminal_race,
        crime_name,
        COUNT(*) AS total_arrests,
        ROW_NUMBER() OVER(PARTITION BY criminal_race ORDER BY COUNT(*) DESC) AS rn
    FROM
        VArrestDetails
    WHERE
        criminal_race IS NOT NULL AND crime_name IS NOT NULL
    GROUP BY
        criminal_race,
        crime_name
)
SELECT
    criminal_race,
    crime_name,
    total_arrests
FROM
    RankedArrests
WHERE
    rn <= 5
ORDER BY
    criminal_race,
    total_arrests DESC;

Question: "List the number of arrests by criminal gender and the top 3 cities for each gender."
Answer:
WITH RankedCities AS (
    SELECT
        criminal_gender,
        city,
        COUNT(*) AS total_arrests,
        ROW_NUMBER() OVER(PARTITION BY criminal_gender ORDER BY COUNT(*) DESC) AS rn
    FROM
        VArrestDetails
    WHERE
        criminal_gender IS NOT NULL AND city IS NOT NULL
    GROUP BY
        criminal_gender,
        city
)
SELECT
    criminal_gender,
    city,
    total_arrests
FROM
    RankedCities
WHERE
    rn <= 3
ORDER BY
    criminal_gender,
    total_arrests DESC;

Question: "Show the most common crime in each city, where the criminal is of 'BLACK' race."
Answer:
WITH RankedCrimes AS (
    SELECT
        city,
        crime_name,
        COUNT(*) AS total_crimes,
        ROW_NUMBER() OVER(PARTITION BY city ORDER BY COUNT(*) DESC) AS rn
    FROM
        VCrimeDetails
    WHERE
        city IS NOT NULL AND crime_name IS NOT NULL AND criminal_race = 'BLACK'
    GROUP BY
        city,
        crime_name
)
SELECT
    city,
    crime_name,
    total_crimes
FROM
    RankedCrimes
WHERE
    rn = 1
ORDER BY
    city;
"""


# Inicializa o modelo
@st.cache_resource
def load_agent():
    base_url = os.getenv("TEXT_TO_SQL_AGENT_ENDPOINT") + "/api/v1"
    api_key = os.getenv("TEXT_TO_SQL_API_KEY")
    client = OpenAI(base_url=base_url, api_key=api_key)
    return client


client = load_agent()


def to_sql_query(user_query: str) -> str:
    final_prompt = f"{prompt}\n\nQUESTION:\n{user_query}\n\nSQL:"

    response = client.chat.completions.create(
        model="n/a",  # ou outro modelo se você tiver
        messages=[{"role": "user", "content": final_prompt}],
        extra_body={"include_retrieval_info": True},
        max_tokens=512,
        temperature=0,
    )

    # Extrai o conteúdo do retorno
    content = ""
    for choice in response.choices:
        content += choice.message.content

    return clean_text(content)


def clean_text(text: str) -> str:
    # Se houver bloco de código SQL, extrai somente ele
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"SELECT .*?;", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return text.strip()


# CSS personalizado com tema escuro
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
        <h1>Text-to-SQL Converter</h1>
        <p>Transforme suas perguntas em consultas SQL profissionais</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Seção de cards de recursos
st.markdown("### Principais Recursos")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(
        """
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
        <a href="http://161.35.61.141:3000/public/dashboard/95ac4087-b5b8-45af-9a87-668741ffa295" class="card" style="display: block; text-decoration: none;">
            <div class="card-icon"><i class="fas fa-handcuffs card-icon"></i></div>
            <h3>Arrests</h3>
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
            <h3>Fatal Encounters</h3>
            <p>Casos com resultados fatais e análises de circunstâncias</p>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <a href="http://161.35.61.141:3000/public/dashboard/a81a61ba-5c63-4e3f-b6a0-e3efba33feae" class="card" style="display: block; text-decoration: none;">
            <div class="card-icon"><i class="fas fa-heart-broken card-icon"></i></div>
            <h3>Police Deaths</h3>
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
            <h3>Shootings</h3>
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
            <p>Inclua detalhes como tabelas, campos e condições desejadas</p>
        </div>

        <div class="feature-card">
            <h4>Exemplo de consulta</h4>
            <p>"Liste todos os clientes ativos que compraram mais de 3 produtos no último mês"</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_right:
    st.markdown(
        """
        <div class="info-box">
            💡 Descreva em linguagem natural quais dados você precisa do banco de dados.
            Nosso sistema irá gerar a consulta SQL correspondente automaticamente.
        </div>
    """,
        unsafe_allow_html=True,
    )

    query = st.text_area(
        "Descreva sua necessidade de dados:",
        placeholder="Ex: Obter todos os clientes que fizeram compras acima de R$1000 no último mês, ordenados por valor decrescente",
        label_visibility="collapsed",
    )

    if st.button("Gerar Consulta SQL", type="primary"):
        if not query:
            st.warning("Por favor, insira uma descrição antes de gerar o SQL.")
        else:
            with st.spinner("🧠 Processando sua solicitação..."):
                try:
                    sql_query = to_sql_query(query, schema_text)

                    st.markdown("### 🔍 Resultado")
                    st.code(sql_query, language="sql")

                    # Botões de ação
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.download_button(
                            label="📥 Baixar SQL",
                            data=sql_query,
                            file_name="query_generated.sql",
                            mime="text/plain",
                        )
                    with col2:
                        if st.button("🔄 Gerar Novamente"):
                            st.experimental_rerun()

                except Exception as e:
                    st.error(f"⚠️ Ocorreu um erro ao gerar a consulta: {str(e)}")

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 14px; margin-top: 2rem;">
        <p>Text-to-SQL Converter v2.0 • Desenvolvido com Ollama e LangChain</p>
        <p style="font-size: 0.8rem;">© 2023 Todos os direitos reservados</p>
    </div>
""",
    unsafe_allow_html=True,
)
