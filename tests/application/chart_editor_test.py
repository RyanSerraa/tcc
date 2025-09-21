from unittest.mock import MagicMock

from src.application.chart_editor import ChartEditor
from src.domain.state import State


def test_chart_editor_respond():
    mock_agent = MagicMock()
    mock_responnse_json = '{ "teste": "valor" }'
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_responnse_json))
    ]

    chart_editor = ChartEditor(mock_agent)

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

    result = chart_editor.respond(state)
    expected_response = {"teste": "valor"}

    assert result["chartEditor_response"] == expected_response
    mock_agent.chat.completions.create.assert_called_once()
