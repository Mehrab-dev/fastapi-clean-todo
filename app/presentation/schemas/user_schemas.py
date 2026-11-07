
from pydantic import BaseModel, Field, EmailStr, model_validator, field_validator

from uuid import UUID
from datetime import datetime

from app.core.shared.password import validation_password



class UserSignUpSchema(BaseModel):
    email: EmailStr = Field(..., description="email of the user")
    password: str = Field(..., description="password of the user")
    confirm_password: str = Field(..., description="confirm password of the user")

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        validation_password(password=password)
        return password
    

    @model_validator(mode="after")
    def check_match_password(self):
        if self.password != self.confirm_password:
            raise ValueError("password do not match.")
        return self



class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="email of the user for login")
    password: str = Field(..., description="password of the user for login")



class UserUpdateSchema(BaseModel):
    email: EmailStr | None = Field(None, description="email of the user for update")
    password: str  | None = Field(None, description="password of the user for update")
    confirm_password: str | None = Field(None, description="confirm password of the user for update")

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, password: str | None) -> str | None:
        if password is not None:
            validation_password(password=password)
        return password

    @model_validator(mode="after")
    def check_match_password(self):
        if self.password is not None:
            if self.password != self.confirm_password:
                raise ValueError("password do not match.")
        return self


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool = True
    created_at: datetime
    updated_at: datetime