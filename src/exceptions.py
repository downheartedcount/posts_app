class AppException(Exception):
   pass


class FetchError(AppException):
    pass


class DatabaseError(AppException):
    pass


class NotFoundError(AppException):
    pass
