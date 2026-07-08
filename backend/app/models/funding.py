from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base


class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    source = Column(String)              # e.g. "Government Grant", "Startup Accelerator"
    description = Column(Text)
    eligibility = Column(Text)           # who can apply
    domains = Column(Text)               # comma-separated, matched against research_domains
    deadline = Column(String)
    amount = Column(String)
    link = Column(String)