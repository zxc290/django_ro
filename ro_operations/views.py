import json
import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.conf import settings
from django.db import connections
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from itsdangerous import TimedJSONWebSignatureSerializer
from .models import User, AppChannelList, AppManage, AppServerList, AppPlatformCfg, WelfareManagement, RolePlayerManagement
from .serializers import UserSerializer, AppChannelListSerializer, AppManageSerializer, AppServerListSerializer, AppPlatformCfgSerializer, WelfareManagementSerializer, RolePlayerManagementSerializer
from django.contrib.auth.decorators import login_required
from .tokens import gen_json_web_token
from .decorators import token_required
from .dbtools import dict_fetchall
# Create your views here.



# @api_view(['POST'])
# def login(request):
#     data = JSONParser().parse(request)
#     # data = json.loads(request.body)
#     username = data.get('username')
#     password = data.get('password')
#     try:
#         user = User.objects.get(useridentity=username, password=password)
#         user_info = dict()
#         user_info['userid'] = user.userid
#         user_info['username'] = user.useridentity
#         token = gen_json_web_token(user_info)
#         message = '登录成功'
#         return Response({'code': 1, 'message': message, 'user_id': user.userid, 'username': user.useridentity, 'token': token})
#     except:
#         message = '用户名或密码错误'
#         return Response({'code': 0, 'message': message})


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

            # if user_info.get('is_applicant') == user_info.get('is_approver') == True:
            #     # 提审 审核无法共存，此时应禁止登陆
            #     pass

            token = gen_json_web_token(user_info)
            message = '登录成功'
            # logger.info('登录成功')
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
        print(e)
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
# @token_required
def server_list(request):
    data = JSONParser().parse(request)
    gid = data.get('gid')
    cid = data.get('cid')
    appid = data.get('appid')
    if request.method == 'POST':
        try:
            server_management_cursor = connections['server_management'].cursor()
            sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTable] (51, 1) WHERE appid='com.dkm.tlsj.tlsj'"
            # sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTable] ({gid}, {cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
            server_management_cursor.execute(sql)
            server_management_db_result = dict_fetchall(server_management_cursor)
            # server_list = JSONRenderer().render(server_management_db_result)
            # print(type(server_list))
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
        return Response(serializer.data)


class AppServerListList(APIView):
    '''
    列出所有的AppServer
    '''
    def get(self, request, format=None):
        app_server_list =  AppServerList.objects.all()
        serializer = AppServerListSerializer(app_server_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @method_decorator(token_required, name='dispatch')
class WelfareManagementList(APIView):
    '''
    列出所有的WelfareManagement或新增一个Welfare
    '''
    @token_required
    def get(self, request, format=None):
        welfare_managements =  WelfareManagement.objects.all()
        serializer = WelfareManagementSerializer(welfare_managements, many=True)
        return Response(serializer.data)

    @token_required
    def post(self, request, format=None):
        data = request.data
        print(data)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(token_required, name='dispatch')
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
        print(data)
        now = datetime.now()
        data.update(approver_id=approver_id, approver_name=approver_name, approve_date=now)
        serializer = WelfareManagementSerializer(welfare_management, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def delete(self, request, id, format=None):
        welfare_management = self.get_object(id)
        if welfare_management.status == 0:
            welfare_management.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = '只能撤销审核中的申请'
            return Response(message, status=status.HTTP_202_ACCEPTED)


# @method_decorator(token_required, name='dispatch')
class RolePlayerManagementList(APIView):
    '''
    列出所有的RolePlayerManagement或新增一个RolePlayerManagement
    '''
    @token_required
    def get(self, request, format=None):
        role_player_list = RolePlayerManagement.objects.all()
        serializer = RolePlayerManagementSerializer(role_player_list, many=True)
        return Response(serializer.data)

    @token_required
    def post(self, request, format=None):
        data = request.data
        print(data)
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
            return Response(message, status=status.HTTP_202_ACCEPTED)

        data.update(pname=pname, zname=zname, creator_name=creator_name)

        serializer = RolePlayerManagementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(token_required, name='dispatch')
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
        print(data)
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
            return Response(message, status=status.HTTP_202_ACCEPTED)

        data.update(pname=pname, zname=zname, creator_name=creator_name)
        serializer = RolePlayerManagementSerializer(role_player, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def delete(self, request, id, format=None):
        role_player = self.get_object(id)
        role_player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['POST'])
# def login(request):
#     data = json.loads(request.body)
#     username = data.get('username')
#     password = data.get('password')
#
#     try:
#         user = User.objects.get(useridentity=username, password=password)
#         with connections['default'].cursor() as admin_cursor:
#             # sql = "SELECT * FROM dbo.NAuth({user_id}, 2) WHERE PID > 0 AND AID=50".format(user_id=user.userid)
#             sql = "SELECT DISTINCT CID FROM dbo.NAuth(27, 2) WHERE PID > 0 AND AID=50 AND FID=4"
#             # sql = "SELECT * FROM dbo.NAuth({user_id}, 2) WHERE PID > 0 AND AID=50 AND FID IN {fid_permission} ".format(user_id=user.userid, fid_permission=settings.FID_PERMISSION)
#             admin_cursor.execute(sql)
#             admin_db_result = dict_fetchall(admin_cursor)
#         if not admin_db_result:
#             message = '该用户没有此权限'
#             return Response({'code': 0, 'message': message})
#
#         permission_dict = dict()
#         result = admin_db_result[0]
#
#         permission_dict['uid'] = result.get('UID')
#         permission_dict['aid'] = result.get('AID')
#         permission_dict['cid'] = result.get('CID')
#         permission_dict['pid'] = result.get('PID')
#         permission_dict['fid'] = result.get('FID')
#         permission_dict['gname'] = result.get('GName')
#         permission_dict['pname'] = result.get('PName')
#         permission_dict['fname'] = result.get('FName')
#
#         user_info = dict()
#         user_info['user_id'] = user.userid
#         user_info['username'] = username
#         user_info['permission'] = permission_dict
#
#         token = gen_json_web_token(user_info)
#         message = '登录成功'
#
#         app_manages = AppManage.objects.all()
#         app_manages_serializer = AppManageSerializer(app_manages, many=True)
#         # app_server_channels = AppServerChannel.objects.all()
#         # app_server_channels_serializer = AppServerChannelSerializer(app_server_channels, many=True)
#
#         app_channel_list = AppChannelList.objects.all()
#         app_channel_list_serializer = AppChannelListSerializer(app_channel_list, many=True)
#
#         return Response({
#             'code': 1,
#             'username': username,
#             'token': token,
#             'message': message,
#             'app_manages': app_manages_serializer.data,
#             'app_channel_list': app_channel_list_serializer.data
#         })
#     except:
#         message = '用户名或密码错误'
#         return Response({'code': 0, 'message': message})


# @api_view(['POST'])
# def get_channel_list(request):
#     data = json.loads(request.body)
#     gid = data.get('gid')
#     cid = data.get('cid')
#     if cid > 0:
#         channel_list = AppChannelList.objects.filter(gid=gid, cid=cid)
#     else:
#         channel_list = AppChannelList.objects.filter(gid=gid)
#     # cid = data.get('cid')
#     # channel_list = AppChannelList.objects.filter(gid=gid, cid=cid)
#     channel_dict = {each.cid: each.cname for each in channel_list}
#     return Response(channel_dict)
#
#
# @api_view(['POST'])
# def get_appid_list(request):
#     data = json.loads(request.body)
#     gid = data.get('gid')
#     cid = data.get('cid')
#     appid_list = AppManage.objects.filter(gametypeno=gid, channelid=cid)
#     appid_dict = {each.appname: each.appid for each in appid_list}
#     return Response(appid_dict)


# @api_view(['POST'])
# def get_server_table(request):
#     data = json.loads(request.body)
#     gid = data.get('gid')
#     cid = data.get('cid')
#     appid = data.get('appid')
#
#     try:
#         admin_cursor = connections['default'].cursor()
#         sql = "SELECT * FROM ServerManagement.dbo.[GetServerTable] ({gid},{cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
#         admin_cursor.execute(sql)
#         admin_db_result = dict_fetchall(admin_cursor)
#         server_list = []
#         for each in admin_db_result:
#             pass
#
#     except:
#         message = '服务器列表查询失败'
#         return Response({'code': 0, 'message': message})



@api_view(['GET', 'POST'])
@token_required
def test1(request):
    if request.method == 'GET':
        print('333')
        app_manages = AppManage.objects.all()
        app_manages_serializer = AppManageSerializer(app_manages, many=True)
        return Response(app_manages_serializer.data)
    elif request.method == 'POST':
        print('222')
        return Response({'t': 't1'})


@token_required
def test2(request):
    return Response({'t2': 't2'})


    # with connections['default'].cursor() as admin_cursor:
    #     admin_cursor.execute(
    #         "SELECT * FROM dbo.[User] WHERE userIdentity='{username}' AND passWord='{password}'".format(
    #             username=username, password=password))
    #     admin_db_result = dict_fetchall(admin_cursor)
    #     logger.info('查询登录用户')
    #
    #     if admin_db_result:
    #         user = admin_db_result[0]
    #         user_id = user.get('userId')
    #         username = user.get('userIdentity')
    #
    #         sql = "SELECT * FROM dbo.NAuth({user_id}, 5) WHERE PID > 0 and FID IN {fid_permission}".format(user_id=user_id, fid_permission=settings.FID_PERMISSION)
    #         admin_cursor.execute(sql)
    #         admin_db_result = dict_fetchall(admin_cursor)
    #         logger.info('查询用户权限')
    #
    #         if not admin_db_result:
    #             message = '该用户没有此权限'
    #             logger.info('登录用户无权限')
    #             return Response({'code': 0, 'message': message})
    #
    #         permission_dict = dict()
    #         for each in admin_db_result:
    #             aid = each.get('AID')
    #             pid = each.get('PID')
    #             fid = each.get('FID')
    #             gname = each.get('GName')
    #             pname = each.get('PName')
    #             fname = each.get('FName')
    #             if aid not in permission_dict:
    #                 permission_dict[aid] = {
    #                     'GName': gname,
    #                     pid: {
    #                         'PName': pname,
    #                         fid: {
    #                             'FName': fname
    #                         }
    #                     }
    #                 }
    #             else:
    #                 if pid not in permission_dict[aid]:
    #                     permission_dict[aid][pid] = {
    #                         'PName': pname,
    #                         fid: {
    #                             'FName': fname
    #                         }
    #                     }
    #                 else:
    #                     if fid not in permission_dict[aid][pid]:
    #                         permission_dict[aid][pid][fid] = {
    #                             'FName': fname
    #                         }
    #
    #         user_info = dict()
    #         user_info['user_id'] = user_id
    #         user_info['username'] = username
    #         user_info['permission'] = permission_dict
    #
    #         token = gen_json_web_token(user_info)
    #         message = '登录成功'
    #         logger.info('登录成功')
    #         return Response({'code': 1, 'username': username, 'token': token, 'message': message})
    #     else:
    #         message = '用户名或密码错误'
    #         logger.info('用户名或密码错误，登录失败')
    #         return Response({'code': 0, 'message': message})

