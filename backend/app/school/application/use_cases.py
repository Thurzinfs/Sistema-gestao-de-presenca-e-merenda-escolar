from uuid import UUID

from app.school.application.dtos import SchoolInDTO, SchoolOutDTO
from app.school.domain.entites import SchoolEntity
from app.school.domain.exceptions import SchoolNotActiveException, SchoolNotFoundException
from app.school.domain.repositories import ISchoolRepository


class RegisterSchoolUseCase:
    def __init__(self, school_repo: ISchoolRepository) -> None:
        self.school_repo = school_repo

    def execute(self, dto: SchoolInDTO) -> SchoolOutDTO:
        if not self.school_repo.verify_exists_school_by_name(dto.name):
            raise SchoolNotFoundException('school not found')
        
        school = SchoolEntity(
            name=dto.name,
            time_closing_presence=dto.time_closing_presence,
            time_send_lunch=dto.time_send_lunch,
            time_send_snack_afternoon=dto.time_send_snack_afternoon,
            number_whats=dto.number_whats
        )

        self.school_repo.save(school)
        return SchoolOutDTO.from_domain(school)


class ResponseSchoolUseCase:
    def __init__(self, school_repo: ISchoolRepository) -> None:
        self.school_repo = school_repo

    def execute(self, id: UUID) -> SchoolOutDTO:
        school = self.school_repo.find_by_id(id)
        if not school:
            raise SchoolNotFoundException('school not found')
        
        if school.deleted_at is not None:
            raise SchoolNotActiveException('school not active')
        
        return SchoolOutDTO.from_domain(school)
    