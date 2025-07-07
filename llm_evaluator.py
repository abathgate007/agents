# Author: Andrew Bathgate | Date: 2025-06-26
from typing import Tuple, Optional
from llm_model import LLMModel
import openai
import re

class LLMEvaluator:
    #constructor takes a model and a threshold for passing or failing
    def __init__(self, model: LLMModel, threshold: float = 7.0):
        self.model = model
        self.threshold = threshold

    #evaluate method takes an original prompt used to create the output, the output, and an optional evaluation prompt
    #returns a tuple of a boolean indicating if the output passed, a reason for the pass or fail, and a score from 0 to 10
    #if no evaluation prompt is provided, it uses a default prompt 
    async def evaluate(
        self,
        original_prompt: str,
        output: str,
        eval_prompt: Optional[str] = None
    ) -> Tuple[bool, str, float]:
        """Evaluate whether the output satisfies the original prompt using an optional evaluation instruction prompt."""
        
        # Use default eval prompt if none provided
        if eval_prompt is None:
            eval_prompt = """
You are an expert evaluator.

Given the following task prompt and the LLM-generated output, assess how well the output fulfills the intent of the prompt.

Provide a score from 0 to 10, a pass/fail recommendation, and a short justification.

Respond in the format:

Score: <float from 0 to 10>  
Pass: <yes/no>  
Reason: <short explanation>
"""

#create the full prompt cleaning it of any leading or trailing whitespace
        full_prompt = f"""{eval_prompt.strip()}

---

Prompt:
{original_prompt}

---

Output:
{output}
"""
#call the LLM model to evaluate the output

        content = await self.model.call(full_prompt)
        if content is None:
            content = ""
        text = content.strip()
        

        #parse the text to extract the score, pass/fail, and reason
        # Parse
        score = self._extract_score(text)
        passes = score >= self.threshold
        reason = self._extract_value(text, "Reason")

        return passes, reason, score

    def _extract_value(self, text: str, field: str) -> str:
        for line in text.splitlines():
            if line.strip().lower().startswith(field.lower()):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return "N/A"

    def _extract_score(self, text: str) -> float:
        """Extract and parse score with better error handling."""
        score_text = self._extract_value(text, "Score")
        if score_text == "N/A":
            return 0.0
        
        try:
            # Extract numeric value from text like "Score: 8.5" or "Score: 8"
            match = re.search(r'\d+(?:\.\d+)?', score_text)
            if match:
                score = float(match.group())
                return max(0.0, min(10.0, score))  # Clamp between 0 and 10
            else:
                return 0.0
        except (ValueError, TypeError):
            return 0.0
