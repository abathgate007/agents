# Author: Andrew Bathgate | Date: 2025-06-26

from default_evaluation_routine import DefaultEvaluationRoutine
from llm_model import LLMModel
from evaluated_output import EvaluatedOutput
from design import Design  # You’ve defined this elsewhere
from typing import Optional

class SecurityDesignReviewer:
    """
    Orchestrates a security design review using multiple LLMs and a structured evaluation routine.
    """

    def __init__(self, models: list[LLMModel], max_attempts: int = 3, threshold: float = 7.0):
        self.evaluator = DefaultEvaluationRoutine(models=models, max_attempts=max_attempts, evaluator_threshold=threshold)

    async def review(self, design: Design, eval_prompt: Optional[str] = None) -> EvaluatedOutput:
        """
        Runs a security review on the provided design.

        Args:
            design: Design object containing architecture artifacts (e.g., plaintext, mermaid).
            eval_prompt: Optional prompt guiding how outputs are evaluated.

        Returns:
            EvaluatedOutput with review results.
        """
        prompt = self._build_prompt_from_design(design)
        result = await self.evaluator.run(prompt=prompt, eval_prompt=eval_prompt)
        return result

    def _build_prompt_from_design(self, design: Design) -> str:
        """
        Builds a security review prompt from the design content.

        Args:
            design: The Design instance to review.

        Returns:
            A natural-language prompt instructing the model to perform a security review.
        """
        parts = []
        if design.text_docs:
            parts.append(f"Architecture Overview:\n{design.text_docs}")
        if design.mermaid_diagrams:
            parts.append(f"\nMermaid Diagram:\n```\n{design.mermaid_diagrams}\n```")

        return (
            "You are a senior application security architect. Perform a security design review of the system below. "
            "Identify any architectural weaknesses, potential attack surfaces, and recommend mitigations.\n\n"
            + "\n\n".join(parts)
        )
