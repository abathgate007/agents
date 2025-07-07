# Author: Andrew Bathgate | Date: 2025-06-26

from typing import List, Optional
from evaluation_routine import EvaluationRoutine
from llm_model import LLMModel
from evaluated_output import EvaluatedOutput
from llm_evaluator import LLMEvaluator
import asyncio
import openai  # Ensure you have this import
from openai import AsyncOpenAI

class DefaultEvaluationRoutine(EvaluationRoutine):
    """
    Runs a prompt across multiple LLMs asynchronously.
    Evaluates outputs and returns the best result or fails after N attempts.
    """

    def __init__(
        self,
        models: List[LLMModel],
        max_attempts: int = 3,
        evaluator_threshold: float = 7.0
    ):
        """
        Initialize the evaluation routine with a list of models, retry limit, and pass threshold.

        Args:
            models: List of LLMModel instances to use.
            max_attempts: Number of retry attempts allowed.
            evaluator_threshold: Score threshold for passing.
        """
        self.models = models
        self.max_attempts = max_attempts
        self.evaluator_threshold = evaluator_threshold
        # TODO: Track failed attempts or switch models dynamically in future.

    async def run(
        self,
        prompt: str,
        eval_prompt: Optional[str] = None
    ) -> EvaluatedOutput:
        """
        Run the evaluation routine using multiple LLM models in parallel.

        Each model attempts to generate and evaluate output based on the given prompt.
        The routine retries up to max_attempts if evaluation fails, and selects the first passing result.

        Returns:
            An EvaluatedOutput instance containing the best passing result.

        Raises:
            RuntimeError: If no model produces acceptable output within allowed attempts.
        """
        print (self.models)
        for attempt in range(self.max_attempts):
            print(f"🧠 Attempt {attempt + 1} of {self.max_attempts}")

            outputs = await asyncio.gather(
                *[self._generate_and_evaluate(model, prompt, eval_prompt) for model in self.models],
                return_exceptions=True
            )

            for result in outputs:
                if isinstance(result, EvaluatedOutput) and result.passes:
                    print(f"✅ Success from {result.model_name} on attempt {attempt + 1}")
                    return result

        raise RuntimeError("❌ All models failed to produce acceptable output within the allowed attempts.")

    async def _generate_and_evaluate(
        self,
        model: LLMModel,
        prompt: str,
        eval_prompt: Optional[str]
    ) -> Optional[EvaluatedOutput]:
        """
        Generate output from a single LLM model and evaluate its quality.

        Args:
            model: The LLMModel instance to generate and evaluate output with.
            prompt: The original task prompt to send to the model.
            eval_prompt: Optional evaluation instructions to guide the evaluator.

        Returns:
            An EvaluatedOutput object containing the model's output, evaluation result, and score,
            or None if an error occurs.
        """
        try:
            print(f"🔑 Using model: {model.model_name}, key: {model.api_key[:6]}..., base_url: {model.base_url or 'default (OpenAI)'}")
            '''
            if model.base_url:
                client = AsyncOpenAI(api_key=model.api_key, base_url=model.base_url)
            else:
                client = AsyncOpenAI(api_key=model.api_key)
            response = await client.chat.completions.create(
                model=model.model_name,
                messages=[{"role": "user", "content": prompt}],
            )
            output = response.choices[0].message.content or ""
            '''
            output = await model.call(prompt)
            print(f"🔑 Output: {output}")
            evaluator = LLMEvaluator(model, threshold=self.evaluator_threshold)
            passed, reason, score = await evaluator.evaluate(prompt, output, eval_prompt)

            return EvaluatedOutput(
                output_content=output,
                model_name=model.model_name,
                passes=passed,
                evaluation_reason=reason,
                attempts=1,
                final_score=score,
                failed_attempts=[]
            )

        except Exception as e:
            print(f"⚠️ Model {model.model_name} failed: {str(e)}")
            return None
