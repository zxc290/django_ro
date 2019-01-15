import json
import time
from django.shortcuts import render
from django.conf import settings
from django.db import connections
from rest_framework.decorators import api_view
from rest_framework.response import Response
from itsdangerous import TimedJSONWebSignatureSerializer
from .models import User, AppChannelList, AppServerChannel, AppManage
# Create your views here.


def dict_fetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def gen_json_web_token(user_info):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 8 * 60 * 60)
    timestamp = time.time()
    user_info['iat'] = timestamp
    token = s.dumps(user_info)
    return token


def verify_token(token):
    s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 8 * 60 * 60)
    try:
        user_auth = s.loads(token)
    except:
        return
    if ('user_id' not in user_auth) or ('username' not in user_auth):
        return
    return user_auth


@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.objects.get(useridentity=username, password=password)
        with connections['default'].cursor() as admin_cursor:
            # sql = "SELECT * FROM dbo.NAuth({user_id}, 2) WHERE PID > 0 AND AID=50".format(user_id=user.userid)
            sql = "SELECT DISTINCT CID FROM dbo.NAuth(27, 2) WHERE PID > 0 AND AID=50 AND FID=4"
            # sql = "SELECT * FROM dbo.NAuth({user_id}, 2) WHERE PID > 0 AND AID=50 AND FID IN {fid_permission} ".format(user_id=user.userid, fid_permission=settings.FID_PERMISSION)
            admin_cursor.execute(sql)
            admin_db_result = dict_fetchall(admin_cursor)
        if not admin_db_result:
            message = '该用户没有此权限'
            return Response({'code': 0, 'message': message})

        permission_dict = dict()
        result = admin_db_result[0]

        permission_dict['uid'] = result.get('UID')
        permission_dict['aid'] = result.get('AID')
        permission_dict['cid'] = result.get('CID')
        permission_dict['pid'] = result.get('PID')
        permission_dict['fid'] = result.get('FID')
        permission_dict['gname'] = result.get('GName')
        permission_dict['pname'] = result.get('PName')
        permission_dict['fname'] = result.get('FName')

        user_info = dict()
        user_info['user_id'] = user.userid
        user_info['username'] = username
        user_info['permission'] = permission_dict

        token = gen_json_web_token(user_info)
        message = '登录成功'
        return Response({'code': 1, 'username': username, 'token': token, 'message': message})
    except:
        message = '用户名或密码错误'
        return Response({'code': 0, 'message': message})


@api_view(['POST'])
def get_channel_list(request):
    data = json.loads(request.body)
    gid = data.get('gid')
    cid = data.get('cid')
    if cid > 0:
        channel_list = AppChannelList.objects.filter(gid=gid, cid=cid)
    else:
        channel_list = AppChannelList.objects.filter(gid=gid)
    # cid = data.get('cid')
    # channel_list = AppChannelList.objects.filter(gid=gid, cid=cid)
    channel_dict = {each.cid: each.cname for each in channel_list}
    return Response(channel_dict)


@api_view(['POST'])
def get_appid_list(request):
    data = json.loads(request.body)
    gid = data.get('gid')
    cid = data.get('cid')
    appid_list = AppManage.objects.filter(gametypeno=gid, channelid=cid)
    appid_dict = {each.appname: each.appid for each in appid_list}
    return Response(appid_dict)


@api_view(['POST'])
def get_server_table(request):
    data = json.loads(request.body)
    gid = data.get('gid')
    cid = data.get('cid')
    appid = data.get('appid')

    try:
        admin_cursor = connections['default'].cursor()
        sql = "SELECT * FROM ServerManagement.dbo.[GetServerTable] ({gid},{cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
        admin_cursor.execute(sql)
        admin_db_result = dict_fetchall(admin_cursor)
        server_list = []
        for each in admin_db_result:
            pass

    except:
        message = '服务器列表查询失败'
        return Response({'code': 0, 'message': message})

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
# a = {'user_id': 28, 'username': 'guchengdong', 'permission': {50: {'GName': '仙境传说', 1: {'PName': '畅梦测试', 100: {'FName': '分时段数据'}, 107: {'FName': '客服查询'}, 4: {'FName': '渠道管理'}, 75: {'F
# Name': '汇总'}, 76: {'FName': '罗盘'}, 77: {'FName': '注册收入比'}, 78: {'FName': 'LTV'}, 79: {'FName': '运营数据分析'}, 80: {'FName': '前端点击功能'}, 81: {'FName': '产出消耗汇总'}, 88: {'FName': '元
# 宝消耗'}, 89: {'FName': '元宝商城'}, 90: {'FName': '绑定元宝消耗'}, 91: {'FName': '绑定元宝商城'}, 92: {'FName': '特殊道具使用销售'}, 93: {'FName': '特殊道具产出'}, 94: {'FName': '寻宝'}, 95: {'FName'
# : '地图传送统计'}, 96: {'FName': '平台最高在线'}, 97: {'FName': '各时间段消费比例'}, 98: {'FName': '在线人数分析'}, 99: {'FName': '在线时长'}, 101: {'FName': '等级分布'}, 102: {'FName': '转生等级分布'
# }, 103: {'FName': '收入分析'}, 104: {'FName': '付费构成'}, 106: {'FName': '激活用户'}, 108: {'FName': '充值排行'}, 109: {'FName': '充值金额查询'}, 110: {'FName': '充值记录'}, 111: {'FName': '各渠道新
# 增充值'}, 112: {'FName': '消费记录'}, 114: {'FName': '活动数据查询'}, 115: {'FName': '元宝消耗排行'}, 116: {'FName': '玩家角色账号互查'}, 117: {'FName': '基本信息'}, 118: {'FName': '死亡记录'}, 119: {
# 'FName': '任务记录'}, 120: {'FName': '元宝记录(点数变化)'}, 121: {'FName': '物品记录'}, 122: {'FName': '升级记录'}, 123: {'FName': '道具交易'}, 124: {'FName': '邮件信息'}, 125: {'FName': 'Boss掉落'},
# 128: {'FName': '激活码查询'}, 129: {'FName': '战斗力排行'}, 135: {'FName': '玩家登录信息'}, 136: {'FName': '合区列表'}, 138: {'FName': '金币记录'}, 139: {'FName': '绑金记录'}, 140: {'FName': '绑元记录
# '}, 141: {'FName': '在线分析'}, 146: {'FName': '配置区服信息'}, 148: {'FName': '手游管理(渠道)'}, 149: {'FName': '包管理(渠道)'}, 150: {'FName': '公告管理(渠道)'}, 151: {'FName': '区服管理(渠道)'}, 15
# 8: {'FName': '留存分析'}, 162: {'FName': '行会公告'}}}}
