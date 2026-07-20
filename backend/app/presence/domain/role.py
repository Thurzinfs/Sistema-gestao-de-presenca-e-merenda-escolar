from django.db import models

class MomentRole(models.TextChoices):
    snack_morning = 'SNACK_MORNING', 'snack_morning'
    lunch = 'LUNCH', 'lunch'
    snack_afternoon = 'SNACK_AFTERNOON', 'snack_afternoon'