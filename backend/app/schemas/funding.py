from pydantic import BaseModel
from typing import Optional


class FundingCreate(BaseModel):
    title: str
    source: Optional[str] = None
    description: Optional[str] = None
    eligibility: Optional[str] = None
    domains: Optional[str] = None
    deadline: Optional[str] = None
    amount: Optional[str] = None
    link: Optional[str] = None


class FundingResponse(BaseModel):
    id: int
    title: str
    source: Optional[str] = None
    description: Optional[str] = None
    eligibility: Optional[str] = None
    domains: Optional[str] = None
    deadline: Optional[str] = None
    amount: Optional[str] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True