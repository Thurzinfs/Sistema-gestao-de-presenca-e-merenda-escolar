from django.db import models


class ManagerRole(models.TextChoices):
    pending = 'PENDING', 'pending'
    direction = 'DIRECTION', 'direction'
    coordinator = 'COORDINATOR', 'coordinator'
    monitor = 'MONITOR', 'monitor'
    canteen = 'CANTEEN', 'canteen'
