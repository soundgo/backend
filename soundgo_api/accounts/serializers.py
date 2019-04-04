from rest_framework import serializers

from .models import Actor, CreditCard


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'user_account', 'photo', 'email', 'minutes', 'credit_card')


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id', 'holderName', 'brandName', 'number', 'expirationMonth', 'expirationYear', 'cvvCode', 'isDelete')