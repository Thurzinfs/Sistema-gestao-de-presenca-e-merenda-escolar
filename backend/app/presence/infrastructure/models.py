from django.db import models
from uuid import uuid4

from  app.presence.domain.role import MomentRole

class Readings(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    student_id = models.ForeignKey(

    )
    moment = models.CharField(
        max_length=20, choices=MomentRole, default=MomentRole.snack_morning
    )

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'readings'

