from abc import ABC, abstractmethod
from typing import Any, List
from uuid import UUID


class IWahaMessageAdapter(ABC):
    @abstractmethod
    def send_message(self, number: str, message: str):
        ...

    @abstractmethod
    def create_session(self):
        ...

    @abstractmethod
    def start_session(self):
        ...

    @abstractmethod
    def get_session_status(self):
        ...

    @abstractmethod
    def get_login_qrcode(self):
        ...

    @abstractmethod
    def send_code_for_login_waha(self, phone: str) -> dict | None:
        ...


class ITaskSendMessage(ABC):
    @abstractmethod
    def send_message(self, id: UUID):
        ...
