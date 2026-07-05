from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("research_profiles.id"), nullable=False)

    title = Column(String, nullable=False)
    authors = Column(String)
    year = Column(String)
    source = Column(String)      # journal/conference name
    link = Column(String)        # URL to paper

    profile = relationship("ResearchProfile", backref="publication_list")