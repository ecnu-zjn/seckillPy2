# coding:utf-8
from django.shortcuts import render

# Create your views here.
from django. contrib. auth. models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer,GroupSerializers
from django.http import HttpResponse



def index(request):
    return HttpResponse(u"欢迎进入抢杀！")


class UserViewSet(viewsets.ModelViewSet):
    """
    用户界面
    """
    queryset=User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    组界面
    """
    queryset=Group.objects.all()
    serializer_class = GroupSerializers
