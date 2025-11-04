# test_agent_manager.py

from unittest.mock import Mock

import pytest

from src.application.agent_orchestrator import AgentManager
from src.domain.state import State


@pytest.fixture
def mock_agents():
    return {
        "text_to_sql_agent": Mock(),
        "insight_writer_agent": Mock(),
        "insight_drawer_agent": Mock(),
        "web_researcher_agent": Mock(),
        "supervisor_agent": Mock(),
        "embeddings": Mock(),
        "db": Mock(),
        "manager_agent": Mock(),
        "run_query_agent": Mock(),
        "insight_reasoner_agent": Mock(),
        "insight_editor_agent": Mock(),
    }


@pytest.fixture
def agent_manager(mock_agents):
    return AgentManager(
        db=mock_agents["db"],
        text_to_sql_agent=mock_agents["text_to_sql_agent"],
        insight_writer_agent=mock_agents["insight_writer_agent"],
        insight_drawer_agent=mock_agents["insight_drawer_agent"],
        web_researcher_agent=mock_agents["web_researcher_agent"],
        supervisor_agent=mock_agents["supervisor_agent"],
        embeddings=mock_agents["embeddings"],
        manager_agent=mock_agents["manager_agent"],
        run_query_agent=mock_agents["run_query_agent"],
        insight_reasoner_agent=mock_agents["insight_reasoner_agent"],
        insight_editor_agent=mock_agents["insight_editor_agent"],
    )


def test_verifySupervisorAnswer_yes(agent_manager):
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        manager_decision={},
        insight_writer_response="",
        insight_drawer_response="",
        insight_reasoner_response="",
        web_researcher_response="",
        insight_editor_response={},
    )
    assert agent_manager.verifySupervisorResponse(state) == "Yes"


def test_verifySupervisorAnswer_no(agent_manager):
    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=False,
        query="",
        result="",
        manager_decision={},
        insight_writer_response="",
        insight_drawer_response="",
        insight_reasoner_response="",
        web_researcher_response="",
        insight_editor_response={},
    )
    assert agent_manager.verifySupervisorResponse(state) == "No"


def test_workflow_nodes_exist(agent_manager):
    nodes = agent_manager.workflow.nodes
    expected_nodes = [
        "supervisor",
        "web_researcher",
        "to_sql_query",
        "run_query",
        "insight_writer",
        "insight_drawer",
        "insight_reasoner",
        "insight_editor",
        "manager",
    ]
    for node in expected_nodes:
        assert node in nodes


def test_workflow_edges_exist(agent_manager):
    edges = agent_manager.workflow.edges
    edge_list = [(from_node, to_node) for from_node, to_node in edges]
    assert ("__start__", "supervisor") in edge_list
    assert ("web_researcher", "__end__") in edge_list
    # Note: redator has conditional edges, not direct edges to __end__


def test_insight_editor_conditional_edge_logic(agent_manager):
    # Test when redoChart is True - should go to chartEditor
    state_redo_chart = State(
        question="Test question", insight_editor_response={"redoChart": True}
    )
    result = agent_manager.verifyInsightEditorResponse(state_redo_chart)
    assert result == "redoChart"

    state_no_redo = State(
        question="Test question", insight_editor_response={"redoChart": False}
    )
    result = agent_manager.verifyInsightEditorResponse(state_no_redo)
    assert result is None

    state_empty = State(question="Test question", insight_editor_response={})
    result = agent_manager.verifyInsightEditorResponse(state_empty)
    assert result is None
