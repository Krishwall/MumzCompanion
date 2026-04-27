from pydantic import BaseModel
from typing import List, Optional, Literal

class WeeklyInsight(BaseModel):
    stage_bucket: str
    exact_week_or_month: int
    headline: str
    body: str
    heads_up: Optional[str] = None

class ProductResult(BaseModel):
    id: str
    name: str
    price_aed: float
    relevance_reason: str
    confidence: float

class MumzCompanionResponse(BaseModel):
    input_language: Literal["en", "ar", "unknown"]
    stage_bucket: str
    timeline_insight: WeeklyInsight
    products: List[ProductResult]
    follow_up_prompt: str
    refused: bool
    refusal_reason: Optional[str] = None
    disclaimer: Optional[str] = None