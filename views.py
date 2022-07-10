from django.shortcuts import render
from rest_framework import status,parsers
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes,parser_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import authentication, permissions

from izzyApp.serializers import AccountSerializer
from .models import Account
from rest_framework.authtoken.models import Token

from django.core.exceptions import ValidationError

from django.contrib.auth import login,authenticate,logout
from rest_framework.parsers import MultiPartParser, FormParser

from django.http import Http404
from rest_framework.views import APIView

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = AccountSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = AccountSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    """
    List all users, or create a new user.
    """
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, format=None):
        user = Account.objects.all()
        serializer = AccountSerializer(user, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get_or_create(user=user)[0].key
            data['response'] = 'successfully registered new user.'
            data['email'] = user.email
            data['username'] = user.username
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
            

    

   


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(request, email=email, password=password)
    if user:
        if user.is_active:
            token = Token.objects.get_or_create(user=user)[0].key
            login(request, user)
            data = {}
            data["message"] = "User Logged In!"
            data["email_address"] = user.email
            Res = {"data": data, "token": token}
            return Response(Res)
        else:
            raise ValidationError({"400": f'Account not active'})
    else:
        raise ValidationError({"400": f'Invalid Login Credentials'})
    


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):

    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')





