# Author: Andrew Bathgate | Date: 2025-06-26
from dataclasses import dataclass, field
from typing import List

@dataclass
class Design:
    text_docs: List[str] = field(default_factory=list)
    mermaid_diagrams: List[str] = field(default_factory=list)

    def add_text(self, doc: str):
        self.text_docs.append(doc)

    def add_mermaid(self, diagram: str):
        self.mermaid_diagrams.append(diagram)

    def summary(self) -> str:
        return f"{len(self.text_docs)} text docs, {len(self.mermaid_diagrams)} mermaid diagrams"

    def get_all_content(self) -> str:
        return "\n\n".join(self.text_docs + self.mermaid_diagrams)
