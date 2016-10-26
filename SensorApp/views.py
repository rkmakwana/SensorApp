from django.http import Http404

from SensorApp.serializers import UserSerializer, SignalDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.db.models import F
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import SignalData



@api_view(['POST'])
def create_user(request):
    userName = request.POST.get('username', None)
    userPass = request.POST.get('password', None)
    userMail = request.POST.get('email', None)

    # TODO: check if already existed
    if userName and userPass and userMail:
        try:
            u,created = User.objects.get_or_create(username=userName, password=userPass, email=userMail)
            token = Token.objects.all().filter(user=u)[0]
            serializer = UserSerializer(u, many=False)
            data_dict = serializer.data
            data_dict['token'] = token.key
            return Response(data_dict)
        except Exception as e:
            data_dict = {
                'error' : '1',
            }
            return Response(data_dict)

    else:
       data_dict = {
           'error' : '1',
       }
       return Response(data_dict)

@api_view(['POST'])
def login_user(request):
    userName = request.POST.get('username', None)
    userPass = request.POST.get('password', None)
    userMail = request.POST.get('email', None)

    # TODO: check if already existed
    if (userName or userMail) and userPass:
        try:
            user = None
            if userName:
                user = User.objects.get(username=userName, password=userPass)
            else :
                user = User.objects.get(email=userMail, password=userPass)
            token = Token.objects.all().filter(user=user)[0]
            serializer = UserSerializer(user, many=False)
            data_dict = serializer.data
            data_dict['token'] = token.key
            return Response(data_dict)
        except Exception as e:
            print(e)
            data_dict = {
                'error' : '1',
            }
            return Response(data_dict)

    else:
       data_dict = {
           'error' : '1',
       }
       return Response(data_dict)


@api_view(['POST'])
def save_signal_data(request):
    authentication_classes = (TokenAuthentication,)
    if request.user:
        return Response('chall gaya')
    else:
        return Response('NAHIII chall gaya')

    return Response('Unexpected error occurred')


class SignalDataList(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        data = SignalData.objects.all()
        serializer = SignalDataSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SignalDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
