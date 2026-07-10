from uuid import UUID

from app.school.application.dtos import ManagerInDTO, ManagerInUpdateDTO, ManagerOutDTO, SchoolInDTO, SchoolInUpdateDTO, SchoolOutDTO
from app.school.domain.entites import ManagerEntity, SchoolEntity
from app.school.domain.exceptions import ManagerFieldIsRequiredException, ManagerNotActiveException, ManagerNotFoundException, SchoolNotActiveException, SchoolNotFoundException
from app.school.domain.repositories import IManagerRepository, ISchoolRepository


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
    

class UpdateSchoolUseCase:
    def __init__(self, school_repo: ISchoolRepository) -> None:
        self.school_repo = school_repo

    def execute(self, id: UUID, dto: SchoolInUpdateDTO) -> SchoolOutDTO:
        school = self.school_repo.find_by_id(id)
        if not school:
            raise SchoolNotFoundException('school not found')
        
        if school.deleted_at is not None:
            raise SchoolNotActiveException('school not active')
        
        if dto.name:
            school.change_name(dto.name)

        if dto.time_closing_presence:
            school.change_time_closing_presence(dto.time_closing_presence)

        if dto.time_send_lunch:
            school.change_time_send_lunch(dto.time_send_lunch)

        if dto.time_send_snack_afternoon:
            school.change_time_snack_afternoon(dto.time_send_snack_afternoon)

        if dto.number_whats:
            school.change_number_whats(dto.number_whats)

        self.school_repo.save(school)
        return SchoolOutDTO.from_domain(school)


class DeactiveSchoolUseCase:
    def __init__(self, school_repo: ISchoolRepository) -> None:
        self.school_repo = school_repo

    def execute(self, id: UUID) -> SchoolOutDTO:
        school = self.school_repo.find_by_id(id)
        if not school:
            raise SchoolNotFoundException('school not found')

        school.deactive()
        self.school_repo.save(school)
        return SchoolOutDTO.from_domain(school)
    

class RegisterManagerUseCase:
    def __init__(self, manager_repo: IManagerRepository) -> None:
        self.manager_repo = manager_repo

    def execute(self, dto: ManagerInDTO) -> ManagerOutDTO:
        if self.manager_repo.find_by_email(dto.email):
            raise ManagerNotFoundException('email already register')
        
        if not dto.school_id:
            raise ManagerFieldIsRequiredException('school id is required')
        
        manager = ManagerEntity(
            name=dto.name,
            email=dto.email,
            password=dto.password,
            role=dto.role,
            school=dto.school_id
        )

        self.manager_repo.save(manager)
        return ManagerOutDTO.from_domain(manager)
    

class ResponseManagerByIDUseCase:
    def __init__(self, manager_repo: IManagerRepository) -> None:
        self.manager_repo = manager_repo

    def execute(self, id:UUID) -> ManagerOutDTO:
        manager = self.manager_repo.find_by_id(id)
        if not manager:
            raise ManagerNotFoundException('manager not found')
        
        if manager.active is not False:
            raise ManagerNotActiveException('manager not active')
        
        return ManagerOutDTO.from_domain(manager)


class UpdateManagerUseCase:
    def __init__(self, manager_repo: IManagerRepository) -> None:
        self.manager_repo = manager_repo

    def execute(self, id: UUID, dto: ManagerInUpdateDTO) -> ManagerOutDTO:
        manager = self.manager_repo.find_by_id(id)
        if not manager:
            raise ManagerNotFoundException('manager not found')
        
        if manager.active is not False:
            raise ManagerNotActiveException('manager not is active')
        
        if dto.name:
            manager.change_name(dto.name)

        if dto.email:
            manager.change_email(dto.email)

        if dto.password:
            manager.change_password(dto.password)

        if dto.role:
            manager.change_role(dto.role)

        self.manager_repo.save(manager)
        return ManagerOutDTO.from_domain(manager)


class DeactiveManagerUseCase: 
    def __init__(self, manager_repo: IManagerRepository) -> None:
        self.manager_repo = manager_repo

    def execute(self, id: UUID) -> ManagerOutDTO:
        manager = self.manager_repo.find_by_id(id)
        if not manager:
            raise ManagerNotFoundException("manager not found")
        
        if manager.active is not True:
            raise ManagerNotActiveException("manager not active")
        
        manager.deactive()
        self.manager_repo.save(manager)
        return ManagerOutDTO.from_domain(manager)
    