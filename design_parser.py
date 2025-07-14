"""
design_parser.py

Author: Andrew Bathgate
Created: 2025-07-12

Description:
    DesignParser extracts raw text from local design documents (DOCX, or PDF).
    No network or OpenAI interaction.
"""

from pathlib import Path
from typing import IO

from docx import Document
from PyPDF2 import PdfReader


class DesignParser:
    def __init__(self, file_obj: IO, filename: str):
        """
        :param file_obj: An open file object (rb mode)
        :param filename: Original filename (used to determine type)
        """
        self.file_obj = file_obj
        self.filename = filename
        self.ext = Path(filename).suffix.lower()

        if self.ext not in [".pdf", ".docx", ".txt"]:
            raise ValueError(f"Unsupported file type: {self.ext}")

    def parse(self) -> str:
        """
        Extracts and returns all readable text from the document.
        """
        if self.ext == ".txt":
            return self.file_obj.read().decode("utf-8", errors="ignore")

        elif self.ext == ".docx":
            doc = Document(self.file_obj)
            return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

        elif self.ext == ".pdf":
            reader = PdfReader(self.file_obj)
            return "\n".join(page.extract_text() or "" for page in reader.pages)

        else:
            raise ValueError(f"Unsupported file type: {self.ext}")
