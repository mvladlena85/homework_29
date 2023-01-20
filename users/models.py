from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class User(models.Model):
    ROLES = [('member', 'пользователь'), ('moderator', 'модератор'), ('admin', 'администратор')]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLES, default="member")
    age = models.SmallIntegerField()
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']


