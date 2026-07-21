from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import urlparse


DATA = {
    "profile": {
        "name": "Siri",
        "role": "Researcher",
        "organization": "Student / Internship Project",
        "domains": ["Artificial Intelligence", "Research Analytics", "Innovation"],
        "keywords": ["AI", "funding", "patent analytics", "commercialization"],
        "technologyAreas": ["Machine Learning", "NLP", "Data Science"],
    },
    "metrics": {
        "fundingMatches": 24,
        "researchHotspots": 9,
        "patentSignals": 42,
        "innovationScore": 79,
    },
    "funding": [
        {
            "title": "AI Research Grant",
            "source": "Government Research Council",
            "domain": "Artificial Intelligence",
            "deadline": "30 Aug 2026",
            "match": 92,
            "eligibility": "Researchers, students, and university teams",
            "amount": "Up to Rs. 5,00,000",
            "reason": "Strong match with AI, NLP, and research analytics keywords.",
        },
        {
            "title": "Startup Innovation Seed Fund",
            "source": "Innovation Fund",
            "domain": "Productization",
            "deadline": "15 Sep 2026",
            "match": 84,
            "eligibility": "Startup founders and prototype-stage teams",
            "amount": "Up to Rs. 10,00,000",
            "reason": "Useful for converting research output into a prototype or startup idea.",
        },
        {
            "title": "University Technology Transfer Grant",
            "source": "University Innovation Cell",
            "domain": "Commercialization",
            "deadline": "05 Oct 2026",
            "match": 78,
            "eligibility": "University research groups and innovation cells",
            "amount": "Up to Rs. 3,00,000",
            "reason": "Supports licensing, industry partnerships, and applied research.",
        },
        {
            "title": "Women In AI Innovation Fellowship",
            "source": "International Innovation Agency",
            "domain": "AI Research",
            "deadline": "22 Oct 2026",
            "match": 81,
            "eligibility": "Women students and early-stage researchers",
            "amount": "Mentorship + research support",
            "reason": "Relevant because the profile contains AI, research, and innovation keywords.",
        },
    ],
    "trends": [
        {
            "topic": "Responsible AI Evaluation",
            "growth": "High",
            "relevance": 88,
            "papers": 1280,
            "insight": "Growing interest in safe and explainable AI systems.",
        },
        {
            "topic": "AI-assisted Diagnostics",
            "growth": "High",
            "relevance": 83,
            "papers": 970,
            "insight": "Healthcare AI continues to attract research and funding.",
        },
        {
            "topic": "Research Knowledge Graphs",
            "growth": "Medium",
            "relevance": 76,
            "papers": 640,
            "insight": "Useful for connecting papers, authors, patents, and technologies.",
        },
        {
            "topic": "Patent Similarity Search",
            "growth": "Medium",
            "relevance": 72,
            "papers": 410,
            "insight": "Important for novelty checks and patent landscape analysis.",
        },
    ],
    "patents": [
        {
            "title": "AI System For Research Recommendation",
            "assignee": "Example Labs",
            "domain": "NLP",
            "filingDate": "2025-11-04",
            "citations": 14,
        },
        {
            "title": "Patent Landscape Mapping Method",
            "assignee": "Innovation Analytics Inc.",
            "domain": "Patent Analytics",
            "filingDate": "2025-08-18",
            "citations": 9,
        },
        {
            "title": "Technology Commercialization Scoring Engine",
            "assignee": "Research Ventures",
            "domain": "Innovation Scoring",
            "filingDate": "2026-01-22",
            "citations": 5,
        },
    ],
    "scoreBreakdown": [
        {"factor": "Research Novelty", "weight": 30, "score": 82},
        {"factor": "Patent Strength", "weight": 20, "score": 70},
        {"factor": "Technology Maturity", "weight": 15, "score": 73},
        {"factor": "Market Potential", "weight": 20, "score": 78},
        {"factor": "Funding Relevance", "weight": 15, "score": 81},
    ],
}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/dashboard":
            self.send_json(DATA)
            return
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def send_json(self, data):
        encoded = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("localhost", 8000), Handler)
    print("Research Funding & Innovation Intelligence Platform")
    print("Open http://localhost:8000 in your browser")
    print("Press Ctrl+C to stop the server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
