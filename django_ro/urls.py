"""django_ro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from ro_operations.views import login, user_permission, server_list, test1
from ro_operations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login', views.login),
    path('app_platforms', views.AppPlatformCfgList.as_view()),
    path('app_servers', views.AppServerListList.as_view()),
    path('app_channels/', views.AppChannelListList.as_view()),
    path('app_server_channels/', views.AppServerChannelList.as_view()),
    # path('app_server_channels/<int:id>/', views.AppServerChannelDetail.as_view()),
    path('app_managements/', views.AppManageList.as_view()),
    path('welfares/', views.WelfareManagementList.as_view()),
    path('welfares/<int:id>/', views.WelfareManagementDetail.as_view()),
    path('role_players/', views.RolePlayerManagementList.as_view()),
    path('role_players/<int:id>/', views.RolePlayerManagementDetail.as_view()),
    path('server_managements/', views.ServerManagementList.as_view()),
    path('recommend_server_managements/', views.RecommendServerList.as_view()),
    path('set_open_plan/<int:id>/', views.set_open_plan),
    path('delete_open_plan/<int:id>/', views.delete_open_plan),
    path('change_recommend/<int:id>/', views.change_recommend),
    path('open_now/<int:id>/', views.open_now),
    path('mock_user/', views.mock_user)
]

