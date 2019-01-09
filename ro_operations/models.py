# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .model_managers import AppManagementManager


class AppManage(models.Model):
    # id = models.AutoField()
    gametypeno = models.IntegerField(db_column='GameTypeno', verbose_name='游戏类型id')  # Field name made lowercase.
    gametype = models.CharField(db_column='GameType', max_length=50, verbose_name='游戏类型')  # Field name made lowercase.
    ptid = models.IntegerField(db_column='Ptid', verbose_name='平台id')  # Field name made lowercase.
    channelid = models.IntegerField(db_column='ChannelId', blank=True, null=True, verbose_name='渠道id')  # Field name made lowercase.
    appid = models.CharField(db_column='Appid', max_length=50, verbose_name='appid')  # Field name made lowercase.
    appname = models.CharField(db_column='Appname', max_length=50, verbose_name='app名称')  # Field name made lowercase.
    callbackurl = models.CharField(db_column='CallbackUrl', max_length=50, blank=True, null=True, verbose_name='回调url')  # Field name made lowercase.
    os = models.IntegerField(blank=True, null=True, verbose_name='os')
    lable = models.CharField(max_length=50, blank=True, null=True, verbose_name='标签')
    mix = models.IntegerField(blank=True, null=True, verbose_name='mix')
    app_parameter = models.CharField(max_length=1000, blank=True, null=True, verbose_name='app参数')
    del_field = models.IntegerField(db_column='del', verbose_name='删除')  # Field renamed because it was a Python reserved word.

    objects = AppManagementManager()

    def __str__(self):
        return self.appid

    class Meta:
        verbose_name = 'APP管理'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'app_manage'


class ServerList(models.Model):
    # id = models.AutoField()
    uniconid = models.CharField(max_length=50, blank=True, null=True, verbose_name='uniconid')
    gametypeno = models.IntegerField(verbose_name='游戏类型id')
    pid = models.IntegerField(blank=True, null=True, verbose_name='平台id')
    truezoneid = models.IntegerField(verbose_name='真实区id')
    # tradeid = models.IntegerField(blank=True, null=True,)
    server_id = models.IntegerField(verbose_name='服务器id')
    server_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='服务器名称')
    server_status = models.IntegerField(blank=True, null=True, verbose_name='服务器状态')
    server_address = models.CharField(max_length=50, blank=True, null=True, verbose_name='服务器地址')
    server_suggest = models.IntegerField(blank=True, null=True, verbose_name='服务器推荐')
    statu = models.IntegerField(blank=True, null=True, verbose_name='状态')
    del_field = models.IntegerField(db_column='del', blank=True, null=True, verbose_name='删除')  # Field renamed because it was a Python reserved word.
    kaiqu_time = models.CharField(max_length=50, blank=True, null=True, verbose_name='开区时间')
    # listver = models.CharField(db_column='Listver', max_length=50, blank=True, null=True)  # Field name made lowercase.
    # listvertest = models.CharField(db_column='ListVerTest', max_length=50, blank=True, null=True)  # Field name made lowercase.
    max_users = models.IntegerField(blank=True, null=True, verbose_name='最大用户数')
    server_weight = models.IntegerField(blank=True, null=True, verbose_name='服务器权重')
    plan_time = models.DateTimeField(blank=True, null=True, verbose_name='计划开区时间')

    objects = AppManagementManager()

    def __str__(self):
        return self.uniconid

    class Meta:
        verbose_name = '服务器列表'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'Server_list'


class VersionInfo(models.Model):
    # id = models.AutoField()
    appidx = models.IntegerField(verbose_name='appidx')
    gametypeno = models.IntegerField(verbose_name='游戏类型id')
    ptid = models.IntegerField(verbose_name='平台id')
    appid = models.CharField(db_column='Appid', max_length=50, verbose_name='appid')  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=50, verbose_name='版本')  # Field name made lowercase.
    channelid = models.IntegerField(db_column='ChannelId', blank=True, null=True, verbose_name='渠道id')  # Field name made lowercase.
    statu = models.IntegerField(verbose_name='状态')
    ondate = models.DateField(db_column='onDate', blank=True, null=True, verbose_name='开启时间')  # Field name made lowercase.
    offdate = models.DateField(db_column='offDate', blank=True, null=True, verbose_name='关闭时间')  # Field name made lowercase.
    cdn = models.CharField(db_column='CDN', max_length=250, blank=True, null=True, verbose_name='cdn')  # Field name made lowercase.
    testcdn = models.CharField(db_column='TESTCDN', max_length=250, blank=True, null=True, verbose_name='测试cdn')  # Field name made lowercase.
    # cdn�Ƿ�Ͷ��ʹ�� = models.IntegerField(db_column='CDN�Ƿ�Ͷ��ʹ��', blank=True, null=True)  # Field name made lowercase.
    # cdn�Ƿ�ʹ��https = models.IntegerField(db_column='CDN�Ƿ�ʹ��https', blank=True, null=True)  # Field name made lowercase.
    appurl = models.CharField(max_length=250, blank=True, null=True, verbose_name='appurl')
    testappurl = models.CharField(db_column='TestAppurl', max_length=250, blank=True, null=True, verbose_name='测试appurl')  # Field name made lowercase.
    cashurl = models.CharField(db_column='Cashurl', max_length=250, blank=True, null=True, verbose_name='现金url')  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=50, blank=True, null=True, verbose_name='信息')  # Field name made lowercase.
    noticeid = models.CharField(db_column='Noticeid', max_length=50, blank=True, null=True, verbose_name='通知id')  # Field name made lowercase.
    testnoticeid = models.CharField(db_column='TESTNoticeid', max_length=50, blank=True, null=True, verbose_name='测试通知id')  # Field name made lowercase.
    prevnoticeid = models.CharField(db_column='PREVNoticeid', max_length=50, blank=True, null=True, verbose_name='上一个通知id')  # Field name made lowercase.
    isdel = models.IntegerField(verbose_name='是否删除')
    iosshenhe = models.IntegerField(db_column='IosShenhe', blank=True, null=True, verbose_name='ios审核')  # Field name made lowercase.

    objects = AppManagementManager()

    def __str__(self):
        return str(self.gametypeno) + '_' + self.appid + '_' + self.version

    class Meta:
        verbose_name = '版本信息'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'Version_info'


class User(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True, verbose_name='用户id')
    useridentity = models.CharField(db_column='userIdentity', max_length=50, verbose_name='用户身份')
    password = models.CharField(db_column='passWord', max_length=50, blank=True, null=True, verbose_name='密码')
    emailaddress = models.CharField(db_column='emailAddress', max_length=32, blank=True, null=True, verbose_name='邮件地址')
    # phonenumber = models.CharField(db_column='phoneNumber', max_length=11, blank=True, null=True)
    # ipaddress = models.CharField(db_column='ipAddress', max_length=16, blank=True, null=True)
    # mac = models.CharField(max_length=32, blank=True, null=True)
    # username = models.CharField(db_column='userName', max_length=50, blank=True, null=True)
    # admin = models.IntegerField(blank=True, null=True)
    # failcount = models.IntegerField(db_column='failCount', blank=True, null=True)
    # lastlogintime = models.IntegerField(db_column='lastLoginTime', blank=True, null=True)
    # token = models.CharField(max_length=32, blank=True, null=True)

    # objects = UserWithEmailManager()

    def __str__(self):
        return self.useridentity

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'User'