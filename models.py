# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AppPlatformCfg(models.Model):
    idx = models.AutoField()
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    pname = models.CharField(db_column='PName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True)  # Field name made lowercase.
    offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'App_Platform_cfg'
