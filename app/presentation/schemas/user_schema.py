from pydantic import BaseModel, Field, EmailStr, field_validator
import re



class UserSignUpSchema(BaseModel):
    email: EmailStr = Field(..., description="email of the user")
    password: str = Field(..., description="password of the user for signup")
    confirm_password: str = Field(..., description="confirm password of the user for signup")


    @field_validator("confirm_password")
    @classmethod
    def chack_match_password(cls, confirm_password,validation):
        if (confirm_password != validation.data.get("password")):
            raise ValueError("password does not match")


    @field_validator("password")
    @classmethod
    def validation_password(cls, password: str) -> str:
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
        if not re.match(password_pattern, password):
            raise ValueError(
                "Password must be at least 8 characters long "
                "and contain uppercase, lowercase, and a number."
            )
        return password


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="email of the user for login")
    password: str = Field(..., description="password of the user for login")



class UserUpdateEmailSchema(BaseModel):
    new_email: EmailStr = Field(..., description="new email of the user for update")



class UserUpdatePasswordSchema(BaseModel):
    new_password: str = Field(..., description="new password of the user for update")
    confirm_new_password: str = Field(..., description="confirm new password of the user for update")

    @field_validator("confirm_password")
    @classmethod
    def check_match_password(cls, confirm_password, validation):
        if (confirm_password != validation.data.get("password")):
            raise ValueError("password does not match")


    @field_validator("password")
    @classmethod
    def password_validation(cls, password: str) -> str:
        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
        if not re.match(password_pattern, password):
            raise ValueError(
                "Password must be at least 8 characters long "
                "and contain uppercase, lowercase, and a number."
            )
        return password
