# test_agent_manager.py

from unittest.mock import Mock

import pytest

from src.application.agent_orchestrator import AgentManager
from src.domain.state import State


@pytest.fixture
def mock_agents():
    return {
        "text_to_sql_agent": Mock(),
        "text_editor_agent": Mock(),
        "chart_editor_agent": Mock(),
        "web_search_agent": Mock(),
        "supervisor_agent": Mock(),
        "embeddings": Mock(),
        "connection": Mock(),
    }


@pytest.fixture
def agent_manager(mock_agents):
    return AgentManager(
        connection=mock_agents["connection"],
        text_to_sql_agent=mock_agents["text_to_sql_agent"],
        text_editor_agent=mock_agents["text_editor_agent"],
        chart_editor_agent=mock_agents["chart_editor_agent"],
        web_search_agent=mock_agents["web_search_agent"],
        supervisor_agent=mock_agents["supervisor_agent"],
        embeddings=mock_agents["embeddings"],
    )


def test_verifySupervisorAnswer_yes(agent_manager):
    state = State({"isEUA": True})
    assert agent_manager.verifySupervisorAnswer(state) == "Yes"


def test_verifySupervisorAnswer_no(agent_manager):
    state = State({"isEUA": False})
    assert agent_manager.verifySupervisorAnswer(state) == "No"


def test_hasChart_yes(agent_manager):
    state = State(
        {
            "question": "Pode gerar um gráfico com a principal causa de morte na california em encontros fatais?",
            "isEUA": True,
            "query": "",
            "result": "",
            "answer": "",
        }
    )
    assert agent_manager.hasChart(state) == "Yes"


def test_hasChart_no(agent_manager):
    state = State({"question": "Qual é a previsão do tempo?"})
    assert agent_manager.hasChart(state) == "No"


def test_workflow_nodes_exist(agent_manager):
    nodes = agent_manager.workflow.nodes
    expected_nodes = [
        "supervisor",
        "searchWeb",
        "to_sql_query",
        "run_query",
        "respondWithChart",
        "respondWithText",
    ]
    for node in expected_nodes:
        assert node in nodes


def test_workflow_edges_exist(agent_manager):
    edges = agent_manager.workflow.edges
    edge_list = [(from_node, to_node) for from_node, to_node in edges]
    assert ("__start__", "supervisor") in edge_list
    assert ("respondWithText", "__end__") in edge_list
    assert ("respondWithChart", "__end__") in edge_list

