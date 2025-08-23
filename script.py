import psycopg2
import requests

# Função para chamar agentes DigitalOcean
def call_agent(agent_endpoint, api_key, prompt):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(agent_endpoint, json={"input": prompt}, headers=headers)
    return response.json()["output"]

# Conexão com o banco de dados
def execute_sql(sql):
    conn = psycopg2.connect(
        host="dev-police-analytic-11477.j77.aws-us-east-1.cockroachlabs.cloud",
        database="defaultdb",
        user="metabase",
        password="aAQdwnmo2618q"
    )
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# Usuário faz uma pergunta
user_input = "Me dê os produtos mais vendidos no último mês"

# 1️⃣ Business Analysis Agent interpreta intenção
baa_prompt = f"Transforme essa pergunta em um objetivo SQL: {user_input}"
baa_interpretation = call_agent(baa_endpoint, baa_api_key, baa_prompt)

# 2️⃣ Text-to-SQL Agent gera SQL
sql_query = call_agent(t2s_endpoint, t2s_api_key, baa_interpretation)

# 3️⃣ Executa SQL no banco de dados
results = execute_sql(sql_query)

# 4️⃣ Business Analysis Agent analisa os resultados
final_prompt = f"Analise os seguintes dados: {results}"
final_analysis = call_agent(baa_endpoint, baa_api_key, final_prompt)

print(final_analysis)
