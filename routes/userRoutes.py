from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from schemas.UserSchema import UserCreate, UserLogin, UserUpdate, PasswordResetRequest, PasswordResetVerify, ResetPassword
from core.database import get_db
from services.UserServices import create_user, login_user
from dependencies.auth import get_current_user
from services.UserServices import get_user_details
from services.UserServices import update_user_profile, reset_user_password
from services.VerificationCodeServices import send_code, verify_code
from models.User import User
from utils.passwordReset import set_reset_code, verify_reset_code, clear_reset_code

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

@router.post('/send-verification-code')
async def request_password_reset(playload: PasswordResetRequest,db: Session = Depends(get_db)):
    email = playload.email
    response, error = await send_code(db, email)

    if error:
        raise HTTPException(status_code=404, detail=error)
    return response

@router.post('/verify-verification-code')
def verify_reset_code_endpoint(playload: PasswordResetVerify, db: Session = Depends(get_db)):
    email = playload.email
    code = playload.code
    response, error = verify_code(db, email, code)

    if error:
        raise HTTPException(status_code=404, detail=error)
    return response

@router.put('/reset-password')
def reset_password(playload: ResetPassword, db: Session = Depends(get_db)):
    email = playload.email
    new_password = playload.new_password
    response, error = reset_user_password(db, email, new_password)

    if error:
        raise HTTPException(status_code=404, detail=error)
    return response
