from http import HTTPStatus


class CustomException(Exception):
    def __init__(self, http_code=None, code=None, message=None, details=None):
        self.http_code = (
            http_code
            if isinstance(http_code, int) and http_code in list(HTTPStatus)
            else HTTPStatus.INTERNAL_SERVER_ERROR
        )
        self.code = code if isinstance(code, int) else 0
        self.message = message if isinstance(message, str) else ""
        self.details = details if isinstance(details, dict) else {}
        super().__init__(message)

    def __str__(self):
        return f"[code {self.code}] {self.message}"

    def to_dict(self):
        return {"code": self.code, "message": self.message, "details": self.details}


class BadRequestException(CustomException):
    def __init__(self, message):
        super().__init__(http_code=HTTPStatus.BAD_REQUEST, message=message)


class ContentTypeNotSupportedException(CustomException):
    def __init__(self):
        super().__init__(
            http_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE, message="Content type is not supported"
        )


class FailedResponse(CustomException):
    def __init__(self, code, message):
        super().__init__(http_code=HTTPStatus.BAD_REQUEST, code=code, message=message)


class NotFoundException(CustomException):
    def __init__(self, message):
        super().__init__(http_code=HTTPStatus.NOT_FOUND, message=message)


EXCEPTIONS_IGNORING_ALERT = (FailedResponse,)
