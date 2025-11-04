from unittest.mock import MagicMock

from src.application.insight_writer import InsightWriter
from src.domain.state import State


def test_text_editor_respond():
    # Mock do agente
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    insight_writer = InsightWriter(mock_agent)

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

    result = insight_writer.respond(state)

    assert result["insight_writer_response"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
