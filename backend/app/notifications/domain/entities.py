from dataclasses import dataclass, field
from uuid import UUID, uuid4

from datetime import datetime, date as Date

from app.notifications.infrastructure.models import StatusMessage


@dataclass
class WahaMessageEntity:
    id: UUID = field(default_factory=uuid4)
    school: UUID | None = field(default=None)
    moment: str | None = field(default=None)
    date: Date | None = field(default=None)
    number: str = field(default='')
    status: str = field(default=StatusMessage.PENDING)
    message: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)

    def change_status(self, new_status: StatusMessage):
        self.status = new_status
