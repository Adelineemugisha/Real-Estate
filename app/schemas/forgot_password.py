from pydantic import BaseModel, EmailStr

class UserForgotPassword(BaseModel):
    email: EmailStr