from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationInfo

import re
from datetime import datetime



class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="email of the user for signup")
    password: str = Field(..., description="password of the user for signup")
    confirm_password: str = Field(..., description="confirm password of the user for signup")

    @field_validator("confirm_password")
    @classmethod
    def check_match_password(
        cls, 
        confirm_password, 
        info: ValidationInfo) -> str:
        if (confirm_password != info.data.get("password")):
            raise ValueError("password does not match")
        return confirm_password


    @field_validator("password")
    @classmethod
    def validation_password(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be longer than 8 characters.")
        
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit.")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase English letter.")

        if not re.search(r"[a-z]", password):
            raise ValueError("Password must contain at least one lowercase English letter.")
        return password



class UserLoginSchema(BaseModel):
        email: EmailStr = Field(..., description="email of the user for login", examples=["example@gmail.com"], title="email")
        password: str = Field(..., description="password of the user for login")



class UserUpdateEmailSchema(BaseModel):
    new_email: EmailStr = Field(..., description="new email for update")



class UserUpdatePasswordSchema(BaseModel):
    new_password: str = Field(..., description="new password for update")
    confirm_new_password: str = Field(..., description="confirm new password for update")

    @field_validator("confirm_new_password")
    @classmethod
    def chack_match_password(
        cls,
        confirm_new_password,
        info: ValidationInfo
    ) -> str:
        if (confirm_new_password != info.data.get("new_password")):
            raise ValueError("password does not match")
        return confirm_new_password


    @field_validator("new_password")
    @classmethod
    def validation_password(cls, new_password: str) -> str:
        if len(new_password) <8:
            raise ValueError("Password must be longer than 8 characters.")

        if not re.search(r"[0-9]", new_password):
            raise ValueError("Password must contain at least one digit.")

        if not re.search(r"[A-Z]", new_password):
            raise ValueError("Password must contain at least one uppercase English letter.")

        if not re.search(r"[a-z]", new_password):
            raise ValueError("Password must contain at least one lowercase English letter.")
        return new_password



class UserResponseSchema(BaseModel):
    email: EmailStr
    password: str
    is_active: bool
    created_at: datetime