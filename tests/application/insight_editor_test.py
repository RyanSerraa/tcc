from unittest.mock import MagicMock

from src.application.insight_editor import InsightEditor
from src.domain.state import State


def test_redator_respond():
    mock_agent = MagicMock()
    # Mock de uma resposta JSON válida
    mock_response_json = '{"final_textual_response": "Resposta simulada", "chart": null, "redoChart": false}'
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content=mock_response_json))
    ]

    insight_editor = InsightEditor(mock_agent)

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

    result = insight_editor.respond(state)

    expected_response = {
        "final_textual_response": "Resposta simulada",
        "chart": None,
        "redoChart": False,
    }
    assert result["insight_editor_response"] == expected_response
    mock_agent.chat.completions.create.assert_called_once()
