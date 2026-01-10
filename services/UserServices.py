from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.User import User
from utils.jwt import create_access_token

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_user(db: Session, firstName: str, lastName: str, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None, "Email already registered"

    hashed_password = pwd_context.hash(password)

    new_user = User(
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user, None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return none, "Invalid email or password"
    
    if not verify_password(password, user.password):
        return none, "Invalid email or password"
    
    token_data = {"first_name": user.firstName, "last_name": user.lastName, "email": user.email}
    access_token = create_access_token(token_data)
    return {"token": access_token, "token_type": "bearer"}, None