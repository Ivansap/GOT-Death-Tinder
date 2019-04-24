from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response


from .models import Series
from .serializers import *


class SeriesListViewSet(ListAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesListSerializer


class CharactersViewSet(ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class SeriesSingleViewSet(ListAPIView):
    serializer_class = SeriesSingleSerializer

    def get(self, request, pk, *args, **kwargs):
        queryset = Series.objects.get(pk=pk)
        return Response(self.serializer_class(queryset).data)


class UserAnswerViewSet(CreateAPIView):

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        card_answer_id = request.data.pop('id')

        u_a = UserAnswer(user_id=user_id, card_id=card_answer_id)

        try:
            u_a.save()
        except Exception as e:
            print(e)

        return Response('ok', status=200)


class UserAuthViewSet(CreateAPIView):

    def create(self, request, *args, **kwargs):
        base_user_id = request.user.id
        username = request.data.pop('username')

        User.objects.create(username=username, base_user_id=base_user_id)

        return Response('ok', status=200)
