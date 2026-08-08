from uuid import uuid4

from django.db import models

from app.presence.domain.role import MomentRole


class StatusMessage(models.TextChoices):
    PENDING = "pending", "Pendente"
    READY = "ready", "Enviada"
    FAILED = "failed", "Falha"


class WhatsAppMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    school = models.ForeignKey('school.School', on_delete=models.PROTECT)
    moment = models.CharField(max_length=20, choices=MomentRole)
    date = models.DateField()
    number = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=StatusMessage.choices, default=StatusMessage.PENDING)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'whatsapp_message'
