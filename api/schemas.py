from pydantic import BaseModel
from typing import List

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    answer: str
    explanation: str

class ExplainRequest(BaseModel):
    prompt: str
    output: str

class ExplainResponse(BaseModel):
    explanation: str
    decision_trace: List[str]
