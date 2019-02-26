import logging
from datetime import datetime, timedelta
from django.db import connections
from django.http import Http404
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import User, AppChannelList, AppManage, AppServerList, AppPlatformCfg, AppServerChannel, WelfareManagement, RolePlayerManagement
from .serializers import UserSerializer, AppChannelListSerializer, AppManageSerializer, AppServerListSerializer, AppPlatformCfgSerializer, AppServerChannelSerializer, AppServerChannelUpdateSerializer ,ServerManagementSerializer, WelfareManagementSerializer, RolePlayerManagementSerializer
from .tokens import gen_json_web_token
from .decorators import token_required
from .dbtools import dict_fetchall
# Create your views here.

logger = logging.getLogger('django')


def index(request):
    return render(request, 'index.html')


@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    now = datetime.now()
    try:
        user = User.objects.get(useridentity=username)
        user.lastlogintime = int(now.timestamp())
        if user.check_password(password):
            user.failcount = 0
            user.save()

            user_info = dict()
            user_info['user_id'] = user.userid
            user_info['username'] = user.useridentity
            user_info['is_applicant'] = True if user.is_applicant() else False
            user_info['is_approver'] = True if user.is_approver() else False
            user_info['is_role_manager'] = True if user.is_role_manager() else False
            user_info['is_record_checker'] = True if user.is_record_checker() else False

            token = gen_json_web_token(user_info)
            message = '登录成功'
            logger.info('登录成功')
            return Response({'code': 1, 'user_info': user_info, 'token': token, 'message': message})
        else:
            last_login_time = datetime.fromtimestamp(user.lastlogintime)
            past_time = now - last_login_time
            if past_time > timedelta(hours=1):
                user.failcount = 0
            user.failcount += 1
            user.save()
            if user.failcount >= 5:
                message = '用户冻结中，请稍后重试'
            else:
                message = '密码错误，剩余{0}次尝试次数'.format(str(5 - user.failcount))
            return Response({'code': 0, 'message': message})
    except BaseException as e:
        message = '该用户不存在'
        return Response({'code': 0, 'message': message})


@api_view(['GET'])
@token_required
def user_permission(request, id):
    try:
        user = User.objects.get(userid=id)
    except:
        message = '用户不存在'
        return Response({'code': 0, 'message': message})

    if request.method == 'GET':
        # uid, aid, fid = id, 50, 4
        try:
            admin_cursor = connections['default'].cursor()
            sql = "SELECT * FROM dbo.NAuth({uid}, 2) WHERE PID > 0 AND AID=50 AND FID=4".format(uid=id)
            admin_cursor.execute(sql)
            admin_db_result = dict_fetchall(admin_cursor)
            cid = admin_db_result[0]['CID']
            if cid > 0:
                channel = AppChannelList.objects.filter(cid=cid, gid=50)
                channel_serializer = AppChannelListSerializer(channel, many=True)
                app = AppManage.objects.filter(channelid=cid, gametypeno=50)
                app_serializer = AppManageSerializer(app, many=True)
            else:
                channel = AppChannelList.objects.filter(gid=50)
                channel_serializer = AppManageSerializer(channel, many=True)
                app = AppManage.objects.filter(gametypeno=50)
                app_serializer = AppManageSerializer(app, many=True)
            message = '获取权限成功'
            return Response({'code': 1, 'message': message, 'channel_list': channel_serializer.data, 'app_list': app_serializer.data})
        except:
            message = '用户权限查询错误'
            return Response({'code': 0, 'message': message})


@api_view(['POST'])
def server_list(request):
    data = JSONParser().parse(request)
    gid = data.get('gid')
    cid = data.get('cid')
    appid = data.get('appid')
    if request.method == 'POST':
        try:
            server_management_cursor = connections['server_management'].cursor()
            sql = "SELECT * FROM ServerManagement.dbo.[GetServerTable] (51, 1) WHERE appid='com.dkm.tlsj.tlsj'"
            # sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTable] ({gid}, {cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
            server_management_cursor.execute(sql)
            server_management_db_result = dict_fetchall(server_management_cursor)
            message = '查询成功'
            return Response({'code':1, 'message': message, 'server_list': server_management_db_result})
        except:
            message = '查询失败'
            return Response({'code': 0, 'message': message})


class AppPlatformCfgList(APIView):
    '''
    列出所有的AppPlatformCfg
    '''
    def get(self, request, format=None):
        app_platform_cfg =  AppPlatformCfg.objects.all()
        serializer = AppPlatformCfgSerializer(app_platform_cfg, many=True)
        logger.info('获取游戏平台配置列表')
        return Response(serializer.data)


class AppServerListList(APIView):
    '''
    列出所有的AppServer
    '''
    def get(self, request, format=None):
        app_server_list =  AppServerList.objects.all()
        serializer = AppServerListSerializer(app_server_list, many=True)
        logger.info('获取游戏服务器列表')
        return Response(serializer.data)


class AppChannelListList(APIView):
    '''
    列出所有的AppChannel
    '''
    def get(self, request, format=None):
        # app_channel_list =  AppChannelList.objects.all()
        app_channel_list =  AppChannelList.objects.all().filter(gid=50)
        serializer = AppChannelListSerializer(app_channel_list, many=True)
        logger.info('获取应用渠道列表')
        return Response(serializer.data)


class ServerManagementList(APIView):
    '''
    列出所有的ServerManagement或新增一个ServerManagement
    '''
    # @token_required
    def get(self, request, format=None):
        data = request.GET
        cid = data.get('cid')
        appid = data.get('appid')
        print(cid, appid)

        try:
            server_management_cursor = connections['server_management'].cursor()
            if appid:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE appid='{appid}'".format(cid=cid, appid=appid)
            else:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid})".format(cid=cid)
            # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12)"
            # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12) WHERE appid='com.dkm.tlsj.tlsj'"
            # sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTableTest] ({gid}, {cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
            server_management_cursor.execute(sql)
            server_management_result = dict_fetchall(server_management_cursor)
            print(server_management_result[0])
            serializer = ServerManagementSerializer(server_management_result, many=True)
            logger.info('获取服务器管理列表成功')
            return Response(serializer.data)
        except Exception as e:
            print(e)
            message = '获取服务器管理列表失败'
            logger.info(message)
            return Response(message)


class AppManageList(APIView):
    '''
    列出所有的AppManage
    '''
    def get(self, request, format=None):
        app_manage_list = AppManage.objects.all().filter(gametypeno=50)
        serializer = AppManageSerializer(app_manage_list, many=True)
        logger.info('获取应用服务器渠道列表')
        return Response(serializer.data)


class AppServerChannelList(APIView):
    '''
    列出所有的AppServerChannel
    '''
    def get(self, request, format=None):
        app_server_channel_list = AppServerChannel.objects.all().filter(gid=50)
        serializer = AppServerChannelSerializer(app_server_channel_list, many=True)
        logger.info('获取应用服务器渠道列表')
        return Response(serializer.data)


class AppServerChannelDetail(APIView):
    """
    检索，更新或删除一个AppServerChannel
    """
    def get_object(self, id):
        try:
            return AppServerChannel.objects.get(id=id)
        except AppServerChannel.DoesNotExist:
            raise Http404

    # def get_object_list(self, appid):
    #     return AppServerChannel.objects.filter(appid=appid)

    def put(self, request, id, format=None):
        data = request.data
        by_zone = data.get('by_zone')
        app_server_channel = self.get_object(id)
        # 如果是按区更新，多条更新
        if by_zone:
            zoneidx = app_server_channel.zoneidx
            app_server_channel_list = AppServerChannel.objects.filter(zoneidx=zoneidx)
            for each in app_server_channel_list:
                # 更新序列器
                update_serializer = AppServerChannelUpdateSerializer(each, data=data)
                if update_serializer.is_valid():
                    update_serializer.save()
                    logger.info('更新多条应用服务器之一成功, id为{each_id}'.format(each_id=each.id))
                else:
                    print(update_serializer.errors)
                    logger.info('更新多条应用服务器之一失败, id为{each_id}'.format(each_id=each.id))
                    return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # 获取序列器
            serializer = AppServerChannelSerializer(app_server_channel_list, many=True)
            logger.info('更新多条应用服务器成功')
            return Response(serializer.data)

        else:
            # 更新序列器
            update_serializer = AppServerChannelUpdateSerializer(app_server_channel, data=data)
            if update_serializer.is_valid():
                update_serializer.save()
                logger.info('更新单条应用服务器成功')
                # 获取序列器
                serializer = AppServerChannelSerializer(app_server_channel)
                print('222')
                print(serializer.data)
                print('333')
                return Response(serializer.data)
            print(update_serializer.errors)
            logger.info('更新单条应用服务器失败')
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        app_server_channel = self.get_object(id)
        app_server_channel.delete()
        logger.info('删除应用服务器成功')
        return Response(status=status.HTTP_204_NO_CONTENT)
        # if welfare_management.status == 0:
        #     welfare_management.delete()
        #     logger.info('删除福利管理成功')
        #     return Response(status=status.HTTP_204_NO_CONTENT)
        # else:
        #     message = '只能撤销审核中的申请'
        #     logger.info('删除福利管理失败')
        #     return Response(message, status=status.HTTP_202_ACCEPTED)


# class ServerManagementDetail(APIView):
#     """
#     检索，更新或删除一个ServerManagement
#     """
#     def get_object(self, id):
#         try:
#             server_management_cursor = connections['server_management'].cursor()
#             sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12) WHERE id='{id}'".format(id=id)
#             server_management_cursor.execute(sql)
#             server_management_result = dict_fetchall(server_management_cursor)
#             if server_management_result:
#                 return server_management_result[0]
#             else:
#                 raise Http404
#         except:
#             raise Http404
#
#     @token_required
#     def put(self, request, id, format=None):
#         welfare_management = self.get_object(id)
#         data = request.data
#         approver_id = data.get('approver_id')
#         approver_name = User.objects.get(userid=approver_id).username
#         now = datetime.now()
#         data.update(approver_id=approver_id, approver_name=approver_name, approve_date=now)
#         serializer = WelfareManagementSerializer(welfare_management, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             logger.info('修改福利管理成功')
#             return Response(serializer.data)
#         logger.info('修改福利管理失败')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @token_required
#     def delete(self, request, id, format=None):
#         welfare_management = self.get_object(id)
#         if welfare_management.status == 0:
#             welfare_management.delete()
#             logger.info('删除福利管理成功')
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             message = '只能撤销审核中的申请'
#             logger.info('删除福利管理失败')
#             return Response(message, status=status.HTTP_202_ACCEPTED)


class WelfareManagementList(APIView):
    '''
    列出所有的WelfareManagement或新增一个WelfareManagement
    '''
    @token_required
    def get(self, request, format=None):
        welfare_managements =  WelfareManagement.objects.all()
        serializer = WelfareManagementSerializer(welfare_managements, many=True)
        logger.info('获取福利管理列表')
        return Response(serializer.data)

    @token_required
    def post(self, request, format=None):
        data = request.data
        pid = data.get('pid')
        zid = data.get('zid')
        applicant_id = data.get('applicant_id')
        is_regular = data.get('is_regular')
        regular_period = data.get('regular_period')

        pname = AppPlatformCfg.objects.get(gid=50, pid=pid).pname
        zname = AppServerList.objects.get(gid=50, pid=pid, sid=zid).sname
        applicant_name = User.objects.get(userid=applicant_id).username

        # 判断是否常规发放，决定是否传入固定周期字段
        if is_regular:
            data.update(pname=pname, zname=zname, applicant_name=applicant_name, regular_period=regular_period)
        else:
            data.update(pname=pname, zname=zname, applicant_name=applicant_name)
        serializer = WelfareManagementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('新增福利管理成功')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info('新增福利管理失败')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WelfareManagementDetail(APIView):
    """
    检索，更新或删除一个WelfareManagement
    """
    def get_object(self, id):
        try:
            return WelfareManagement.objects.get(id=id)
        except WelfareManagement.DoesNotExist:
            raise Http404

    @token_required
    def put(self, request, id, format=None):
        welfare_management = self.get_object(id)
        data = request.data
        approver_id = data.get('approver_id')
        approver_name = User.objects.get(userid=approver_id).username
        now = datetime.now()
        data.update(approver_id=approver_id, approver_name=approver_name, approve_date=now)
        serializer = WelfareManagementSerializer(welfare_management, data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('修改福利管理成功')
            return Response(serializer.data)
        logger.info('修改福利管理失败')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def delete(self, request, id, format=None):
        welfare_management = self.get_object(id)
        if welfare_management.status == 0:
            welfare_management.delete()
            logger.info('删除福利管理成功')
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = '只能撤销审核中的申请'
            logger.info('删除福利管理失败')
            return Response(message, status=status.HTTP_202_ACCEPTED)


class RolePlayerManagementList(APIView):
    '''
    列出所有的RolePlayerManagement或新增一个RolePlayerManagement
    '''
    @token_required
    def get(self, request, format=None):
        role_player_list = RolePlayerManagement.objects.all()
        serializer = RolePlayerManagementSerializer(role_player_list, many=True)
        logger.info('获取人员角色管理列表')
        return Response(serializer.data)

    @token_required
    def post(self, request, format=None):
        data = request.data
        pid = data.get('pid')
        zid = data.get('zid')
        creator_id = data.get('creator_id')
        role_name = data.get('role_name')

        pname = AppPlatformCfg.objects.get(gid=50, pid=pid).pname
        zname = AppServerList.objects.get(gid=50, pid=pid, sid=zid).sname
        creator_name = User.objects.get(userid=creator_id).username

        is_existed = RolePlayerManagement.objects.filter(pid=pid, zid=zid, role_name=role_name).exists()
        if is_existed:
            message = '该人员角色已存在，请勿重复添加'
            logger.info('人员角色重复，添加失败')
            return Response(message, status=status.HTTP_202_ACCEPTED)

        data.update(pname=pname, zname=zname, creator_name=creator_name)

        serializer = RolePlayerManagementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('添加人员角色成功')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info('添加人员角色失败')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RolePlayerManagementDetail(APIView):
    """
    检索，更新或删除一个WelfareManagement
    """
    def get_object(self, id):
        try:
            return RolePlayerManagement.objects.get(id=id)
        except RolePlayerManagement.DoesNotExist:
            raise Http404

    @token_required
    def put(self, request, id, format=None):
        role_player = self.get_object(id)
        data = request.data
        pid = data.get('pid')
        zid = data.get('zid')
        creator_id = data.get('creator_id')
        role_name = data.get('role_name')

        pname = AppPlatformCfg.objects.get(gid=50, pid=pid).pname
        zname = AppServerList.objects.get(gid=50, pid=pid, sid=zid).sname
        creator_name = User.objects.get(userid=creator_id).username

        is_existed = RolePlayerManagement.objects.filter(pid=pid, zid=zid, role_name=role_name).exclude(id=id).exists()
        if is_existed:
            # role_player_obj = RolePlayerManagement.objects.get(pid=pid, zid=zid, role_name=role_name, user_name=user_name)
            # if role_player_obj.is_active == is_active:
            message = '已有用户使用此角色'
            logger.info('人员角色重复，修改失败')
            return Response(message, status=status.HTTP_202_ACCEPTED)

        data.update(pname=pname, zname=zname, creator_name=creator_name)
        serializer = RolePlayerManagementSerializer(role_player, data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info('修改人员角色成功')
            return Response(serializer.data)
        logger.info('修改人员角色失败')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def delete(self, request, id, format=None):
        role_player = self.get_object(id)
        role_player.delete()
        logger.info('删除人员角色成功')
        return Response(status=status.HTTP_204_NO_CONTENT)
