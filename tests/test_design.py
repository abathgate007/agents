# Author: Andrew Bathgate | Date: 2025-06-26
import pytest
from design import Design

def test_add_text_document():
    d = Design()
    d.add_text("This is a requirements document.")
    assert len(d.text_docs) == 1
    assert d.text_docs[0] == "This is a requirements document."

def test_add_mermaid_diagram():
    d = Design()
    diagram = "graph TD; A-->B;"
    d.add_mermaid(diagram)
    assert len(d.mermaid_diagrams) == 1
    assert d.mermaid_diagrams[0] == diagram

def test_summary_counts_correctly():
    d = Design()
    d.add_text("Text A")
    d.add_mermaid("graph TD; A-->B;")
    d.add_mermaid("graph TD; B-->C;")
    summary = d.summary()
    assert "1 text docs" in summary
    assert "2 mermaid diagrams" in summary

def test_get_all_content_combines_both():
    d = Design()
    d.add_text("Doc1")
    d.add_text("Doc2")
    d.add_mermaid("graph TD; A-->B;")
    content = d.get_all_content()
    assert "Doc1" in content
    assert "Doc2" in content
    assert "graph TD; A-->B;" in content
