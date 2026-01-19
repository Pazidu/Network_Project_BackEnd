from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.UserSchema import UserCreate, UserLogin, UserUpdate
from core.database import get_db
from services.UserServices import create_user, login_user
from dependencies.auth import get_current_user
from services.UserServices import get_user_details
from services.UserServices import update_user_profile

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

@router.get("/profile")
def get_profile(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_data, error = get_user_details(db, current_user['email'])

    if error:
        raise HTTPException(status_code=404, detail=error)
    return user_data

@router.put('/profile')
def update_profile(user: UserUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    updateToken, error = update_user_profile(db, current_user['email'], user.email, user.firstName, user.lastName)

    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"message": "Profile updated successfully", "token": updateToken}
