import io
import pytest
from design_parser import DesignParser

def test_parse_txt_file_returns_expected_string():
    # Simulate a simple text file
    content = "This is a test document.\nWith multiple lines.\n"
    fake_file = io.BytesIO(content.encode("utf-8"))
    fake_filename = "test.txt"

    parser = DesignParser(file_obj=fake_file, filename=fake_filename)
    result = parser.parse()

    assert result == content