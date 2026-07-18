from uuid import UUID
from app.canteen.application.dtos import DailyMenuInDTO, DailyMenuOutDTO, DailyMenuUpdateDTO
from app.canteen.domain.entities import DailyMenuEntity
from app.canteen.domain.repositories import IDailyMenuRepository
from datetime import date as Date

class RegisterDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo
    
    def execute(self, dto: DailyMenuInDTO) -> DailyMenuOutDTO:
        if self.daily_menu_repo.find_by_date(dto.date):
            raise ...
        
        daily_Menu = DailyMenuEntity(
            school=dto.school,
            date=dto.date,
            main_course=dto.main_course,
            manager=dto.manager
        )

        daily_Menu = self.daily_menu_repo.save(daily_Menu)
        return DailyMenuOutDTO.from_domain(daily_Menu)
    
class ReturnDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo
        
    def execute(self, date: Date) -> DailyMenuOutDTO:
        entity = self.daily_menu_repo.find_by_date(date)

        if not entity:
            raise ...
        
        return DailyMenuOutDTO.from_domain(entity)

class UpdateDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo

    def execute(self, id: UUID, dto: DailyMenuUpdateDTO) -> DailyMenuOutDTO:
        entity = self.daily_menu_repo.find_by_id(id)
        if not entity:
            raise ...
        
        if dto.date:
            entity.change_date(dto.date)
        
        if dto.main_course:
            entity.change_main_course(dto.main_course)
        
        entity = self.daily_menu_repo.save(entity)
        return DailyMenuOutDTO.from_domain(entity)
        