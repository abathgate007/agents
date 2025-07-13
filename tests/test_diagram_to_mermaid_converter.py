import unittest
from unittest.mock import patch, MagicMock
from diagram_to_mermaid_converter import DiagramToMermaidConverter
import os
import tempfile
import base64

class TestDiagramToMermaidConverter(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and fake image file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.image_path = os.path.join(self.temp_dir.name, "test_diagram.png")
        self.output_path = os.path.join(self.temp_dir.name, "output.mmd")

        # Create a fake PNG file (valid header, minimal content)
        with open(self.image_path, "wb") as f:
            f.write(base64.b64decode(
                b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGBgAAAABAABJzQnCgAAAABJRU5ErkJggg=='
            ))

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("diagram_to_mermaid_converter.OpenAI")
    def test_convert_success(self, mock_openai_class):
        # Mock the OpenAI client and response
        mock_openai_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "graph TD;\nA --> B"
        mock_openai_instance.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_openai_instance

        # Run the converter
        converter = DiagramToMermaidConverter(model_name="gpt-4o")
        result = converter.convert(self.image_path, self.output_path)

        # Check the result
        self.assertIn("graph TD", result)

        # Check if file was written
        self.assertTrue(os.path.exists(self.output_path))
        with open(self.output_path, "r", encoding="utf-8") as f:
            written_content = f.read()
        self.assertEqual(written_content.strip(), "graph TD;\nA --> B")

        # Ensure the mock API was called
        mock_openai_instance.chat.completions.create.assert_called_once()

if __name__ == '__main__':
    unittest.main()
