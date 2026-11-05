

class AppException(Exception):

    default_message = "bad requests"

    def __init__(self, message: str | None):
        self.message = message or self.default_message
        super().__init__(self.message)


class ConflictException(AppException):
    default_message = "already exists."

class AuthenticationException(AppException):
    default_message = "authentication error."

class ForbiddenException(AppException):
    default_message = "forbidden."

class NotFoundException(AppException):
    default_message = "not found."