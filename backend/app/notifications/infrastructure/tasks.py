from uuid import UUID

from celery import shared_task

from app.notifications.infrastructure.models import StatusMessage
from app.notifications.infrastructure.repository import DjangoWhatsAppMessageRepository
from config import settings


@shared_task(name='verify_school_send_report')
def verify_school_send_report():
    from app.notifications.application.use_case import ListSchoolsByTimeAndSendLunchUseCase
    from app.notifications.infrastructure.adapters import TaskSendMessageAdapter
    from app.notifications.infrastructure.repository import DjangoWhatsAppMessageRepository

    from app.school.infrastructure.repository import DjangoSchoolRepository

    school_repo = DjangoSchoolRepository()
    whatsapp_repo = DjangoWhatsAppMessageRepository()
    task_adapter = TaskSendMessageAdapter()

    use_case = ListSchoolsByTimeAndSendLunchUseCase(
        school_repo=school_repo, 
        whatsapp_repo=whatsapp_repo, 
        sender_message=task_adapter
    )

    use_case.execute()


@shared_task
def send_message_to_school(id: UUID):
    message = None
    try:
        from app.notifications.application.use_case import SendMessageToSchoolUseCase
        from app.notifications.infrastructure.adapters import WahaMessageAdapter

        sender_message = WahaMessageAdapter(base_url=settings.WAHA_URL, session=settings.WAHA_SESSION)
        message_repo = DjangoWhatsAppMessageRepository()
        use_case = SendMessageToSchoolUseCase(sender_message=sender_message, message_repo=message_repo)

        message = use_case.execute(id)
        if message is not None:
            message.change_status(StatusMessage.READY)
            message_repo.save(message)

    except Exception as e:
        if message is not None:
            message.change_status(StatusMessage.FAILED)
            message_repo.save(message)

        raise e
    