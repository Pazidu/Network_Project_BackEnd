from sqlalchemy.orm import Session
from models.VerificationCode import VerificationCode
import random
from utils.mail import send_verification_code
from utils.passwordReset import set_reset_code, verify_reset_code, clear_reset_code

async def send_code(db: Session, email: str, purpose: str):
    code = str(random.randint(100000, 999999))
    set_reset_code(db, email, code, purpose)
    await send_verification_code(email, code)

    return {"message": "Verification code sent to your email."}, None

def verify_code(db: Session, email: str, code: str, purpose: str):
    record = db.query(VerificationCode).filter(
        VerificationCode.email == email
    ).first()
    if not record:
        return None, "Invalid verification code"
    is_valid, error = verify_reset_code(db, record, code)
    if not is_valid:
        return None, error
    
    clear_reset_code(db, record)
    return {"message": "Verification code is valid."}, None