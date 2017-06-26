# coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from seckill.models import ExposedNoOpen,ExposedOpen,Exposed
from seckill.models import Seckill,SuccessKilled
from seckill.serializers import SeckillSerializer
from seckill.serializers import SuccessKilledSerializer,ExposedNoIdSerializer,ExposedNoOpenSerializer,ExposedOpenSerializer
import time
from getMd5 import getMd5
import json
import datetime
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

# class JSONResponse(HttpResponse):
#     """
#     """
#     def __init__(self,data,**kwargs):
#         content=JSONRenderer().render(data)
#         kwargs['content_type']='application/json'
#         super(JSONResponse,self).__init__(content,**kwargs)

# @csrf_exempt
# def SeckillList(request):
#     """
#
#     :param request:
#     :return:
#     """
#     if request.method == 'GET':
#         seckills=Seckill.objects.all()
#         serializer=SeckillSerializer(seckills,many=True)
#         return JsonResponse(serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         data=JSONParser().parse(request)
#         serializer=SeckillSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


#抢杀商品的显示和新建
class SeckillList(generics.ListCreateAPIView):
    queryset = Seckill.objects.all()
    serializer_class = SeckillSerializer




# @csrf_exempt
# def seckill_detail(request,pk):
#     """
#     :param request:
#     :param seckill_id:
#     :return:
#     """
#     if pk == None:
#         return HttpResponseRedirect("list")
#     try:
#         seckill=Seckill.objects.get(seckill_id=pk)
#     except Seckill.DoesNotExist:
#         return HttpResponseRedirect("list")
#
#     if request.method == 'GET':
#         serializer=SeckillSerializer(seckill)
#         return JsonResponse(serializer.data)



#抢杀商品的详细信息
class seckill_detail(viewsets.ViewSet):
    def retrieve(self, request,pk=None):
        queryset = Seckill.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = SeckillSerializer(user)
        return Response(serializer.data)

#显示当前时间
@api_view(['GET'])
def seckill_time(request):
        now=datetime.datetime.fromtimestamp(time.time())
        now={"now":now}
        return Response(now)



#暴露url
@api_view(['GET'])
def expose_url(request,pk):
    try:
       seckill = Seckill.objects.get(seckill_id=pk)
    except:
        return Response(ExposedNoIdSerializer(Exposed(exposed=False,seckill_id=pk)).data)

    now=datetime.datetime.fromtimestamp(time.time())
    start=seckill.start_time.replace(tzinfo=None)
    end=seckill.end_time.replace(tzinfo=None)
    print now,start,end
    if start > now or end < now:
        nowStr=now.strftime('%Y-%m-%d %H:%M:%S')
        staStr = start.strftime('%Y-%m-%d %H:%M:%S')
        endStr = end.strftime('%Y-%m-%d %H:%M:%S')
        return Response(ExposedNoOpenSerializer(ExposedNoOpen(exposed=False,seckill_id=pk,now=nowStr,start=staStr,end=endStr)).data)
    md5=getMd5(pk)
    print ExposedOpenSerializer(ExposedOpen(exposed=True, seckill_id=pk, md5=md5)).data
    try:
       return Response(ExposedOpenSerializer(ExposedOpen(exposed=True,seckill_id=pk,md5=md5)).data)
    except:
        return Response({'error':'暴露失败！'})

@csrf_exempt
def set_phone(request):
    if request.method == 'POST':
        phone=request.POST.get('phone','')
        request.session['phone']=phone
        return HttpResponseRedirect('./kill')
    else:
        return HttpResponse("set failure.")


@api_view(['GET','POST'])
def killone(request):
    """
    :param request:
    :return:
    """
    if request.method == 'GET':
        successKilled=SuccessKilled.objects.all()
        serializer=SuccessKilledSerializer(successKilled,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
            print request.data
            user_phone = long(request.data['user_phone'])
            seckill_id = long(request.data['seckill_id'])

            if user_phone!=request.session.get('phone',''):
                print request.session.get('phone','')
                return Response({'message':'电话号码不对'})

            if seckill_id not in [i.seckill_id for i in Seckill.objects.all()]:
                print seckill_id==1000L
                print [i.seckill_id for i in Seckill.objects.all()]
                return Response({'message':'秒杀商品不存在'})

            seckill = Seckill.objects.get(seckill_id=seckill_id)
            if datetime.datetime.fromtimestamp( time.time())<seckill.start_time.replace(tzinfo=None):
                return Response({'message':'还未开始'})
            if datetime.datetime.fromtimestamp(time.time()) > seckill.end_time.replace(tzinfo=None):
                return Response({'message':'已经结束'})

            idstr = [str(i.seckill_id) for i in SuccessKilled.objects.all()]
            phstr = [str(i.user_phone) for i in SuccessKilled.objects.all()]
            if str(user_phone)+str(seckill_id) not in [phstr[i]+idstr[i] for i in range(len(phstr))]:
                seckill.number=seckill.number-1
                seckill.save()
                obj=SuccessKilled(seckill_id=seckill_id, user_phone=user_phone,state=1,create_time=seckill.create_time)
                return Response({'mesage':'抢杀成功'})
            else:
                return Response({'message':'重复秒杀'})
