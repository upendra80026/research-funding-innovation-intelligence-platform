from pydantic import BaseModel
from typing import Optional


class PublicationCreate(BaseModel):
    title: str
    authors: Optional[str] = None
    year: Optional[str] = None
    source: Optional[str] = None
    link: Optional[str] = None


class PublicationResponse(BaseModel):
    id: int
    profile_id: int
    title: str
    authors: Optional[str] = None
    year: Optional[str] = None
    source: Optional[str] = None
    link: Optional[str] = None

    class Config:
        from_attributes = True
        

