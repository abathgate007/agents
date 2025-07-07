import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from default_evaluation_routine import DefaultEvaluationRoutine
from llm_model import LLMModel
from evaluated_output import EvaluatedOutput

@pytest.mark.asyncio
async def test_run_returns_passing_output():
    dummy_model = LLMModel(model_name="fake-model", api_key="fake-api-key")

    fake_output = EvaluatedOutput(
    model_name=dummy_model.model_name,
    output_content="Generated content",
    final_score=9.0,
    passes=True,
    evaluation_reason="Looks great",
    attempts=1,
)

    with patch.object(DefaultEvaluationRoutine, "_generate_and_evaluate", new=AsyncMock(return_value=fake_output)):
        routine = DefaultEvaluationRoutine(models=[dummy_model], max_attempts=1)
        result = await routine.run(prompt="Do a fake review")

        assert result is not None
        assert isinstance(result, EvaluatedOutput)
        assert result.passes is True
        assert result.final_score >= 7.0
