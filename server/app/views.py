import requests

from django.contrib.auth import logout, login
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework_jwt.views import api_settings

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


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserAuthSerializer

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)

        return token

    def vk_auth(self, user_info, token):
        req = requests.get('https://api.vk.com/method/account.getProfileInfo?access_token={}&v=5.59'.
                           format(token)).json()
        user_info['first_name'] = req['response']['first_name']
        user_info['last_name'] = req['response']['last_name']

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        token = request.data.get('token')
        device_id = request.data.get('device_id')

        if device_id is None:
            return Response({'error': 'no device id found'}, status=status.HTTP_400_BAD_REQUEST)

        user_info = {'first_name': '', 'last_name': '', 'user_id': ''}

        req = ''
        try:
            self.vk_auth(user_info=user_info, token=token)
            user_info['user_id'] = user_id
        except Exception as e:
            return Response({'error': str(e),
                             'd': req}, status=status.HTTP_400_BAD_REQUEST)

        username = '{}_{}'.format('vk', user_info['user_id'])

        base_user = BaseUser.objects.filter(username=username).first()
        if base_user is None:
            base_user = BaseUser.objects.create(username=username,
                                                first_name=user_info['first_name'],
                                                last_name=user_info['last_name'])

        user_device = UserDevices.objects.filter(device_id=device_id).first()
        if user_device:
            if user_device.user != base_user:
                user_device.user = base_user
                user_device.save()
        else:
            UserDevices.objects.create(device_id=device_id, user=base_user)

        user = User.objects.get(base_user=base_user)

        user.first_name = user_info['first_name']
        user.last_name = user_info['last_name']
        user.url = f'https://vk.com/id{user_id}'
        user.save()

        if self.request.user.is_authenticated:
            logout(self.request)

        if base_user is not None and base_user.is_active:
            login(self.request, base_user)
        else:
            raise ValueError("Can't authenticate username: {}.\nUser is null or not active".format(token))

        serializer = self.serializer_class(user)
        response = serializer.data
        response['token'] = 'JWT {}'.format(self.get_token(base_user))

        return Response(response, status=status.HTTP_200_OK)
