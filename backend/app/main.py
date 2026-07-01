from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Research Funding & Innovation Intelligence Platform"
)


@app.get("/")
def home():
    return {
        "message": "Platform Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }