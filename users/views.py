from rest_framework.decorators import authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .serializers import UserSerializer


class SignUp(generics.CreateAPIView, generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class Login(generics.CreateAPIView, generics.ListAPIView):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


@authentication_classes([TokenAuthentication])
class YourAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        return Response("hiiiiii")
