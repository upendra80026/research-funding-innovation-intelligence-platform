from sqlalchemy.orm import Session
from app.models.patent import Patent
from app.schemas.patent import PatentCreate


def create_patent(db: Session, profile_id: int, data: PatentCreate):
    new_patent = Patent(
        profile_id=profile_id,
        title=data.title,
        assignee=data.assignee,
        filing_date=data.filing_date,
        patent_number=data.patent_number,
    )
    db.add(new_patent)
    db.commit()
    db.refresh(new_patent)
    return new_patent


def get_patents_by_profile(db: Session, profile_id: int):
    return db.query(Patent).filter(Patent.profile_id == profile_id).all()