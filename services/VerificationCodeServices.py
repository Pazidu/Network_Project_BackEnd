from sqlalchemy.orm import Session
from models.User import User
import random
from utils.mail import send_verification_code
from utils.passwordReset import set_reset_code, verify_reset_code, clear_reset_code

async def send_code(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None, "User not found"
    
    code = str(random.randint(100000, 999999))
    set_reset_code(db, user, code)
    await send_verification_code(email, code)

    return {"message": "Verification code sent to your email."}, None

def verify_code(db: Session, email: str, code: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None, "User not found"
    
    is_valid, error = verify_reset_code(db, user, code)
    if not is_valid:
        return None, error
    
    clear_reset_code(db, user)
    return {"message": "Verification code is valid."}, None