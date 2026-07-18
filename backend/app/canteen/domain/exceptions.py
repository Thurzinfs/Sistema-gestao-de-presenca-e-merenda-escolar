from core.exceptions import BaseDomainException


class ConflictFieldCanteenException(BaseDomainException):
    pass

class NotFoundCanteenException(BaseDomainException):
    pass