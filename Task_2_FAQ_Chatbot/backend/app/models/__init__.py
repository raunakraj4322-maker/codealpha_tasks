from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's question")
    
    @field_validator('question')
    @classmethod
    def question_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()


class ChatResponse(BaseModel):
    answer: str
    matched_question: Optional[str] = None
    confidence: float
    category: Optional[str] = None
    faq_id: Optional[int] = None


class FAQItem(BaseModel):
    id: int
    question: str
    answer: str
    category: str


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
