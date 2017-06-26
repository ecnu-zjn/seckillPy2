# coding:utf-8
"""seckillPy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from userAdmin.views import UserViewSet,GroupViewSet,index
from seckill.views import SeckillList,seckill_detail,seckill_time,expose_url,set_phone,killone
from rest_framework import routers
router=routers.DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'groups',GroupViewSet)
user_detail = seckill_detail.as_view({'get': 'retrieve'})

urlpatterns = [
    url(r'^$', index,name='welcome'),
    url(r'^admin/', admin.site.urls),
    url(r'^ctr/',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest-framework')),
    url(r'^seckill/list$', SeckillList.as_view()),
    url(r'^seckill/(?P<pk>[0-9]+)/detail$', user_detail),
    url(r'^seckill/time/now$', seckill_time),
    url(r'^seckill/(?P<pk>[0-9]+)/url$', expose_url),
    url(r'^seckill/setphone$', set_phone),
    url(r'^seckill/kill$', killone),
]
