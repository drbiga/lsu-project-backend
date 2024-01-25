from fastapi import APIRouter

from attention.domain.attention import Attention
from attention.domain.attention_algorithm import FourThresholdsAlgorithm
from attention.infra.instances import attention_service

attention_router = APIRouter(prefix='/attentions')

@attention_router.post('')
def save_attention(attention: Attention):
    attention_service.save_attention(attention)

@attention_router.get('')
def get_attentions():
    return attention_service.attentions

@attention_router.get('/feedback')
def compute_attention_feedback():
    four_thresh_algo = FourThresholdsAlgorithm(attention_service.attentions)
    return attention_service.get_attention_feedback(four_thresh_algo)
