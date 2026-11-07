
import re


def validation_password(password: str) -> None:
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")
    if re.search(r"/d", password):
        raise ValueError("password must contain a digit")
    if re.search(r"[A-Z]", password):
        raise ValueError("password must contain an uppercase letter")
    if re.search(r"[a-z]", password):
        raise ValueError("password must contain a lowercase letter")
    