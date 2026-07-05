from pydantic import BaseModel
from typing import Optional


class PatentCreate(BaseModel):
    title: str
    assignee: Optional[str] = None
    filing_date: Optional[str] = None
    patent_number: Optional[str] = None


class PatentResponse(BaseModel):
    id: int
    profile_id: int
    title: str
    assignee: Optional[str] = None
    filing_date: Optional[str] = None
    patent_number: Optional[str] = None

    class Config:
        from_attributes = True