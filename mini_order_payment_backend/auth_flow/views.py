from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import serializers, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
# Create your views here.
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message': 'User registered successfully'})


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']


        refresh = RefreshToken.for_user(user)
        return Response({
        'id'    : user.id,    
        'refresh': str(refresh),
        'access': str(refresh.access_token)
        })