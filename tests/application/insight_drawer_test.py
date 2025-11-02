from unittest.mock import MagicMock

from src.application.insight_drawer import InsightDrawer
from src.domain.state import State


def test_chart_editor_respond():
    mock_agent = MagicMock()
    mock_responnse_json = '{ "teste": "valor" }'
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_responnse_json))
    ]

    insight_drawer = InsightDrawer(mock_agent)

    state = State(
        question="Qual é a capital da Califórnia?",
        isEUA=True,
        query="",
        result="",
        manager_decision={},
        textEditor_response="",
        chartEditor_response="",
        analista_response="",
        web_researcher_response="",
        redator_response={},
    )

    result = insight_drawer.respond(state)
    expected_response = {"teste": "valor"}

    assert result["chartEditor_response"] == expected_response
    mock_agent.chat.completions.create.assert_called_once()
