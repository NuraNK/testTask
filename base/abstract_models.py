from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField("Создано", auto_now_add=True)
    modified = models.DateTimeField("Изменено", auto_now=True)

    class Meta:
        abstract = True
