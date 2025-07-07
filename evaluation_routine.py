# Author: Andrew Bathgate | Date: 2025-06-26
from typing import List, Tuple, Protocol
from llm_model import LLMModel

class Evaluator(Protocol):
    def evaluate(self, output: str) -> Tuple[bool, str]:
        ...

class EvaluationRoutine:
    def __init__(self, prompt: str, models: List[LLMModel], evaluator: Evaluator, max_attempts: int = 3):
        self.prompt = prompt
        self.models = models
        self.evaluator = evaluator
        self.max_attempts = max_attempts
        self.fail_log = []  # Placeholder: list of (model, output, reason)

    def run(self) -> str:
        # Main generation + retry + merge + final eval loop
        raise NotImplementedError("EvaluationRoutine.run() not implemented yet")

    def _track_failure(self, model: LLMModel, output: str, reason: str):
        # 🔧 Placeholder for future logic: storing failed attempts
        self.fail_log.append((model.model_name, reason))
        # Optional: print/debug now
        print(f"⚠️ {model.model_name} rejected: {reason[:100]}...")

    def _switch_model(self, current_index: int) -> int:
        # 🔄 Placeholder for future model fallback/switching
        # For now, just rotate to the next model
        return (current_index + 1) % len(self.models)
