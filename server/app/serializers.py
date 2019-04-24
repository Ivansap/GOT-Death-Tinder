from rest_framework import serializers
from django.contrib.auth.models import User as BaseUser

from .models import *


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class CardAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAnswer
        fields = ('id', 'title', 'description')


class CardSerializer(serializers.ModelSerializer):
    answers = CardAnswerSerializer(many=True)

    class Meta:
        model = Card
        fields = ('title', 'description', 'img', 'answers')


class SeriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = ('title', 'showtime', 'img', 'status')


class SeriesSingleSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True)

    class Meta:
        model = Series
        fields = ('title', 'showtime', 'img', 'status', 'cards')


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
