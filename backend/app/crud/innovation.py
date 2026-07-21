from sqlalchemy.orm import Session

from app.crud.publication import get_publications_by_profile
from app.crud.patent import get_patents_by_profile
from app.crud.technology import get_technology_intelligence
from app.crud.funding import get_recommended_funding


def _score_research_novelty(publication_count: int) -> float:
    # Each publication contributes up to 100 (capped)
    return min(publication_count * 15, 100)


def _score_patent_strength(patent_count: int) -> float:
    return min(patent_count * 20, 100)


def _score_technology_maturity(db: Session) -> float:
    tech_data = get_technology_intelligence(db, top_n=20)
    if not tech_data:
        return 0

    strong = sum(1 for t in tech_data if t["maturity"] in ("Mature", "Growing"))
    return round((strong / len(tech_data)) * 100, 1)


def _score_market_potential(funding_matches: int) -> float:
    return min(funding_matches * 25, 100)


def _score_funding_relevance(funding_matches: int, total_funding: int) -> float:
    if total_funding == 0:
        return 0
    return round((funding_matches / total_funding) * 100, 1)


def get_innovation_score(db: Session, profile):
    publications = get_publications_by_profile(db, profile.id)
    patents = get_patents_by_profile(db, profile.id)

    from app.crud.funding import get_all_funding
    all_funding = get_all_funding(db)
    matched_funding = get_recommended_funding(db, profile.research_domains)

    research_novelty = _score_research_novelty(len(publications))
    patent_strength = _score_patent_strength(len(patents))
    technology_maturity = _score_technology_maturity(db)
    market_potential = _score_market_potential(len(matched_funding))
    funding_relevance = _score_funding_relevance(len(matched_funding), len(all_funding))

    total_score = (
        research_novelty * 0.30
        + patent_strength * 0.20
        + technology_maturity * 0.15
        + market_potential * 0.20
        + funding_relevance * 0.15
    )

    if total_score >= 75:
        rating = "High Potential"
    elif total_score >= 45:
        rating = "Moderate Potential"
    else:
        rating = "Early Stage"

    return {
        "innovation_score": round(total_score, 1),
        "rating": rating,
        "breakdown": {
            "research_novelty": {"score": research_novelty, "weight": "30%"},
            "patent_strength": {"score": patent_strength, "weight": "20%"},
            "technology_maturity": {"score": technology_maturity, "weight": "15%"},
            "market_potential": {"score": market_potential, "weight": "20%"},
            "funding_relevance": {"score": funding_relevance, "weight": "15%"},
        },
    }