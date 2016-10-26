from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import SignalData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class SignalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalData
        fields = ('uemac', 'timestamp', 'signal', 'noise')
