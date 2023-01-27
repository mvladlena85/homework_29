from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class User(AbstractUser):
    ROLES = [('member', 'пользователь'), ('moderator', 'модератор'), ('admin', 'администратор')]

    role = models.CharField(max_length=20, choices=ROLES, default="member")
    age = models.SmallIntegerField(blank=True, null=True)
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']


