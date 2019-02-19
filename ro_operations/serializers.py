from rest_framework import serializers
from .models import User, AppChannelList, AppManage, AppServerList, AppPlatformCfg, WelfareManagement, RolePlayerManagement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AppChannelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppChannelList
        fields = '__all__'


class AppManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppManage
        fields = '__all__'


class AppPlatformCfgSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppPlatformCfg
        fields = ('idx', 'gid', 'pid', 'pname')


class AppServerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppServerList
        fields = ('id', 'sid', 'sname', 'pid', 'gid')


class WelfareManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelfareManagement
        fields = '__all__'


class RolePlayerManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePlayerManagement
        fields = '__all__'


class ServerTableSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    GID = serializers.IntegerField()
    CID = serializers.IntegerField()
    PID = serializers.IntegerField()
    zonename = serializers.CharField()
    statu = serializers.IntegerField()
    server_statu = serializers.IntegerField()
    server_suggest = serializers.IntegerField()
    is_delete = serializers.IntegerField()
    zoneidx = serializers.IntegerField()
    SID = serializers.IntegerField()
    SName = serializers.CharField()
    DevID = serializers.IntegerField()
    VID = serializers.IntegerField()
    OpenDate = serializers.DateField()
    MergeDate = serializers.DateField()
    MergeID = serializers.IntegerField()
    MergeIdx = serializers.IntegerField()
    ServerID = serializers.IntegerField()
    CT_ipadd = serializers.CharField()
    domain = serializers.CharField()
    appid = serializers.CharField()
    version = serializers.CharField()
    LoginPort = serializers.CharField()
    player_highlines = serializers.IntegerField()
    server_weight = serializers.IntegerField()


# class AppServerChannelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppServerChannel
#         fields = '__all__'
