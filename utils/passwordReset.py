from models.User import User
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

def set_reset_code(db: Session, user: User, code: str, expiry_time: int = 10):
    user.reset_code = code
    user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=expiry_time)
    db.commit()
    db.refresh(user)

def verify_reset_code(db: Session, user: User, code: str):
    if not user.reset_code or user.reset_code != code:
        return False, "Invalid reset code."
    if datetime.utcnow() > user.reset_code_expiry:
        return False, "Verification code has expired."
    return True, None

def clear_reset_code(db: Session, user: User):
    user.reset_code = None
    user.reset_code_expiry = None
    db.commit()