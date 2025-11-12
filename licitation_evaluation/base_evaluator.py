import os
import dotenv
import json
from abc import ABC, abstractmethod
from openai import OpenAI

dotenv.load_dotenv()

class BaseEvaluator(ABC):
    def __init__(self, model: str = "gpt-5-nano-2025-08-07"):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    @abstractmethod
    def evaluate_licitation(self, licitation: json):
        # Evaluates the licitation according to criteria/discipline
        pass
