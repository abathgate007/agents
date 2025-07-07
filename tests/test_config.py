import os
import pytest
from config import load_config, Config

def test_valid_config(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-valid-openai-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "claude-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "gg")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ds1")
    monkeypatch.setenv("GROQ_API_KEY", "grqk")

    config = load_config()

    assert config.openai_api_key.startswith("sk-")
    assert config.anthropic_api_key == "claude-key"
    assert config.google_api_key == "gg"
    assert config.deepseek_api_key == "ds1"
    assert config.groq_api_key == "grqk"

def test_missing_openai_key_raises(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError) as excinfo:
        load_config()
    assert "OPENAI_API_KEY is required" in str(excinfo.value)

def test_optional_keys_can_be_none(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-ok")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    config = load_config()
    assert config.anthropic_api_key is None
    assert config.google_api_key is None