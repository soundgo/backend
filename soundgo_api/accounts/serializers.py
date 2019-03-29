from rest_framework import serializers

from .models import Actor


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'user_account', 'photo', 'email', 'minutes', 'credit_card')


