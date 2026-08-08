from typing import List
from datetime import datetime
from uuid import UUID

from app.presence.application.dtos import FrequencyInDTO, FrequencyOutDTO, ReadingInDTO,ReadingOutDTO, RegisterSnackInDTO, RegisterSnackOutDTO
from app.presence.domain.repositories import IFrequencyRepository, IReadingRepository, IRegisterSnackRepository
from app.presence.api.schema import RegisterSnackOut
from app.presence.domain.entities import FrequencyEntity, ReadingEntity, RegisterSnackEntity
from app.presence.domain.role import MomentRole, SnackRole

class ReadingRegisterUseCase:
    def __init__(self, reading_repo: IReadingRepository):
        self.reading_repo = reading_repo

    def execute(self, dto: ReadingInDTO) -> ReadingOutDTO:
        if self.reading_repo.very_exists_by_student_id(dto.student):
            raise Exception('Reading already exists')
        
        entity = ReadingEntity(
            student=dto.student,
            moment=dto.moment,
        )

        self.reading_repo.save(entity)
        return ReadingOutDTO.from_domain(entity)

class ReadingResponseUseCase:
    def __init__(self, reading_repo: IReadingRepository):
        self.reading_repo = reading_repo

    def execute(self, id: UUID) -> ReadingOutDTO:
        if not self.reading_repo.very_exists(id):
            raise Exception('No reading found')
        
        return ReadingOutDTO.from_domain(self.reading_repo.find_by_id(id))

class ReadingAllUseCase:
    def __init__(self, reading_repo: IReadingRepository):
        self.reading_repo = reading_repo

    def execute(self) -> List[ReadingOutDTO]:

        return  [ReadingOutDTO.from_domain(entity) for entity in self.reading_repo.list_readings_all()]

class FrequencyRegisterUseCase:
    def __init__(self, frequency_repo: IReadingRepository):
        self.reading_repo = frequency_repo

    def execute(self, dto: FrequencyInDTO) -> FrequencyOutDTO:
        entity = FrequencyEntity(
            student=dto.student,
            date=dto.date,
            on_time=dto.on_time,
            reading=dto.reading
        )

        self.reading_repo.save(entity)

        return FrequencyOutDTO.from_domain(entity)

class FrequencyListAll:
    def __init__(self, frequency_repo: IFrequencyRepository):
        self.reading_repo = frequency_repo

    def execute(self) -> List[FrequencyOutDTO]:
        frequencys = self.reading_repo.list_frequency_all()

        return [FrequencyOutDTO.from_domain(frequency) for frequency in frequencys]

class RegisterSnackRegisterUseCase:
    def __init__(self, register_snack_repo: IRegisterSnackRepository):
        self.register_snack_repo = register_snack_repo

    def execute(self, dto: RegisterSnackInDTO) -> RegisterSnackOutDTO:
        if self.register_snack_repo.very_exist_register_snack_by_student_id(dto.student):
            raise Exception('Register snack already recorded')

        entity = RegisterSnackEntity(
            student=dto.student,
            date=dto.date,
            moment=dto.moment,
            type_snack=dto.type_snack,
            reading=dto.reading
        )

        self.register_snack_repo.save(entity)

        return RegisterSnackOutDTO.from_domain(entity)

class ResponseAllRegisterSnackUseCase:
    def __init__(self, register_snack_repo: IRegisterSnackRepository):
        self.register_snack_repo = register_snack_repo

    def execute(self) -> List[RegisterSnackOut]:
        register_snacks = self.register_snack_repo.list_register_snack_all()

        return [RegisterSnackOutDTO.from_domain(register_snack) for register_snack in register_snacks]

class ResponseRegisterSnackByDateUseCase:
    def __init__(self, register_snack_repo: IRegisterSnackRepository):
        self.register_snack_repo = register_snack_repo

    def execute(self, date: datetime) -> List[RegisterSnackOut]:
        if not date:
            raise Exception('Date not privided.')

        register_snacks = self.register_snack_repo.list_register_snack_by_date(date)

        return [
            RegisterSnackOutDTO.from_domain(register_snack)
            for register_snack in register_snacks
        ]

class ResponseRegisterSnackByMomentUseCase:
    def __init__(self, register_snack_repo: IRegisterSnackRepository):
        self.register_snack_repo = register_snack_repo

    def execute(self, moment: MomentRole) -> List[RegisterSnackOut]:
        if not moment:
            raise Exception('Moment not privided.')

        register_snacks = self.register_snack_repo.list_register_snack_by_moment(moment)

        return [
            RegisterSnackOutDTO.from_domain(register_snack)
            for register_snack in register_snacks
        ]

class ResponseRegisterSnackByTypeSnackUseCase:
    def __init__(self, register_snack_repo: IRegisterSnackRepository):
        self.register_snack_repo = register_snack_repo

    def execute(self, type_snack: SnackRole) -> List[RegisterSnackOut]:
        if not type_snack:
            raise Exception('Date not privided.')

        register_snacks = self.register_snack_repo.list_register_snack_by_type_snack(type_snack)

        return [
            RegisterSnackOutDTO.from_domain(register_snack)
            for register_snack in register_snacks
        ]
