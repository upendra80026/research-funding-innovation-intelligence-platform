import re
from collections import defaultdict

from sqlalchemy.orm import Session
from app.models.publication import Publication
from app.models.patent import Patent

STOPWORDS = {
    "the", "and", "for", "with", "using", "based", "from", "into", "study",
    "analysis", "review", "approach", "towards", "via", "of", "on", "in",
    "to", "a", "an", "is", "are", "new", "novel", "improved", "toward",
    "system", "systems", "model", "models", "method", "methods", "framework",
    "device", "devices", "apparatus"
}


def _extract_words(title: str):
    words = re.findall(r"[a-zA-Z]+", title.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


def get_technology_intelligence(db: Session, top_n: int = 10):
    """
    Cross-references research publications and patents to identify
    technology areas, classify their maturity, and flag cross-domain
    signals (present in both research AND patents = strong innovation
    opportunity).
    """
    pub_titles = db.query(Publication.title).all()
    patent_titles = db.query(Patent.title).all()

    pub_counts = defaultdict(int)
    patent_counts = defaultdict(int)

    for (title,) in pub_titles:
        if not title:
            continue
        for word in _extract_words(title):
            pub_counts[word] += 1

    for (title,) in patent_titles:
        if not title:
            continue
        for word in _extract_words(title):
            patent_counts[word] += 1

    all_words = set(pub_counts.keys()) | set(patent_counts.keys())

    results = []
    for word in all_words:
        research_mentions = pub_counts.get(word, 0)
        patent_mentions = patent_counts.get(word, 0)
        total = research_mentions + patent_mentions

        if total >= 5:
            maturity = "Mature"
        elif total >= 2:
            maturity = "Growing"
        else:
            maturity = "Emerging"

        results.append({
            "technology": word,
            "research_mentions": research_mentions,
            "patent_mentions": patent_mentions,
            "total_mentions": total,
            "cross_domain": research_mentions > 0 and patent_mentions > 0,
            "maturity": maturity,
        })

    results.sort(key=lambda r: (r["cross_domain"], r["total_mentions"]), reverse=True)
    return results[:top_n]