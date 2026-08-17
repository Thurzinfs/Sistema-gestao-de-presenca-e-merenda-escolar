from black import mode
from django.db import models
from uuid import uuid4

from  app.presence.domain.role import MomentRole, SnackRole

from app.presence.domain.role import MomentRole


class Readings(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    student = models.ForeignKey(
        'academic.Student', on_delete=models.CASCADE
    )
    moment = models.CharField(
        max_length=20, choices=MomentRole, default=MomentRole.snack_morning
    )

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'readings'

class Frequency(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,default=uuid4)
    student = models.ForeignKey(
        'academic.Student', on_delete=models.CASCADE
    )
    date = models.DateField()
    on_time = models.BooleanField(default=False)
    reading = models.ForeignKey(
        'presence.Readings', on_delete=models.CASCADE
    )
    class Meta:
            db_table = 'frequencys'

class RegisterSnack(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    student = models.ForeignKey(
        'academic.Student', on_delete=models.CASCADE
    )
    date = models.DateField()

    moment = models.CharField(
        max_length=20, choices=MomentRole, default=MomentRole.snack_morning
    )

    type_snack = models.CharField(
        max_length=200, choices=SnackRole, default=SnackRole.normal
    )

    reading = models.ForeignKey(
        'presence.Readings', on_delete=models.CASCADE
    )

    class Meta:
            db_table = 'register_snacks'
