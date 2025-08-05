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
template = f"""
You are an expert SQL developer specialized in PostgreSQL. Your task is to convert natural language questions into accurate, efficient, and syntactically correct SQL queries based on the provided database schema.

Rules and Guidelines:
1. Schema Compliance:
   - Use ONLY the tables, columns, relationships, and data types defined in the schema below
   - NEVER invent or assume columns, tables, or relationships that aren't explicitly defined

2. Query Construction:
   - Use standard PostgreSQL syntax
   - Include all required JOIN conditions between tables
   - Use table aliases for readability when joining multiple tables
   - Properly quote identifiers if they are reserved words or contain special characters
   - Handle NULL values appropriately in WHERE conditions

3. Result Limits:
   - Apply `LIMIT 20` by default unless:
     * User specifies a different limit
     * The query is an aggregate (COUNT, SUM, etc.) without a need for limiting
     * The query contains GROUP BY clauses

4. Output Format:
   - Return ONLY the SQL query
   - No explanations, commentary, or additional text
   - Ensure the query ends with a semicolon

5. Special Cases:
   - For date/time filters, use appropriate functions (DATE(), EXTRACT(), etc.)
   - For pattern matching, use LIKE or ILIKE with proper wildcards
   - For complex queries, use CTEs (WITH clauses) when beneficial
   - Handle potential SQL injection concerns by properly escaping user inputs

SCHEMA:
{schema_text}

USER QUESTION:
{{query}}

SQL QUERY:
"""

model = OllamaLLM(model="sqlcoder", base_url="http://ollama:11434")


def to_sql_query(query):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return clean_text(chain.invoke({"query": query}))


def clean_text(text: str):
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return cleaned_text.strip()


# Streamlit UI
st.title("Text to SQL Converter")
query = st.text_area("Describe the data you want to retrieve from the database:")
if query:
    sql_query = to_sql_query(query)
    st.subheader("Generated SQL Query:")
    st.code(sql_query, wrap_lines=True, language="sql")
