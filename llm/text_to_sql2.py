import os
import streamlit as st
import re
import pandas as pd
import psycopg2
import base64
from openai import OpenAI
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from psycopg2.extras import DictCursor, Json
from langchain_huggingface import HuggingFaceEmbeddings


df = pd.read_csv("depts.csv", header=None)
departamentos_set = set(df[0].str.lower())

embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# Graph state
class State(TypedDict):
    question: str
    isEUA: bool
    query: str
    result: str
    answer: str


load_dotenv()

st.set_page_config(
    page_title="Text-to-SQL Converter",
    page_icon=":database:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    return psycopg2.connect(DATABASE_URL)


def load_file(file):
    with open(file, "r") as f:
        return f.read()


schema_text = load_file("schema.txt")

prompt_text_to_sql = load_file("prompt_text_to_sql.txt")
prompt_supervisor = load_file("prompt_supervisor.txt")
prompt_textEditor = load_file("prompt_text_editor.txt")
prompt_chartEditor = load_file("prompt_chart_editor.txt")
prompt_webSearch = load_file("prompt_web_search.txt")


@st.cache_resource
def load_agent(agentEndpoint, apiKey):
    base_url = agentEndpoint + "/api/v1"
    api_key = apiKey
    client = OpenAI(base_url=base_url, api_key=api_key)
    return client


text_to_sql = load_agent(
    os.getenv("TEXT_TO_SQL_AGENT_ENDPOINT"), os.getenv("TEXT_TO_SQL_API_KEY")
)
textEditor_model = load_agent(
    os.getenv("TEXT_EDITOR_AGENT_ENDPOINT"), os.getenv("TEXT_EDITOR_API_KEY")
)
chartEditor_model = load_agent(
    os.getenv("CHART_EDITOR_AGENT_ENDPOINT"), os.getenv("CHART_EDITOR_API_KEY")
)
webSearch_model = load_agent(
    os.getenv("WEB_SEARCH_AGENT_ENDPOINT"), os.getenv("WEB_SEARCH_API_KEY")
)
supervisor_model = load_agent(
    os.getenv("SUPERVISOR_AGENT_ENDPOINT"), os.getenv("SUPERVISOR_API_KEY")
)


def getContext(question: str, agente: str) -> str:
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    query_emb = embeddings_model.embed_query(question)
    query_emb_vector = Json(query_emb)
    resultados = []
    cursor.execute(
        """
        SELECT pergunta, resposta
        FROM rag_documentos
        WHERE agente = %s
        ORDER BY embedding_pergunta <-> %s::vector
        LIMIT 3
        """,
        (
            agente,
            query_emb_vector,
        ),
    )
    print("consultando o banco de dados...")
    resultados = cursor.fetchall()
    conn.close()

    contexto = "\n".join(
        [
            f"{i+1}. Pergunta: {r['pergunta']}\n   Resposta: {r['resposta']}"
            for i, r in enumerate(resultados)
        ]
    )
    return contexto


def choose_chain(state: State):
    print("Escolhendo a cadeia...")
    question = state["question"].lower()
    hasFoundDept = any(dep.lower() in question for dep in departamentos_set)
    contexto = getContext(state["question"], "supervisor")
    prompt = (
        f"Contexto relevante:\n{contexto}\n"
        f'Pergunta do usuário: "{state["question"]}".\n'
        f"temDepartamentoEncontrado: {hasFoundDept}"
    )
    print("Prompt - Supervisor:", prompt)
    response = supervisor_model.chat.completions.create(
        model="n/a",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"include_retrieval_info": True},
    )
    print("response - Supervisor:", response.choices[0].message.content)
    resposta_texto = (
        response.choices[0].message.content.strip() if response.choices else ""
    )
    if resposta_texto.lower() == "sim":
        return {"isEUA": True}
    return {"isEUA": False}


def verifySupervisorAnswer(state: State):
    if state["isEUA"] == True:
        return "Yes"
    return "No"


def hasChart(state: State):
    if "gráfico" in state["question"]:
        return "Yes"
    return "No"


def searchWeb(state: State):
    print("Buscando na web...")
    prompt = f"Pergunta: \"{state['question']}\"."
    response = webSearch_model.chat.completions.create(
        model="n/a",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"include_retrieval_info": True},
    )
    print("response - searchWeb:", response.choices[0].message.content)
    answer = response.choices[0].message.content.strip() if response.choices else ""
    return {"answer": answer}


def clean_text(text: str) -> str:
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"SELECT .*?;", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return text.strip()


def to_sql_query(state: State):
    print("Convertendo para SQL...")
    cleanedQuestion = state["question"].replace(" em gráfico", "")
    contexto = getContext(state["question"], "text_to_sql")
    print("Contexto:", contexto)
    final_prompt = (
        f"Pergunta do usuario:\n{cleanedQuestion}\n\nContexto relevante:\n{contexto}"
    )
    response = text_to_sql.chat.completions.create(
        model="n/a",
        messages=[{"role": "user", "content": final_prompt}],
        extra_body={"include_retrieval_info": True},
    )
    content = ""
    for choice in response.choices:
        content += choice.message.content

    cleanedQuery = clean_text(content)
    print("Generated SQL Query:", cleanedQuery)
    return {"query": cleanedQuery}


def run_query(sql_query: dict):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            query = sql_query["query"].strip()
            cursor.execute(query)

            if query.lower().startswith("select"):
                rows = cursor.fetchall()
                result = [dict(row) for row in rows]  # Converte para lista de dicts
                return {"result": result}
            else:
                conn.commit()
                return {"affected_rows": cursor.rowcount}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()


def respondWithChart(state: State):
    print("Gerando gráfico...")
    prompt = f"Pergunta: \"{state['question']}\".\n" f"Dados: \"{state['result']}\".\n"

    # Geração da imagem via modelo
    response = chartEditor_model.chat.completions.create(
        model="n/a",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"include_retrieval_info": True},
    )
    print("response - respondWithChart:", response.choices[0].message.content)
    if response.choices and hasattr(response.choices[0].message, "content"):
        answer = response.choices[0].message.content.strip()
    else:
        answer = ""
    return {"answer": answer}


def respondWithText(state: State):
    print("Gerando resposta textual...")
    prompt = f"Pergunta: \"{state['question']}\".\n" f"Dados: \"{state['result']}\".\n"
    response = textEditor_model.chat.completions.create(
        model="n/a",
        messages=[{"role": "user", "content": prompt}],
        extra_body={"include_retrieval_info": True},
    )
    print("response - respondWithText:", response.choices[0].message.content)
    if response.choices and hasattr(response.choices[0].message, "content"):
        answer = response.choices[0].message.content.strip()
    else:
        answer = ""
    return {"answer": answer}


workflow = StateGraph(State)

workflow.add_node("choose_chain", choose_chain)
workflow.add_node("searchWeb", searchWeb)
workflow.add_node("to_sql_query", to_sql_query)
workflow.add_node("run_query", run_query)
workflow.add_node("respondWithChart", respondWithChart)
workflow.add_node("respondWithText", respondWithText)

workflow.add_edge(START, "choose_chain")
workflow.add_conditional_edges(
    "choose_chain", verifySupervisorAnswer, {"Yes": "to_sql_query", "No": "searchWeb"}
)
workflow.add_edge("to_sql_query", "run_query")
workflow.add_conditional_edges(
    "run_query", hasChart, {"Yes": "respondWithChart", "No": "respondWithText"}
)
workflow.add_edge("respondWithText", END)
workflow.add_edge("respondWithChart", END)
workflow.add_edge("searchWeb", END)

chain = workflow.compile()
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
                    answer = chain.invoke({"question": query})["answer"]

                    st.markdown("### 🔍 Resultado")
                    st.write(answer)

                    # Botões de ação
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.download_button(
                            label="📥 Baixar Resposta",
                            data=answer,
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
