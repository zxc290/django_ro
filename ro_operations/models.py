# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import hashlib
from django.db import models, connections
from django.conf import settings
from .model_managers import AppManagementManager, ServerManagementManager, DjangoRoManager
from .dbtools import dict_fetchall


class AppManage(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id')
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
    sync = models.BooleanField(db_column='sync', verbose_name='是否同步')
    # sync = models.IntegerField(db_column='sync', verbose_name='同步')

    objects = AppManagementManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'APP管理'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'app_manage'


class ServerList(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
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
    id = models.AutoField(primary_key=True, verbose_name='id')
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
        return self.id

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
    phonenumber = models.CharField(db_column='phoneNumber', max_length=11, blank=True, null=True)
    ipaddress = models.CharField(db_column='ipAddress', max_length=16, blank=True, null=True)
    mac = models.CharField(max_length=32, blank=True, null=True)
    username = models.CharField(db_column='userName', max_length=50, blank=True, null=True)
    admin = models.IntegerField(blank=True, null=True)
    failcount = models.IntegerField(db_column='failCount', blank=True, null=True)
    lastlogintime = models.IntegerField(db_column='lastLoginTime', blank=True, null=True)
    token = models.CharField(max_length=32, blank=True, null=True)

    # objects = UserWithEmailManager()

    def check_password(self, password):
        return hashlib.md5(password.encode()).hexdigest().upper() == self.password

    def get_user_permission(self):
        sql = "SELECT * FROM dbo.NAuth({user_id}, {function_id}) WHERE PID > 0".format(user_id=self.userid, function_id=settings.FUNCTION_ID)
        try:
            admin_cursor = connections['default'].cursor()
            admin_cursor.execute(sql)
            result = dict_fetchall(admin_cursor)
            return result
        except:
            return False

    def __str__(self):
        return self.useridentity

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'User'


class AppPlatformCfg(models.Model):
    idx = models.IntegerField(primary_key=True)
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    pname = models.CharField(db_column='PName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    createdate = models.DateField(db_column='CreateDate', blank=True, null=True)  # Field name made lowercase.
    onlinedate = models.DateField(db_column='OnlineDate', blank=True, null=True)  # Field name made lowercase.
    offlinedate = models.DateField(db_column='OfflineDate', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(db_column='Company', max_length=50, blank=True, null=True)  # Field name made lowercase.

    objects = ServerManagementManager()

    def __str__(self):
        return self.idx

    class Meta:
        verbose_name = '平台配置'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'App_Platform_cfg'


class AppServerList(models.Model):
    sid = models.IntegerField(db_column='SID', blank=True, null=True)  # Field name made lowercase.
    sname = models.CharField(db_column='SName', max_length=512, blank=True, null=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    apid = models.IntegerField(db_column='APID', blank=True, null=True)  # Field name made lowercase.
    display = models.IntegerField(db_column='Display', blank=True, null=True)  # Field name made lowercase.
    devid = models.IntegerField(db_column='DevID', blank=True, null=True)  # Field name made lowercase.
    dn = models.CharField(db_column='DN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    vid = models.IntegerField(db_column='VID', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    prostatus = models.IntegerField(db_column='ProStatus', blank=True, null=True)  # Field name made lowercase.
    opendate = models.DateField(db_column='OpenDate')  # Field name made lowercase.
    mergedate = models.DateField(db_column='MergeDate')  # Field name made lowercase.
    mergeid = models.IntegerField(db_column='MergeID')  # Field name made lowercase.
    mergeidx = models.IntegerField(db_column='MergeIdx')  # Field name made lowercase.
    serverid = models.IntegerField(db_column='ServerID', blank=True, null=True)  # Field name made lowercase.
    gslist = models.CharField(db_column='GSList', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbsvr_in = models.CharField(db_column='DBSvr_in', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbname_in = models.CharField(db_column='DBName_in', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbqueryid_in = models.IntegerField(db_column='DBQueryId_in', blank=True, null=True)  # Field name made lowercase.
    dbsvr_out = models.CharField(db_column='DBSvr_out', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbname_out = models.CharField(db_column='DBName_out', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dbqueryid_out = models.IntegerField(db_column='DBQueryId_out', blank=True, null=True)  # Field name made lowercase.
    serverpath = models.CharField(db_column='ServerPath', max_length=50, blank=True, null=True)  # Field name made lowercase.
    smport = models.IntegerField(db_column='SMPort')  # Field name made lowercase.
    loginport = models.CharField(db_column='LoginPort', max_length=50, blank=True, null=True)  # Field name made lowercase.
    rmbport = models.IntegerField(db_column='RmbPort', blank=True, null=True)  # Field name made lowercase.
    db_svrcfg = models.CharField(max_length=50, blank=True, null=True)
    db_player = models.CharField(max_length=50, blank=True, null=True)
    db_login = models.CharField(max_length=50, blank=True, null=True)
    db_super = models.CharField(max_length=50, blank=True, null=True)
    db_rmb = models.CharField(max_length=50, blank=True, null=True)
    db_param = models.CharField(max_length=50, blank=True, null=True)
    trigger_flag = models.CharField(max_length=50, blank=True, null=True)

    objects = ServerManagementManager()

    class Meta:
        managed = False
        db_table = 'App_Server_list'
        unique_together = (('sid', 'pid', 'gid'),)


class AppChannelList(models.Model):
    cid = models.IntegerField(db_column='CID', primary_key=True)  # Field name made lowercase.
    cname = models.CharField(db_column='CName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cinfo = models.CharField(db_column='CInfo', max_length=512, blank=True, null=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    gid = models.IntegerField(db_column='GID', blank=True, null=True)  # Field name made lowercase.
    pcid = models.IntegerField(db_column='PCID', blank=True, null=True)  # Field name made lowercase.

    objects = ServerManagementManager()

    def __str__(self):
        return self.cname

    class Meta:
        verbose_name = '渠道'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'App_Channel_list'


class AppServerChannel(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='id')
    gid = models.IntegerField(db_column='GID')  # Field name made lowercase.
    zoneidx = models.IntegerField()
    zonename = models.CharField(max_length=50, blank=True, null=True)
    pid = models.IntegerField(db_column='PID', blank=True, null=True)  # Field name made lowercase.
    cid = models.IntegerField(db_column='CID')  # Field name made lowercase.
    appid = models.CharField(max_length=50, blank=True, null=True)
    # version = models.CharField(max_length=50, blank=True, null=True)
    statu = models.IntegerField()
    server_statu = models.IntegerField()
    server_suggest = models.IntegerField()
    is_delete = models.IntegerField()
    open_type = models.IntegerField(blank=True, null=True)
    open_time = models.IntegerField(blank=True, null=True)
    max_user = models.IntegerField(blank=True, null=True)
    server_weight = models.IntegerField(blank=True, null=True)
    weight_deadline = models.CharField(max_length=50, blank=True, null=True)

    objects = ServerManagementManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '应用服务渠道'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'App_Server_Channel'


class WelfareManagement(models.Model):
    pid = models.IntegerField(verbose_name='游戏平台id')
    pname = models.CharField(max_length=100, verbose_name='游戏平台名')
    zid = models.IntegerField(verbose_name='游戏区服id')
    zname = models.CharField(max_length=100, verbose_name='游戏区服名')
    role_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='申请角色名')
    amount = models.IntegerField(verbose_name='申请数额')
    is_regular = models.BooleanField(default=False, verbose_name='是否固定发放')
    regular_period = models.IntegerField(null=True, verbose_name='固定发放周期')
    applicant_id = models.IntegerField(verbose_name='申请人id')
    applicant_name = models.CharField(max_length=100, verbose_name='申请人')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    status = models.IntegerField(default=0, verbose_name='审核状态')
    approver_id = models.IntegerField( blank=True, null=True, verbose_name='审批人id')
    approver_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='审核人')
    approve_date = models.DateTimeField(null=True, verbose_name='审核时间')

    objects = DjangoRoManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '福利发放管理'
        verbose_name_plural = verbose_name


class RolePlayerManagement(models.Model):
    pid = models.IntegerField(verbose_name='游戏平台id')
    pname = models.CharField(max_length=100, verbose_name='游戏平台名')
    zid = models.IntegerField(verbose_name='游戏区服id')
    zname = models.CharField(max_length=100, verbose_name='游戏区服名')
    role_name = models.CharField(max_length=100, verbose_name='角色名')
    user_name = models.CharField(max_length=100, verbose_name='使用人姓名')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    modify_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    creator_id = models.IntegerField(verbose_name='创建者id')
    creator_name = models.CharField(max_length=100, verbose_name='创建者姓名')

    objects = DjangoRoManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '人员角色管理'
        verbose_name_plural = verbose_name

