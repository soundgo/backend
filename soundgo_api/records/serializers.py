# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Audio
from .models import Advertisement
from .models import Category
from .models import Like
from .models import Report
from .models import Reproduction


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('id', 'actor', 'latitude', 'longitude', 'numberReproductions', 'duration', 'path', 'isInappropriate',
                  'timestampCreation', 'timestampFinish', 'category', 'site', 'tags')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'actor', 'latitude', 'longitude', 'numberReproductions', 'duration', 'path', 'maxPriceToPay',
                  'radius', 'isActive', 'isDelete')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'maxTimeRecord', 'minDurationMap')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'audio', 'actor')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'actor', 'audio')


class ReproductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reproduction
        fields = ('id', 'actor', 'date', 'advertisement')
