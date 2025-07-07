from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )


class ResourceNotFoundException(HTTPException):
    def __init__(self, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with ID {resource_id} not found",
        )


class AuthorizationException(HTTPException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class AuthenticationException(HTTPException):
    def __init__(self, message: str = "Unauthenticated access"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class ServerException(HTTPException):
    def __init__(self, message: str = "Server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
