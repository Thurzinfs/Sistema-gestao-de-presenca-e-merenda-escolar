from uuid import UUID

import requests

from app.notifications.domain.adapters import ITaskSendMessage, IWahaMessageAdapter
from app.notifications.infrastructure.tasks import send_message_to_school
from config import settings

from app.notifications.infrastructure.tasks import send_message_to_school


class WahaMessageAdapter(IWahaMessageAdapter):
    def __init__(self, base_url: str, session: str) -> None:
        self.base_url = base_url

        self.session = session

        self.http = requests.Session()
        self.http.headers.update({'X-Api-Key': settings.WAHA_API_KEY})

    def send_message(self, number: str, message: str):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sendText',
                json={
                    'chatId': f'{number}@c.us',
                    'text': message,
                    'session': self.session,
                },
            )
            print(
                f'[DEBUG] status={response.status_code} body={response.text}'
            )

            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def create_session(self):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sessions', json={'name': self.session}
            )
            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def start_session(self):
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/sessions/{self.session}/start',
                json={'session': self.session},
            )
            response.raise_for_status()
        except requests.ConnectTimeout as e:
            raise e

    def get_session_status(self):
        try:
            response = self.http.get(
                url=f'{self.base_url}/api/sessions/{self.session}',
                json={'session': self.session},
            )
            if response.status_code == 404:
                return None
            return response.json().get('status')
        except requests.ConnectTimeout as e:
            raise e

    def get_login_qrcode(self):
        try:
            response = self.http.get(
                url=f'{self.base_url}/api/{self.session}/auth/qr',
                params={'format': 'image'},
            )
            response.raise_for_status()
            return response.content

        except requests.ConnectTimeout as e:
            raise e

    def send_code_for_login_waha(
        self, phone: str
    ) -> dict | None:
        try:
            response = self.http.post(
                url=f'{self.base_url}/api/{self.session}/auth/request-code',
                json={'phoneNumber': phone},
            )
            response.raise_for_status()
            return response.json()

        except requests.ConnectTimeout as e:
            raise e


class TaskSendMessageAdapter(ITaskSendMessage):
    def send_message(self, id: UUID):
        send_message_to_school.delay(id)
        