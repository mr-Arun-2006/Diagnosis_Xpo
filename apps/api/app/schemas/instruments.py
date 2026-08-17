from pydantic import BaseModel, Field


class Instrument(BaseModel):
    symbol: str
    company_name: str
    exchange: str = Field(pattern="^(NSE|BSE)$")
    sector: str | None = None
    industry: str | None = None
    isin: str | None = None
    active: bool = True
