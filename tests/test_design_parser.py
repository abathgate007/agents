import io
import pytest
from unittest.mock import MagicMock, patch
from design_parser import DesignParser

@patch("design_parser.OpenAI")
def test_parse_returns_expected_string(mock_openai_class):
    # Set up a fake file (e.g., DOCX or PDF)
    fake_file = io.BytesIO(b"Fake binary content")
    fake_filename = "test_design.pdf"
    fake_api_key = "sk-fake-key"

    # Mock the OpenAI client and its methods
    mock_client_instance = MagicMock()
    mock_openai_class.return_value = mock_client_instance

    # Simulate file upload return
    mock_file_obj = MagicMock()
    mock_file_obj.id = "file-fake-id"
    mock_client_instance.files.create.return_value = mock_file_obj

    # Simulate LLM response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Parsed document text here."))]
    mock_client_instance.chat.completions.create.return_value = mock_response

    # Create and run parser
    parser = DesignParser(file_obj=fake_file, filename=fake_filename, api_key=fake_api_key)
    result = parser.parse()

    # Assert correct result
    assert result == "Parsed document text here."

    # Assert file was uploaded
    mock_client_instance.files.create.assert_called_once()

    # Assert model was called with correct file reference
    args, kwargs = mock_client_instance.chat.completions.create.call_args
    assert kwargs["model"] == "gpt-4o"

    messages = kwargs["messages"]
    content_blocks = messages[0]["content"]

    assert any(
        block.get("image_url", {}).get("url") == "file-id:file-fake-id"
        for block in content_blocks
    )

