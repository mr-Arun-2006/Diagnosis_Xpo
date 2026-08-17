from pydantic import BaseModel, Field

class MarketSnapshot(BaseModel):
    nifty: float
    sensex: float
    india_vix: float
    market_score: int = Field(ge=0, le=100)
    data_status: str
