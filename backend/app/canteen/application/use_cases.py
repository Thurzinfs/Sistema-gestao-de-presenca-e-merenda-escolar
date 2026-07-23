from typing import List
from uuid import UUID
from app.canteen.application.dtos import (
    DailyMenuInDTO,
    DailyMenuOutDTO,
    DailyMenuUpdateDTO,
    LeftouversLunchInDTO,
    LeftouversLunchOutDTO,
    LeftouversLunchUpdateDTO
)
from app.canteen.domain.entities import DailyMenuEntity, LeftouversLunchEntity
from app.canteen.domain.exceptions import (
    AlreadyExistsCanteenException,
    InvalidDateFieldCanteenException,
    NotFoundCanteenException,
)
from app.canteen.domain.repositories import IDailyMenuRepository, ILeftouversLunchRepository
from datetime import date as Date
from app.canteen.domain.servicies import IPickDatesService, IVerifyLeftouverLunchExistsService


class RegisterDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo

    def execute(self, dto: DailyMenuInDTO) -> DailyMenuOutDTO:
        if self.daily_menu_repo.verify_by_date(dto.date):
            raise AlreadyExistsCanteenException(
                'daily menu already exists by date'
            )

        daily_Menu = DailyMenuEntity(
            school=dto.school,
            date=dto.date,
            main_course=dto.main_course,
            manager=dto.manager,
        )

        daily_Menu = self.daily_menu_repo.save(daily_Menu)
        return DailyMenuOutDTO.from_domain(daily_Menu)


class ReturnDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo

    def execute(self, date: Date) -> DailyMenuOutDTO:
        entity = self.daily_menu_repo.find_by_date(date)

        if not entity:
            raise NotFoundCanteenException('not found daily menu by date')

        return DailyMenuOutDTO.from_domain(entity)


class UpdateDailyMenuUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo

    def execute(self, id: UUID, dto: DailyMenuUpdateDTO) -> DailyMenuOutDTO:
        entity = self.daily_menu_repo.find_by_id(id)
        if not entity:
            raise NotFoundCanteenException('not found daily menu by date')

        if dto.date:
            entity.change_date(dto.date)

        if dto.main_course:
            entity.change_main_course(dto.main_course)

        entity = self.daily_menu_repo.save(entity)
        return DailyMenuOutDTO.from_domain(entity)


class ReturnWithDateRangeUseCase:
    def __init__(self, pick_dates_service: IPickDatesService):
        self.pick_dates_service = pick_dates_service

    def execute(self, from_date: Date, to_date: Date) -> List[DailyMenuOutDTO]:
        if from_date > to_date:
            raise InvalidDateFieldCanteenException(
                'from_date is greater than to_date'
            )

        entities = self.pick_dates_service.pick_dates(from_date, to_date)
        return [DailyMenuOutDTO.from_domain(entity) for entity in entities]

class ReturnWithIdUseCase:
    def __init__(self, daily_menu_repo: IDailyMenuRepository):
        self.daily_menu_repo = daily_menu_repo

    def execute(self, id: UUID) -> DailyMenuOutDTO:
        daily_menu = self.daily_menu_repo.find_by_id(id)
        if not daily_menu:
            raise NotFoundCanteenException('not found this daily menu')
        
        return DailyMenuOutDTO.from_domain(daily_menu)

class RegisterLeftouversLunchUseCase:
    def __init__(self, leftouvers_lunch_repo: ILeftouversLunchRepository, leftouvers_lunch_exists_service: IVerifyLeftouverLunchExistsService):
        self.leftouvers_lunch_repo = leftouvers_lunch_repo
        self.leftouvers_lunch_exists_service = leftouvers_lunch_exists_service

    def execute(self, dto: LeftouversLunchInDTO) -> LeftouversLunchOutDTO:
        if self.leftouvers_lunch_exists_service.verify():
            raise AlreadyExistsCanteenException('a report has already been created today')

        leftouvers_lunch = LeftouversLunchEntity(
            school=dto.school,
            leftouvers_kg=dto.leftouvers_kg,
            amount_students=dto.amount_students,
            user=dto.user
        )

        leftouvers_lunch = self.leftouvers_lunch_repo.save(leftouvers_lunch)
        return LeftouversLunchOutDTO.from_domain(leftouvers_lunch)