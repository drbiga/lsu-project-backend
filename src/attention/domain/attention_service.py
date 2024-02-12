from attention.domain.attention import Attention
from attention.domain.attention_algorithm import AttentionAlgorithm

MAX_ATTENTION_ARRAY_SIZE = 60

class AttentionService:
    def __init__(self) -> None:
        self.attentions = []

    def get_current_attention(self) -> Attention:
        if len(self.attentions) == 0:
            return -1
        return self.attentions[-1]

    def save_attention(self, attention: Attention) -> None:
        if len(self.attentions) > MAX_ATTENTION_ARRAY_SIZE:
            self.attentions.pop(0)
        self.attentions.append(attention)

    def get_attention_feedback(self, attention_algorithm: AttentionAlgorithm) -> float:
        feedback = attention_algorithm.compute()
        return feedback
