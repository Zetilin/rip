from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Reactor(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="default.png", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    fuel = models.CharField(blank=True)

    def get_image(self):
        return self.image.url.replace("minio", "localhost", 1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Реактор"
        verbose_name_plural = "Реакторы"
        db_table = "reactors"


class Station(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален')
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", null=True, related_name='moderator')

    name = models.CharField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Аэс №" + str(self.pk)

    def get_reactors(self):
        return [
            setattr(item.reactor, "value", item.value) or item.reactor
            for item in ReactorStation.objects.filter(station=self)
        ]

    class Meta:
        verbose_name = "Аэс"
        verbose_name_plural = "Аэс"
        ordering = ('-date_formation',)
        db_table = "stations"


class ReactorStation(models.Model):
    reactor = models.ForeignKey(Reactor, models.DO_NOTHING, blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "reactor_station"
        unique_together = ('reactor', 'station')
