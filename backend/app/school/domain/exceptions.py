from core.exceptions import BaseDomainException


class ConflictFieldException(BaseDomainException):
    pass


class SchoolNotFoundException(BaseDomainException):
    pass
