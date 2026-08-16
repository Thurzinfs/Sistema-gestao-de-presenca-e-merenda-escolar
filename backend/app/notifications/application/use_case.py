from collections import Counter
from typing import List
from uuid import UUID

from django.utils import timezone

from app.notifications.domain.adapters import ITaskSendMessage, IWahaMessageAdapter
from app.notifications.domain.entities import WahaMessageEntity
from app.notifications.domain.repositories import IWhatsAppMessageRepository
from app.presence.domain.role import MomentRole
from app.school.domain.repositories import ISchoolRepository
from app.presence.domain.repositories import IRegisterSnackRepository


class ListSchoolsByTimeAndSendLunchUseCase:
    def __init__(
            self, 
            school_repo: ISchoolRepository, 
            whatsapp_repo: IWhatsAppMessageRepository, 
            sender_message: ITaskSendMessage,
            register_snack_repo: IRegisterSnackRepository
    ):
        self.school_repo = school_repo
        self.whatsapp_repo = whatsapp_repo
        self.sender_message = sender_message
        self.register_snack_repo = register_snack_repo

    def execute(self) -> ...:
        now = timezone.localtime().strftime("%H:%M:%S")
        today = timezone.localdate()

        schools = self.school_repo.list_schools_by_time_send_lunch(now)

        for school in schools:
            for moment, time in [
                (MomentRole.snack_morning, school.time_send_snack_morning),
                (MomentRole.lunch, school.time_send_lunch),
                (MomentRole.snack_afternoon, school.time_send_snack_afternoon),
            ]:
                if time is None or now < time.value.strftime("%H:%M:%S"):
                    continue

                if self.whatsapp_repo.exists_for_today(school.id, moment, today):
                    continue

                registers = self.register_snack_repo.filter_by_school_and_moment(
                    school.id,
                    moment,
                    today,
                )

                counted_by_type = Counter()
                for item in registers:
                    counted_by_type[item.upper()] += 1

                total_students = sum(counted_by_type.values())
                normal_count = counted_by_type.get('NORMAL', 0)
                little_count = counted_by_type.get('LITTLE', 0)

                if moment == MomentRole.snack_morning:
                    texto =  f"""Olá {school.name}! \nSegue o resumo do lanche da manhã de hoje {today.day}/{today.month}/{today.year}: \nTotal de alunos: {total_students}."""

                elif moment == MomentRole.lunch:
                    texto =  f"""Olá {school.name}! \nSegue o resumo do almoço de hoje {today.day}/{today.month}/{today.year}: \nTotal de alunos: {total_students} \nAlunos com almoço normal: {normal_count} \nAlunos com almoço pequeno: {little_count}."""

                elif moment == MomentRole.snack_afternoon:
                    texto =  f"""Olá {school.name}! \nSegue o resumo do lanche da tarde de hoje {today.day}/{today.month}/{today.year}: \nTotal de alunos: {total_students}"""
                

                message = WahaMessageEntity(
                    school=school.id,
                    moment=moment,
                    date=today,
                    number=school.number_whats,  # type: ignore
                    message=texto,
                )
                self.whatsapp_repo.save(message)

                if not school.number_whats:
                    continue

                self.sender_message.send_message(message.id)


class SendMessageToSchoolUseCase:
    def __init__(self, message_repo: IWhatsAppMessageRepository, sender_message: IWahaMessageAdapter):
        self.message_repo = message_repo
        self.sender_message = sender_message

    def execute(self, id: UUID):
        message = self.message_repo.find_by_id(id)
        if not message:
            return

        self.sender_message.send_message(message.number, message.message)
        return message
