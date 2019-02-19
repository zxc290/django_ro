from django.db import models


class AppManagementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('appid_management')


class ServerManagementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('server_management')


class DjangoRoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('django_ro')