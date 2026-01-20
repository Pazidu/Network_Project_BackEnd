from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetVerify(BaseModel):
    email: EmailStr
    code: str

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str