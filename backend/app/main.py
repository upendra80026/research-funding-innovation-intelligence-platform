from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user
from app.api.auth import routes as auth_routes
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Research Funding & Innovation Intelligence Platform"
)
app.include_router(
    auth_routes.router,
    prefix="/api/auth",
    tags=["Auth"]
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
