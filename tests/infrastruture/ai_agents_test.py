# tests/infrastructure/test_agents.py
from unittest.mock import MagicMock, patch

from openai import OpenAI

from src.infrastructure.ai_agents import Agents


def test_load_agent_success():
    mock_client = MagicMock(spec=OpenAI)

    with patch(
        "src.infrastructure.ai_agents.OpenAI", return_value=mock_client
    ) as mock_openai:
        client = Agents.load_agent("http://fake-endpoint", "fake-key")
        mock_openai.assert_called_once_with(
            base_url="http://fake-endpoint/api/v1", api_key="fake-key"
        )
        assert client == mock_client


def test_load_agent_invalid_parameters():
    # Fake OpenAI que lança ValueError se base_url ou api_key estiverem vazios
    def fake_openai(*args, **kwargs):
        if not kwargs.get("base_url") or not kwargs.get("api_key"):
            raise ValueError("Parâmetros inválidos")
        return MagicMock(spec=OpenAI)


def test_load_agent_cached():
    mock_client = MagicMock(spec=OpenAI)

    # Limpa cache do Streamlit antes do teste
    Agents.load_agent.clear()

    with patch(
        "src.infrastructure.ai_agents.OpenAI", return_value=mock_client
    ) as mock_openai:
        client1 = Agents.load_agent("http://fake-endpoint", "fake-key")
        client2 = Agents.load_agent("http://fake-endpoint", "fake-key")

        assert client1 is client2
        mock_openai.assert_called_once()  # OpenAI só instanciado 1 vez
