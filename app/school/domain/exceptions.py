from core.exceptions import BaseDomainException


class ConflictFieldException(BaseDomainException):
    pass


class SchoolNotFoundException(BaseDomainException):
    pass


class SchoolNotActiveException(BaseDomainException):
    pass


class ManagerNotFoundException(BaseDomainException):
    pass


class ManagerNotActiveException(BaseDomainException):
    pass


class ManagerFieldIsRequiredException(BaseDomainException):
    pass
