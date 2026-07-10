from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.publication import Publication
from app.schemas.publication import PublicationCreate


def create_publication(db: Session, profile_id: int, data: PublicationCreate):
    new_pub = Publication(
        profile_id=profile_id,
        title=data.title,
        authors=data.authors,
        year=data.year,
        source=data.source,
        link=data.link,
    )
    db.add(new_pub)
    db.commit()
    db.refresh(new_pub)
    return new_pub


def get_publications_by_profile(db: Session, profile_id: int):
    return db.query(Publication).filter(Publication.profile_id == profile_id).all()


def get_publication_trend(db: Session):
    """
    Groups all publications by year and returns a count per year.
    Example: [{"year": "2024", "count": 3}, {"year": "2025", "count": 5}]
    """
    results = (
        db.query(Publication.year, func.count(Publication.id))
        .group_by(Publication.year)
        .order_by(Publication.year)
        .all()
    )

    return [{"year": year if year else "Unknown", "count": count} for year, count in results]