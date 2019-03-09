import logging
from datetime import datetime
import requests
from django_ro import scheduler
from .models import AppServerChannel, AppServerList


logger = logging.getLogger('django')


# 按时开区
def open_by_time(id):
    today = datetime.now().date().strftime('%Y-%m-%d')
    app_server_channel = AppServerChannel.objects.get(id=id)
    app_server_channel.server_statu = 101
    app_server_channel.save()
    app_server_list = AppServerList.objects.get(id=app_server_channel.zoneidx)
    app_server_list.opendate = today
    app_server_list.save()


def open_by_user(id, job_id, open_user):
    app_server_channel = AppServerChannel.objects.get(id=id)
    gid = app_server_channel.gid
    pid = app_server_channel.pid
    app_server_list = AppServerList.objects.get(id=app_server_channel.zoneidx)
    sid = app_server_list.sid

    url = 'http://www.test.com/'
    data = {'gid': gid, 'pid': pid, 'sid': sid}
    response = requests.post(url, data=data)

    if response.json().get('user_amount') >= open_user:

        app_server_channel.server_statu = 101
        app_server_channel.save()

        today = datetime.now().date().strftime('%Y-%m-%d')
        app_server_list.opendate = today
        app_server_list.save()

        try:
            scheduler.remove_job(job_id)
        except:
            print('end')
