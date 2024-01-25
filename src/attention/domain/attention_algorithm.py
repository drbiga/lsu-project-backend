# Interfaces
from abc import ABC, abstractmethod

# Typing
from typing import List

# Time
from datetime import datetime, timedelta
import pytz

from statistics import mean, stdev

from attention.domain.attention import Attention


class AttentionAlgorithm(ABC):
    # @abstractmethod
    # def compute(self, attentions: List[Attention]) -> float:
    #     ...
    @abstractmethod
    def compute(self) -> float:
        ...

class FourThresholdsAlgorithm(AttentionAlgorithm, DeprecationWarning):
    def __init__(self, attentions: List[Attention]) -> None:
        self.attentions = attentions

    def compute(self) -> float:
        subset = self.filter_last_minute(self.attentions)
        input_levels = self.compute_input_levels_from_attentions(subset)
        return self.compute_threshold_from_input_levels(input_levels)

    def filter_last_minute(self, attentions: List[Attention]) -> List[Attention]:
        now = datetime.now()
        utc = pytz.UTC
        now = utc.localize(now)
        subset = [
            attention
            for attention in attentions
            if attention.timestamp_start > now - timedelta(seconds=60)
        ]
        return subset

    def compute_input_levels_from_attentions(self, attentions: List[Attention]) -> List[float]:
        return [
            (
                att.num_keyboard_strokes
                + att.num_mouse_clicks
                + att.size_mouse_scroll
                + att.dist_mouse_movement
            )
            for att in attentions
        ]

    def compute_threshold_from_input_levels(self, input_levels: List[float]) -> float:
        avg_input_level = mean(input_levels)
        std = stdev(input_levels)
        if input_levels[-1] < avg_input_level - std/2:
            return 1
        elif input_levels[-1] < avg_input_level - std/4:
            return 2
        elif input_levels[-1] < avg_input_level + std/4:
            return 3
        else:
            return 4
