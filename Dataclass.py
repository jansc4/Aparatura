from pydantic import BaseModel
from typing import List

class Channel(BaseModel):
    name: str
    unit: str
    data: List[float]

class Badanie(BaseModel):
    name: str
    sample_rate: float  # np. 0.001 dla 1ms/sample
    channels: List[Channel]
