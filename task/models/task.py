from django.db import models

from base.abstract_models import TimeStampedModel


class Task(TimeStampedModel):
    owner = models.ForeignKey(
        "user.user",
        on_delete=models.CASCADE,
        related_name="owner_task",
        verbose_name="Владелец задачи"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок задачи"
    )
    description = models.TextField(
        verbose_name="Описание задачи"
    )
    is_done = models.BooleanField(
        default=False,
        verbose_name="Выполнено"
    )
    execution_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Срок выполнение"
    )

    def __str__(self):
        return "{} {} {}".format(self.id, self.title, self.owner)
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"