import re
import os
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# Carrega o conteúdo do schema externo
with open("schema.txt", "r") as f:
    schema_text = f.read()

# Prompt base com placeholder para schema e query
template = """
You are a SQL generator. You MUST output only the SQL query—no explanations, no markdown, no commentary.

SCHEMA:
{schema}

QUESTION:
{query}

SQL:
"""


model = OllamaLLM(model="deepseek-r1:7b", base_url="http://ollama:11434")


def to_sql_query(query, schema):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return clean_text(chain.invoke({"query": query, "schema": schema}))


def clean_text(text: str) -> str:
    # Se houver bloco de código SQL, extrai somente ele
    match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"SELECT .*?;", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return text.strip()


# Streamlit UI
st.title("Text to SQL Converter")
query = st.text_area("Describe the data you want to retrieve from the database:")
if query:
    sql_query = to_sql_query(query, schema_text)
    st.subheader("Generated SQL Query:")
    st.code(sql_query, wrap_lines=True, language="sql")
