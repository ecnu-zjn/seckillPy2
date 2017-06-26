from rest_framework import serializers

from seckill.models import Seckill, SuccessKilled,Exposed,ExposedNoOpen,ExposedOpen


class SeckillSerializer(serializers.ModelSerializer):
     class Meta:
         model=Seckill
         fields=('seckill_id','name','number','start_time','end_time','create_time')


class SuccessKilledSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessKilled
        fields = ('seckill_id', 'user_phone', 'state', 'create_time')

class ExposedNoIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposed
        fields = ('exposed', 'seckill_id')

class ExposedNoOpenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExposedNoOpen
        fields = ('exposed', 'seckill_id', 'now', 'start','end')

class ExposedOpenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExposedOpen
        fields = ('exposed', 'seckill_id', 'md5')

