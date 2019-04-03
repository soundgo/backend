from rest_framework import serializers

from .models import Configuration

class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ('id', 'maximum_radius', 'minimum_radius', 'time_listen_advertisement', 'minimum_reports_ban', 'time_extend_audio')
