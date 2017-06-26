# coding:utf-8
from django.contrib.auth.models import User,Group
from rest_framework import serializers
#序列化
#对User进行序列化
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=('url','username','email','groups')
#对Group进行序列化
class GroupSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Group
        fields=('url','name')