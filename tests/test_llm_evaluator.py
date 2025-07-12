import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from llm_evaluator import LLMEvaluator
from llm_model import LLMModel

@pytest.fixture
def dummy_model():
    return LLMModel(model_name="gpt-4", api_key="sk-fake-key-12345")

@pytest.mark.asyncio
async def test_evaluator_passes_on_high_score(dummy_model):
    # Mock OpenAI client inside the evaluator
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = """
Score: 9.0
Pass: Yes
Reason: Output fully satisfies the prompt.
""".strip()

    with patch("llm_model.AsyncOpenAI") as mock_client_class:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        evaluator = LLMEvaluator(model=dummy_model)
        passed, reason, score = await evaluator.evaluate("Test prompt", "Fake output")

        assert passed is True
        assert score == 9.0
        assert "fully satisfies" in reason

@pytest.mark.asyncio
async def test_evaluator_fails_on_low_score(dummy_model):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = """
Score: 5.5
Pass: No
Reason: The output was too shallow.
""".strip()

    with patch("llm_model.AsyncOpenAI") as mock_client_class:
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_client_class.return_value = mock_client

        evaluator = LLMEvaluator(model=dummy_model, threshold=7.0)
        passed, reason, score = await evaluator.evaluate("Test prompt", "Fake output")

        assert passed is False
        assert score == 5.5
        assert "shallow" in reason
