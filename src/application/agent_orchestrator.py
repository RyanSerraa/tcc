# agent_manager.py
import re
import pandas as pd
from langgraph.graph import END, START, StateGraph
from psycopg2.extras import Json, DictCursor
from src.application.run_query import RunQuery
from src.domain.state import State
from src.application.supervisor import Supervisor


class AgentManager:

    def __init__(
        self,
        connection,
        text_to_sql_agent,
        text_editor_agent,
        chart_editor_agent,
        web_search_agent,
        supervisor_agent,
        embeddings_model,
    ):
        self.connection = connection
        self.text_to_sql = text_to_sql_agent
        self.text_editor = text_editor_agent
        self.chart_editor = chart_editor_agent
        self.web_search = web_search_agent
        self.embeddings_model = embeddings_model
        self.departamentos_set = set(
            pd.read_csv("src/resources/depts.csv", header=None)[0].str.lower()
        )
        self.run_query = RunQuery(connection).run_query
        self.supervisor = supervisor_agent
        self.workflow = StateGraph(State)
        self._build_workflow()
        self.chain = self.workflow.compile()

    def _build_workflow(self):
        self.workflow.add_node("choose_chain", self.choose_chain)
        self.workflow.add_node("searchWeb", self.searchWeb)
        self.workflow.add_node("to_sql_query", self.to_sql_query)
        self.workflow.add_node("run_query", self.run_query)
        self.workflow.add_node("respondWithChart", self.respondWithChart)
        self.workflow.add_node("respondWithText", self.respondWithText)

        self.workflow.add_edge(START, "choose_chain")
        self.workflow.add_conditional_edges(
            "choose_chain",
            self.verifySupervisorAnswer,
            {"Yes": "to_sql_query", "No": "searchWeb"},
        )
        self.workflow.add_edge("to_sql_query", "run_query")
        self.workflow.add_conditional_edges(
            "run_query",
            self.hasChart,
            {"Yes": "respondWithChart", "No": "respondWithText"},
        )
        self.workflow.add_edge("respondWithText", END)
        self.workflow.add_edge("respondWithChart", END)
        self.workflow.add_edge("searchWeb", END)

    @staticmethod
    def clean_text(text: str) -> str:
        match = re.search(r"```sql(.*?)```", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r"SELECT .*?;", text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0).strip()
        return text.strip()

    def getContext(self, question: str, agente: str) -> str:
        query_emb = self.embeddings_model.embed_query(question)
        query_emb_vector = Json(query_emb)
        resultados = []

        with self.connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                SELECT pergunta, resposta
                FROM rag_documentos
                WHERE agente = %s
                ORDER BY embedding_pergunta <-> %s::vector
                LIMIT 5
                """,
                (agente, query_emb_vector),
            )
            resultados = cursor.fetchall()

        contexto = "\n".join(
            [
                f"{i+1}. Pergunta: {r['pergunta']}\n   Resposta: {r['resposta']}"
                for i, r in enumerate(resultados)
            ]
        )
        return contexto

    def choose_chain(self, state: State):
        question = state["question"].lower()
        hasFoundDept = any(dep.lower() in question for dep in self.departamentos_set)
        contexto = self.getContext(state["question"], "supervisor")
        prompt = (
            f"Contexto relevante:\n{contexto}\n"
            f'Pergunta do usuário: "{state["question"]}".\n'
            f"temDepartamentoEncontrado: {hasFoundDept}"
        )
        response = self.supervisor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        resposta_texto = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        return {"isEUA": resposta_texto.lower() == "sim"}
    
    def verifySupervisorAnswer(self, state: State):
        return "Yes" if state.get("isEUA") else "No"

    def hasChart(self, state: State):
        return "Yes" if "gráfico" in state.get("question", "").lower() else "No"

    def searchWeb(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\"."
        response = self.web_search.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = response.choices[0].message.content.strip() if response.choices else ""
        return {"answer": answer}

    def to_sql_query(self, state: State):
        cleanedQuestion = state["question"].replace(" em gráfico", "")
        contexto = self.getContext(state["question"], "text_to_sql")
        final_prompt = f"Pergunta do usuario:\n{cleanedQuestion}\n\nContexto relevante:\n{contexto}"
        response = self.text_to_sql.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": final_prompt}],
            extra_body={"include_retrieval_info": True},
        )
        content = "".join(choice.message.content for choice in response.choices)
        cleanedQuery = self.clean_text(content)
        return {"query": cleanedQuery}
    
    def respondWithChart(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\".\nDados: \"{state['result']}\".\n"
        response = self.chart_editor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"answer": answer}

    def respondWithText(self, state: State):
        prompt = f"Pergunta: \"{state['question']}\".\nDados: \"{state['result']}\".\n"
        response = self.text_editor.chat.completions.create(
            model="n/a",
            messages=[{"role": "user", "content": prompt}],
            extra_body={"include_retrieval_info": True},
        )
        answer = (
            response.choices[0].message.content.strip()
            if response.choices and hasattr(response.choices[0].message, "content")
            else ""
        )
        return {"answer": answer}
