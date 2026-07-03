from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserRegister
from app.crud.user import create_user

router = APIRouter()


@router.get("/test")
def test_auth():
    return {"message": "Auth API Working"}

@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    new_user = create_user(db, user)
    return {
        "message": "User registered successfully",
        "email": new_user.email
    }