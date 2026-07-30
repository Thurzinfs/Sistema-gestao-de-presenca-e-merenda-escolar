from core.exceptions import BaseDomainException


class ConflictFieldException(BaseDomainException):
    pass


class ClassroomAlreadyExistsException(BaseDomainException):
    pass


class ClassroomNotFoundException(BaseDomainException):
    pass


class ClassroomNotActiveException(BaseDomainException):
    pass


class StudentAlreadyExistsException(BaseDomainException):
    pass


class StudentsNotFoundException(BaseDomainException):
    pass
