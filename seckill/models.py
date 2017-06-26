# coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#商品信息
class Seckill(models.Model):
    seckill_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=120)
    number = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    create_time = models.DateTimeField()

    def __unicode__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'seckill'

#抢杀记录
class SuccessKilled(models.Model):
    id = models.BigIntegerField(primary_key=True)
    seckill_id = models.BigIntegerField()
    user_phone = models.BigIntegerField()
    state = models.IntegerField()
    create_time = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'success_killed'

# class Exposed(object):
#     def __init__(self,exposed,seckill_id):
#         self.exposed = exposed
#         self.seckill_id = seckill_id
#     class Meta:
#         abstract = True
#
# class ExposedNoId(Exposed):
#     def __init__(self,exposed,seckill_id):
#         Exposed.__init__(self,exposed,seckill_id)
#     class Meta:
#         abstract = True
# class ExposedNoOpen(Exposed):
#     def __init__(self,exposed,seckill_id,now,start,end):
#         Exposed.__init__(self,exposed,seckill_id)
#         self.now=now
#         self.start=start
#         self.end=end
#     class Meta:
#         abstract = True
#
# class ExposedOpen(Exposed):
#     def __init__(self,exposed,seckill_id,md5):
#         Exposed.__init__(self,exposed,seckill_id)
#         self.md5=md5
#     class Meta:
#         abstract = True


#暴露url
#商品不存在时
class Exposed(models.Model):
    exposed=models.BooleanField()
    seckill_id=models.BigIntegerField()

#枪杀未开放时
class ExposedNoOpen(Exposed):
    now =  models.DateTimeField()
    start = models.DateTimeField()
    end = models.DateTimeField()

#md可暴露
class ExposedOpen(Exposed):
    md5= models.CharField(max_length=100)
