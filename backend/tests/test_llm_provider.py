from app.llm.base import LLMProvider
from app.llm.config import LLMConfig
from app.llm.factory import create_llm_provider
from app.llm.mock_provider import MockLLMProvider


def test_mock_provider_implements_llm_provider():
    provider = MockLLMProvider()

    assert isinstance(provider, LLMProvider)


def test_mock_provider_returns_response():
    provider = MockLLMProvider()

    response = provider.generate("Create a story about a tiny star.")

    assert response == '{"status": "mock_response"}'


def test_factory_defaults_to_mock_provider():
    config = LLMConfig()

    provider = create_llm_provider(config)

    assert isinstance(provider, MockLLMProvider)


def test_factory_rejects_unknown_provider():
    config = LLMConfig()
    config.provider = "unknown"

    try:
        create_llm_provider(config)
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "Unsupported KADHAI LLM provider" in str(exc)