# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Audio
from .models import Advertisement
from .models import Category


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('id', 'actor', 'latitude', 'longitude', 'numberReproductions', 'path', 'isInappropriate', 'timestampCreation',
                  'timestampFinish', 'category', 'site', 'tags')


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('id', 'actor', 'latitude', 'longitude', 'numberReproductions', 'path', 'maxPriceToPay', 'radius', 'isActive',
                  'isDelete')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'maxTimeRecord', 'minDurationMap')
