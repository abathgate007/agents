"""
diagram_to_mermaid_converter.py

Author: Andrew Bathgate
Created: 2025-07-12
Description:
    This module defines the DiagramToMermaidConverter class, which takes
    an architecture diagram image and converts it into a Mermaid.js text
    diagram. Intended for use in automated security design review workflows.

    Future extensions may include support for OCR pipelines and vision-based
    LLMs for interpreting diagrams.

License: MIT (or insert appropriate license)
"""
import os
import base64
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

class DiagramToMermaidConverter:
    """
    Converts architecture diagram images into Mermaid diagram text.
    This class is designed to support LLM-based or OCR-assisted workflows.
    """

    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    def convert(self, image_path: str, output_path: str) -> str:
        """
        Converts the given architecture diagram image to a Mermaid-format diagram.

        :param image_path: Path to the input image.
        :param output_path: Path to save the Mermaid file.
        :return: Mermaid diagram as a string.
        """
        load_dotenv()

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            print("OpenAI API Key not set")
            return "Error: OpenAI API Key not set"

        print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")

        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            image_data_url = f"data:image/png;base64,{base64_image}"

        openai = OpenAI(api_key=openai_api_key)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that converts architecture diagrams into clean, accurate Mermaid diagrams."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Convert this diagram into Mermaid format."},
                    {"type": "image_url", "image_url": {"url": image_data_url}}
                ]
            }
        ]

        response = openai.chat.completions.create(model=self.model_name, messages=messages)
        mermaid = response.choices[0].message.content

        if mermaid:
            display(Markdown(mermaid))
            self.save_to_file(mermaid, output_path)

        return mermaid or ""

    def save_to_file(self, mermaid_text: str, output_path: str) -> None:
        """
        Saves the generated Mermaid text to a file.

        :param mermaid_text: The Mermaid-formatted string.
        :param output_path: File path to write the Mermaid text.
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(mermaid_text)
