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
        "gerente_agent": Mock(),
        "run_query_agent": Mock(),
        "analista_agent": Mock(),
        "redator_agent": Mock(),
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
        gerente_agent=mock_agents["gerente_agent"],
        run_query_agent=mock_agents["run_query_agent"],
        analista_agent=mock_agents["analista_agent"],
        redator_agent=mock_agents["redator_agent"],
    )


def test_verifySupervisorAnswer_yes(agent_manager):
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        gerente_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        searchWeb_response="",
        redator_response={},
    )
    assert agent_manager.verifySupervisorResponse(state) == "Sim"


def test_verifySupervisorAnswer_no(agent_manager):
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=False,
        query="",
        result="",
        gerente_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        searchWeb_response="",
        redator_response={},
    )
    assert agent_manager.verifySupervisorResponse(state) == "Não"


def test_workflow_nodes_exist(agent_manager):
    nodes = agent_manager.workflow.nodes
    expected_nodes = [
        "supervisor",
        "searchWeb",
        "to_sql_query",
        "run_query",
        "textEditor",
        "chartEditor",
        "analista",
        "redator",
        "gerente",
    ]
    for node in expected_nodes:
        assert node in nodes


def test_workflow_edges_exist(agent_manager):
    edges = agent_manager.workflow.edges
    edge_list = [(from_node, to_node) for from_node, to_node in edges]
    assert ("__start__", "supervisor") in edge_list
    assert ("searchWeb", "__end__") in edge_list
    # Note: redator has conditional edges, not direct edges to __end__


def test_redator_conditional_edge_logic(agent_manager):
    # Test when redoChart is True - should go to chartEditor
    state_redo_chart = State(
        question="Test question", redator_response={"redoChart": True}
    )
    result = agent_manager.verifyRedatorResponse(state_redo_chart)
    assert result == "refazerGrafico"

    # Test when redoChart is False/None - should go to END
    state_no_redo = State(
        question="Test question", redator_response={"redoChart": False}
    )
    result = agent_manager.verifyRedatorResponse(state_no_redo)
    assert result is None

    # Test when redator_response is empty
    state_empty = State(question="Test question", redator_response={})
    result = agent_manager.verifyRedatorResponse(state_empty)
    assert result is None
