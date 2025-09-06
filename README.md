# 📊 CrimeFlow

## 📖 Visão Geral  

O **CrimeFlow** é um sistema de análise de dados criminais dos Estados Unidos.  
Ele permite consultas e geração de gráficos a partir de informações como:  
- Crimes registrados  
- Prisões  
- Policiais mortos  
- Tiroteios  
- Encontros fatais  

Além dos gráficos do **Metabase**, o sistema conta com **agents** baseados em **LLMs** para que o usuário possa interagir em **linguagem natural** com a base de dados.

## ⚙️ Tecnologias Utilizadas  

- **Linguagem:** Python 3.11  
- **Frameworks / Bibliotecas:** LangGraph, psycopg2, pandas, Streamlit  
- **Banco de Dados:** Cockroachdb  
- **Infraestrutura:** Docker, Docker Compose, Makefile  
- **Testes:** Pytest  

---

## 🚀 Configuração e Execução  

### 1. Pré-requisitos  

- Docker  
- Docker Compose  
- Make  
- Python 3.11  

### 2. Passos de Execução  

```bash
# Clonar o repositório
git clone git@github.com:RyanSerraa/tcc.git
cd crimeflow

make compose-up

make exec-llm

make llm-run
```
