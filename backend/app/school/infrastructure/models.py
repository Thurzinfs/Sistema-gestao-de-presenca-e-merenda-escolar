from uuid import uuid4

from django.db import models

from app.school.domain.role import ManagerRole


class School(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=180)
    time_closing_presence = models.TimeField()
    time_send_lunch = models.TimeField()
    time_send_snack_afternoon = models.TimeField()
    number_whats = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = 'schools'


class Manager(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    school_id = models.ForeignKey(
        'school.School',
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=28, choices=ManagerRole, default=ManagerRole.pending)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    password = models.CharField(max_length=220)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'managers'
