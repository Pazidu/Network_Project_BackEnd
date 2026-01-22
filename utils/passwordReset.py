from models.User import User
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.VerificationCode import VerificationCode

def set_reset_code(db: Session, email: str, code: str, purpose: str, expiry_time: int = 15):
    db.query(VerificationCode).filter(
        VerificationCode.email == email,
        VerificationCode.purpose == purpose
    ).delete()
    
    verification = VerificationCode(
        email=email,
        code=code,
        purpose=purpose,
        expires_at=datetime.utcnow() + timedelta(minutes=expiry_time)
    )
    db.add(verification)
    db.commit()

def verify_reset_code(db: Session, record: VerificationCode, code: str):
    print(record.code, code)
    if not record.code or record.code != code:
        return False, "Invalid reset code."
    if datetime.utcnow() > record.expires_at:
        return False, "Verification code has expired."
    return True, None

def clear_reset_code(db: Session, record: VerificationCode):
    db.delete(record)
    db.commit()