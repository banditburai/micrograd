from dataclasses import dataclass, asdict, field
from typing import List, Any
import json

@dataclass
class VisualizationState:
    zoom_level: float = 0.5
    visible_controls: List[str] = field(default_factory=list)
    params: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class VisualizationStateManager:
    def __init__(self):
        self.states = {}

    def get_state(self, viz_id):
        if viz_id not in self.states:
            self.states[viz_id] = VisualizationState()
        return self.states[viz_id]

    def update_state(self, viz_id, **kwargs):
        current_state = self.get_state(viz_id)
        for key, value in kwargs.items():
            setattr(current_state, key, value)
        self.states[viz_id] = current_state

    def to_dict(self, viz_id):
        return self.get_state(viz_id).to_dict()