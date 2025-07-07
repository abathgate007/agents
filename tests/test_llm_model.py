import pytest
from llm_model import LLMModel

def test_valid_llm_model():
    model = LLMModel(model_name="gpt-4", api_key="sk-test-1234567890")
    assert model.model_name == "gpt-4"
    assert model.api_key.startswith("sk-")

def test_invalid_short_api_key():
    with pytest.raises(ValueError):
        LLMModel(model_name="gpt-4", api_key="123")

def test_missing_model_name():
    with pytest.raises(ValueError):
        LLMModel(model_name="", api_key="sk-valid-123456")

def test_short_id_output():
    model = LLMModel(model_name="gpt-4", api_key="sk-abcdefgh123456")
    assert model.short_id().startswith("sk-ab")