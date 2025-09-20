from unittest.mock import MagicMock

from src.application.text_editor import TextEditor
from src.domain.state import State


def test_text_editor_respond():
    # Mock do agente
    mock_agent = MagicMock()
    mock_agent.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Resposta simulada"))
    ]

    text_editor = TextEditor(mock_agent)

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

    result = text_editor.respond(state)

    assert result["textEditor_response"] == "Resposta simulada"
    mock_agent.chat.completions.create.assert_called_once()
