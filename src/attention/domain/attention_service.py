from attention.domain.attention import Attention
from attention.domain.attention_algorithm import AttentionAlgorithm

class AttentionService:
    def __init__(self) -> None:
        self.attentions = []

    def save_attention(self, attention: Attention) -> None:
        self.attentions.append(attention)

    def get_attention_feedback(self, attention_algorithm: AttentionAlgorithm) -> float:
        return attention_algorithm.compute()
