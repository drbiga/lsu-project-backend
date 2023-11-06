from typing import List
from attention.domain.attention import Attention
from attention.domain.attention_algorithm import AttentionAlgorithm

class IsabelleAttentionAlgorithm(AttentionAlgorithm):
    def __init__(self, path: str) -> None:
        self.path = path

    def compute(self) -> float:
        with open(self.path, 'r') as feedback_file:
            return float(feedback_file.read())
