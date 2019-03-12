import logging
from datetime import datetime
from django.db import connections
from django.conf import settings
from django.core.mail import send_mail
import requests
from django_ro import scheduler
from .models import AppServerChannel, AppServerList
from ro_operations.dbtools import dict_fetchall

logger = logging.getLogger('django')


# 按时开区
def open_by_time(id):
    app_server_channel = AppServerChannel.objects.get(id=id)
    server_statu = app_server_channel.server_statu
    gid = app_server_channel.gid
    pid = app_server_channel.pid
    cid = app_server_channel.cid
    appid = app_server_channel.appid
    app_server_list = AppServerList.objects.get(id=app_server_channel.zoneidx)
    sid = app_server_list.sid

    if server_statu > 200:
        today = datetime.now().date().strftime('%Y-%m-%d')
        app_server_channel.open_type = 1
        app_server_channel.server_statu = 101
        app_server_channel.save()

        app_server_list.opendate = today
        app_server_list.save()
        logger.info(
            '执行按时开区任务,{gid}项目{cid}渠道{appid}包{sid}区'.format(gid=gid, cid=cid, appid=appid, sid=app_server_list.sid))
    else:
        logger.info('{gid}项目{cid}渠道{appid}包{sid}区已处于开服状态，不执行按时开区任务'.format(gid=gid, cid=cid, appid=appid,
                                                                         sid=app_server_list.sid))

    # 如果设置了人数上限
    max_user = app_server_channel.max_user
    if max_user:
        # 设置任务id
        job_id = '_'.join(['django_ro_by_user', str(gid), str(cid), str(appid), str(id)])
        # 获取任务
        job_ins = scheduler.get_job(job_id)
        # 如果任务存在,删除
        if job_ins:
            scheduler.remove_job(job_id)
        # 添加人数开区
        scheduler.add_job(func=open_by_user, trigger='interval', id=job_id, args=[id, job_id], seconds=30)
        logger.info('{gid}项目{cid}渠道{appid}包{sid}区已时间开服，且设置人数上限，添加下个区人数开区任务'.format(gid=gid, cid=cid, appid=appid, sid=sid))

        # 查询当前区是否是最后一个区
        try:
            server_management_cursor = connections['server_management'].cursor()
            if appid:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE appid='{appid}' AND SID < 9000".format(
                    cid=cid, appid=appid)
            else:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE SID < 9000".format(
                    cid=cid)
            # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12)"
            # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12) WHERE appid='com.dkm.tlsj.tlsj'"
            # sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTableTest] ({gid}, {cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
            server_management_cursor.execute(sql)
            server_management_result = dict_fetchall(server_management_cursor)
            # 如果此区是当前包下所有区的最后一个区，通知管理新新增区
            if server_management_result[-1].get('id') == id:
                # 邮件通知配置新区
                subject = '游戏新区提前配置预警'
                msg = '{gid}项目{cid}渠道{appid}包{sid}区是最后区，无新区，请配置下一个新区'.format(gid=gid, cid=cid, appid=appid,
                                                                             sid=app_server_list.sid)
                sender = settings.DEFAULT_FROM_EMAIL
                recepients = ['290704731@qq.com', ]
                send_mail(subject=subject, message=msg, from_email=sender, recipient_list=recepients)
                logger.info(msg)
        except Exception as e:
            print(e)
            logger.info('查询是否有新区失败')





def open_by_user(id, job_id):
    app_server_channel = AppServerChannel.objects.get(id=id)
    appid = app_server_channel.appid
    cid = app_server_channel.cid
    gid = app_server_channel.gid
    pid = app_server_channel.pid
    max_user = app_server_channel.max_user
    app_server_list = AppServerList.objects.get(id=app_server_channel.zoneidx)
    sid = app_server_list.sid

    # url = 'http://www.test.com/'
    url = 'http://127.0.0.1:8000/mock_user/'
    data = {'gid': gid, 'pid': pid, 'sid': sid}
    response = requests.post(url, data=data)

    if response.json().get('user_amount') >= max_user:
        # 查询当前区是否是最后一个区
        try:
            server_management_cursor = connections['server_management'].cursor()
            if appid:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE appid='{appid}' AND SID < 9000".format(
                    cid=cid, appid=appid)
            else:
                sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE SID < 9000".format(
                    cid=cid)

            server_management_cursor.execute(sql)
            server_management_result = dict_fetchall(server_management_cursor)
            print(server_management_result)
            # 没有下一个区，无法正常开区
            if server_management_result[-1].get('id') == id:
                # 邮件通知。。。。
                subject = '游戏新区立即开区报警'
                msg = '{gid}项目{cid}渠道{appid}包{sid}区是最后区，无新区，请立即开启下一个新区'.format(gid=gid, cid=cid, appid=appid, sid=sid)
                sender = settings.DEFAULT_FROM_EMAIL
                recepients = ['290704731@qq.com', ]
                send_mail(subject=subject, message=msg, from_email=sender, recipient_list=recepients)
                logger.info(msg)
            # 有下一个区，可以正常开区
            else:
                id_list = [each.get('id') for each in server_management_result]
                print(id_list)
                # 本区索引
                dict_index = id_list.index(id)
                # 下一个区索引
                target_index = dict_index + 1
                # 下一个区信息
                next_zone = server_management_result[target_index]
                # 如果满最大人数且下一个区处于已开状态
                if next_zone.get('server_statu') < 200:
                    logger.info('{gid}项目{cid}渠道{appid}包{sid}区已处于开服状态，不执行人数上限开区任务'
                                .format(gid=next_zone.get('GID'), cid=next_zone.get('CID'),
                                appid=next_zone.get('appid'), sid=next_zone.get('SID')))
                # 满最大人数，且下一个区未开, 执行人数开区操作
                else:
                    next_id = next_zone.get('id')
                    next_app_server_channel = AppServerChannel.objects.get(id=next_id)
                    next_app_server_channel.open_type = 2
                    next_app_server_channel.server_statu = 101
                    next_app_server_channel.save()

                    today = datetime.now().date().strftime('%Y-%m-%d')
                    next_app_server_list = AppServerList.objects.get(id=next_app_server_channel.zoneidx)
                    next_app_server_list.opendate = today
                    next_app_server_list.save()

                # 如果设置了人数上限
                max_user = next_zone.get('max_user')
                if max_user:
                    # 设置任务id
                    job_id = '_'.join(['django_ro_by_user', str(next_zone.get('GID')), str(next_zone.get('CID')), str(next_zone.get('appid')), str(next_zone.get('id'))])
                    # 获取任务
                    job_ins = scheduler.get_job(job_id)
                    # 如果任务存在,删除
                    if job_ins:
                        scheduler.remove_job(job_id)
                    # 添加人数开区
                    scheduler.add_job(func=open_by_user, trigger='interval', id=job_id, args=[id, job_id],
                                      seconds=30)
                    logger.info('{gid}项目{cid}渠道{appid}包{sid}区已人数开服，且设置人数上限，添加下个区人数开区任务'.format(gid=next_zone.get('GID'), cid=next_zone.get('CID'),
                                appid=next_zone.get('appid'), sid=next_zone.get('SID')))

                    # 查询当前区是否是最后一个区
                    try:
                        server_management_cursor = connections['server_management'].cursor()
                        if appid:
                            sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE appid='{appid}' AND SID < 9000".format(
                                cid=next_zone.get('CID'), appid=next_zone.get('appid'))
                        else:
                            sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, {cid}) WHERE SID < 9000".format(
                                cid=next_zone.get('CID'))
                        # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12)"
                        # sql = "SELECT * FROM ServerManagement.dbo.[GetServerTableTest] (50, 12) WHERE appid='com.dkm.tlsj.tlsj'"
                        # sql = "SELECT * FROM ServerManagementRo.dbo.[GetServerTableTest] ({gid}, {cid}) WHERE appid='{appid}'".format(gid=gid, cid=cid, appid=appid)
                        server_management_cursor.execute(sql)
                        server_management_result = dict_fetchall(server_management_cursor)
                        # 如果此区是当前包下所有区的最后一个区，通知管理新新增区
                        if server_management_result[-1].get('id') == id:
                            # 邮件通知配置新区
                            subject = '游戏新区提前配置预警'
                            msg = '{gid}项目{cid}渠道{appid}包{sid}区是最后区，无新区，请配置下一个新区'.format(gid=gid, cid=cid, appid=appid,
                                                                                         sid=app_server_list.sid)
                            sender = settings.DEFAULT_FROM_EMAIL
                            recepients = ['290704731@qq.com', ]
                            send_mail(subject=subject, message=msg, from_email=sender, recipient_list=recepients)
                            logger.info(msg)
                    except Exception as e:
                        print(e)
                        logger.info('查询是否有新区失败')

                try:
                    logger.info('{gid}项目{cid}渠道{appid}包{sid}区已处于开服状态, 尝试删除人数开区任务'.format(gid=next_zone.get('GID'), cid=next_zone.get('CID'),
                                appid=next_zone.get('appid'), sid=next_zone.get('SID')))
                    scheduler.remove_job(job_id)
                except:
                    print('{gid}项目{cid}渠道{appid}包{sid}区已处于开服状态, 删除人数开区任务失败'.format(gid=next_zone.get('GID'), cid=next_zone.get('CID'),
                                appid=next_zone.get('appid'), sid=next_zone.get('SID')))
        except Exception as e:
            print(e)
            logger.info('人数开区任务，查询是否有新区失败')
