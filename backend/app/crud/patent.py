import re
from collections import defaultdict

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


def _extract_year(filing_date: str):
    if not filing_date:
        return "Unknown"
    match = re.search(r"(19|20)\d{2}", filing_date)
    return match.group(0) if match else "Unknown"


def get_patent_trend(db: Session):
    """
    Groups all patents by filing year and returns a count per year.
    Example: [{"year": "2024", "count": 2}, {"year": "2025", "count": 3}]
    """
    patents = db.query(Patent.filing_date).all()

    year_counts = defaultdict(int)
    for (filing_date,) in patents:
        year = _extract_year(filing_date)
        year_counts[year] += 1

    results = [{"year": year, "count": count} for year, count in year_counts.items()]
    results.sort(key=lambda r: r["year"])
    return results


def get_competitor_analysis(db: Session, top_n: int = 8):
    """
    Groups patents by assignee to identify the most active
    organizations/competitors in the patent landscape.
    """
    patents = db.query(Patent.assignee).all()

    assignee_counts = defaultdict(int)
    for (assignee,) in patents:
        name = assignee if assignee else "Unknown"
        assignee_counts[name] += 1

    results = [{"assignee": name, "patent_count": count} for name, count in assignee_counts.items()]
    results.sort(key=lambda r: r["patent_count"], reverse=True)
    return results[:top_n]


STOPWORDS = {
    "the", "and", "for", "with", "using", "based", "from", "into", "system",
    "systems", "method", "methods", "device", "devices", "apparatus", "of",
    "on", "in", "to", "a", "an", "is", "are", "new", "improved"
}


def _extract_words(title: str):
    words = re.findall(r"[a-zA-Z]+", title.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def get_technology_clusters(db: Session, top_n: int = 8):
    """
    Extracts keywords from patent titles to map the most common
    technology areas represented in the patent portfolio (innovation mapping).
    """
    patents = db.query(Patent.title).all()

    word_counts = defaultdict(int)
    for (title,) in patents:
        if not title:
            continue
        for word in _extract_words(title):
            word_counts[word] += 1

    clusters = [{"technology": word, "mentions": count} for word, count in word_counts.items()]
    clusters.sort(key=lambda c: c["mentions"], reverse=True)
    return clusters[:top_n]