# Generated by Django 2.1.5 on 2019-01-09 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppManage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gametypeno', models.IntegerField(db_column='GameTypeno')),
                ('gametype', models.CharField(db_column='GameType', max_length=50)),
                ('ptid', models.IntegerField(db_column='Ptid')),
                ('channelid', models.IntegerField(blank=True, db_column='ChannelId', null=True)),
                ('appid', models.CharField(db_column='Appid', max_length=50)),
                ('appname', models.CharField(db_column='Appname', max_length=50)),
                ('callbackurl', models.CharField(blank=True, db_column='CallbackUrl', max_length=50, null=True)),
                ('os', models.IntegerField(blank=True, null=True)),
                ('lable', models.CharField(blank=True, max_length=50, null=True)),
                ('mix', models.IntegerField(blank=True, null=True)),
                ('app_parameter', models.CharField(blank=True, max_length=1000, null=True)),
                ('del_field', models.IntegerField(db_column='del')),
            ],
            options={
                'db_table': 'app_manage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniconid', models.CharField(blank=True, max_length=50, null=True)),
                ('gametypeno', models.IntegerField()),
                ('pid', models.IntegerField(blank=True, null=True)),
                ('truezoneid', models.IntegerField()),
                ('tradeid', models.IntegerField(blank=True, null=True)),
                ('server_id', models.IntegerField()),
                ('server_name', models.CharField(blank=True, max_length=50, null=True)),
                ('server_status', models.IntegerField(blank=True, null=True)),
                ('server_address', models.CharField(blank=True, max_length=50, null=True)),
                ('server_suggest', models.IntegerField(blank=True, null=True)),
                ('statu', models.IntegerField(blank=True, null=True)),
                ('del_field', models.IntegerField(blank=True, db_column='del', null=True)),
                ('kaiqu_time', models.CharField(blank=True, max_length=50, null=True)),
                ('listver', models.CharField(blank=True, db_column='Listver', max_length=50, null=True)),
                ('listvertest', models.CharField(blank=True, db_column='ListVerTest', max_length=50, null=True)),
                ('max_users', models.IntegerField(blank=True, null=True)),
                ('server_weight', models.IntegerField(blank=True, null=True)),
                ('plan_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Server_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VersionInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appidx', models.IntegerField()),
                ('gametypeno', models.IntegerField()),
                ('ptid', models.IntegerField()),
                ('appid', models.CharField(db_column='Appid', max_length=50)),
                ('version', models.CharField(db_column='Version', max_length=50)),
                ('channelid', models.IntegerField(blank=True, db_column='ChannelId', null=True)),
                ('statu', models.IntegerField()),
                ('ondate', models.DateField(blank=True, db_column='onDate', null=True)),
                ('offdate', models.DateField(blank=True, db_column='offDate', null=True)),
                ('cdn', models.CharField(blank=True, db_column='CDN', max_length=250, null=True)),
                ('testcdn', models.CharField(blank=True, db_column='TESTCDN', max_length=250, null=True)),
                ('appurl', models.CharField(blank=True, max_length=250, null=True)),
                ('testappurl', models.CharField(blank=True, db_column='TestAppurl', max_length=250, null=True)),
                ('cashurl', models.CharField(blank=True, db_column='Cashurl', max_length=250, null=True)),
                ('info', models.CharField(blank=True, db_column='Info', max_length=50, null=True)),
                ('noticeid', models.CharField(blank=True, db_column='Noticeid', max_length=50, null=True)),
                ('testnoticeid', models.CharField(blank=True, db_column='TESTNoticeid', max_length=50, null=True)),
                ('prevnoticeid', models.CharField(blank=True, db_column='PREVNoticeid', max_length=50, null=True)),
                ('isdel', models.IntegerField()),
                ('iosshenhe', models.IntegerField(blank=True, db_column='IosShenhe', null=True)),
            ],
            options={
                'db_table': 'Version_info',
                'managed': False,
            },
        ),
    ]
