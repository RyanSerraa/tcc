from unittest.mock import MagicMock

from src.application.session_manager import SessionManager


def test_consultar_dados_sucesso():
    # Mock do AgentManager
    mock_agent_manager = MagicMock()
    mock_agent_manager.chain.invoke.return_value = {
        "redator_response": {
            "final_textual_response": "Resultado simulado",
            "chart": None,
        },
        "web_researcher_response": None,
        "result": None,
    }

    qm = SessionManager(mock_agent_manager)
    result = qm.consultar_dados(
        "Qual a principal causa de morte por arma de fogo na Califórnia?"
    )

    assert result == {
        "success": True,
        "text_response": "Resultado simulado",
        "web_researcher_response": None,
        "chart_response": None,
    }
    mock_agent_manager.chain.invoke.assert_called_once()
    # Verificar se foi chamado com um objeto State com a pergunta correta
    called_args = mock_agent_manager.chain.invoke.call_args[0][0]
    assert (
        called_args.question
        == "Qual a principal causa de morte por arma de fogo na Califórnia?"
    )


def test_consultar_dados_erro():
    mock_agent_manager = MagicMock()
    mock_agent_manager.chain.invoke.side_effect = Exception("Falha na chain")

    qm = SessionManager(mock_agent_manager)
    result = qm.consultar_dados("Pergunta qualquer")

    assert result == {"success": False, "error": "Falha na chain"}
