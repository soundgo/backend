# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Audio
from .models import Advertisement
from .models import Category
from .models import Tag
from .models import Site




class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ('latitude', 'id', 'longitude', 'numberReproductions', 'path', 'isInappropriate', 'timestampCreation', 'timestampFinish', 'category', 'site', 'tags')




class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields =  ('latitude', 'id', 'longitude', 'numberReproductions', 'path', 'maxPriceToPay', 'radius', 'isActive', ' isDelete')



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'maxTimeRecord', 'minDurationMap')



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name')


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('latitude', 'longitude', 'name', 'description')


