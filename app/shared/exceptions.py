from collections.abc import Mapping
from typing import Any


class AppError(Exception):
    """ Base Application Exception With Stable Payload for outer layer mapping. """

    default_code = "app_error"
    default_message = "Application Error"

    def __init__(
        self,
        *,
        message: str | None = None,
        details: Mapping[str, Any] | None = None
    ) -> None:
        self.code = self.default_code
        self.message = message or self.default_message
        self.details = dict(details or {})
        super().__init__(self.message)


    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code" : self.code,
            "message" : self.message
        }
        if self.details:
            payload["details"] = self.details
        
        return payload


class AuthenticationError(AppError):
    """ Raised when Authentication fials. """
    default_code = "authentication_error"
    default_message = "Authentication failed."


class ConflictError(AppError):
    """ Raised when a resource already exists. """

    default_code = "conflict"
    default_message = "the requested resource already exists."


class ResourceNotFoundError(AppError):
    """ Raised when a requested resource does not exists. """

    default_code = "not_found"
    default_message = "the requested resource was not found"