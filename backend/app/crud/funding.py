from sqlalchemy.orm import Session
from app.models.funding import FundingOpportunity
from app.schemas.funding import FundingCreate


def create_funding(db: Session, data: FundingCreate):
    new_funding = FundingOpportunity(
        title=data.title,
        source=data.source,
        description=data.description,
        eligibility=data.eligibility,
        domains=data.domains,
        deadline=data.deadline,
        amount=data.amount,
        link=data.link,
    )
    db.add(new_funding)
    db.commit()
    db.refresh(new_funding)
    return new_funding


def get_all_funding(db: Session):
    return db.query(FundingOpportunity).all()


def get_funding_by_id(db: Session, funding_id: int):
    return db.query(FundingOpportunity).filter(FundingOpportunity.id == funding_id).first()


def get_recommended_funding(db: Session, user_domains: str, user_role: str = None):
    """
    Matches funding opportunities on two signals:
    1. Domain overlap between user's research_domains and funding.domains
    2. Optional role/eligibility keyword match (soft match, doesn't exclude if missing)
    """
    if not user_domains:
        return []

    user_keywords = [kw.strip().lower() for kw in user_domains.split(",") if kw.strip()]
    all_funding = db.query(FundingOpportunity).all()

    matched = []
    for funding in all_funding:
        if not funding.domains:
            continue
        funding_keywords = [kw.strip().lower() for kw in funding.domains.split(",")]
        domain_match = any(kw in funding_keywords for kw in user_keywords)

        if not domain_match:
            continue

        if user_role and funding.eligibility:
            eligibility_text = funding.eligibility.lower()
            role_readable = user_role.replace("_", " ").lower()
            if role_readable not in eligibility_text and "all" not in eligibility_text:
                continue

        matched.append(funding)

    return matched