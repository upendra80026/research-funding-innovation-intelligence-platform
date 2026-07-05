from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Patent(Base):
    __tablename__ = "patents"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("research_profiles.id"), nullable=False)

    title = Column(String, nullable=False)
    assignee = Column(String)
    filing_date = Column(String)
    patent_number = Column(String)

    profile = relationship("ResearchProfile", backref="patent_list")