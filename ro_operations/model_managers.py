from django.db import models


class AppManagementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('appid_management')


# class ServerListManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().using('appid_management')
#
#
# class AppManageManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().using('appid_management')