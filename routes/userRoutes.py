from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.UserSchema import UserCreate, UserLogin
from core.database import get_db
from services.UserServices import create_user, login_user

router = APIRouter()

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user, error = create_user(
        db, user.firstName, user.lastName, user.email, user.password
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token, error = login_user(db, user.email, user.password)
    
    if error:
        raise HTTPException(status_code=401, detail=error)
    return token
