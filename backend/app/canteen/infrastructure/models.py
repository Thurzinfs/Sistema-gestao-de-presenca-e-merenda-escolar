from django.db import models
from uuid import uuid4


class DailyMenu(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE)
    date = models.DateField()
    main_course = models.TextField(max_length=1024)
    manager = models.ForeignKey('school.Manager', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_menu'
