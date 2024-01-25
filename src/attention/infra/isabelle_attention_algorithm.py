from typing import List
from attention.domain.attention import Attention
from attention.domain.attention_algorithm import AttentionAlgorithm
import requests

class IsabelleAttentionAlgorithm(AttentionAlgorithm):
    def compute(self) -> float:
        return requests.get('http://localhost:57827/intervention_status').json()['isFocused']
