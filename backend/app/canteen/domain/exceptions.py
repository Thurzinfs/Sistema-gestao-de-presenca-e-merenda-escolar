from core.exceptions import BaseDomainException


class ConflictFieldCanteenException(BaseDomainException):
    pass

class NotFoundCanteenException(BaseDomainException):
    pass

class AlreadyExistsCanteenException(BaseDomainException):
    pass

class InvalidDateFieldCanteenException(BaseDomainException):
    pass