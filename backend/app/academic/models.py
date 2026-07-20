from uuid import uuid4

from django.db import models


class Classroom(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'classrooms'


class Student(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    classroom = models.ForeignKey(
        'academic.Classroom', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=190)
    RA = models.CharField(max_length=40)
    qr_code = models.CharField(max_length=80)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'students'
