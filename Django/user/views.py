from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from user.models import Profile
from rest_framework import viewsets
from user.serializers import UserSerializer

@api_view()
def UserViewSet(request):
    queryset = User.objects.all().order_by('-date_joined')
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST']) #only allows POST methods
def register(request):
    """
    Register a new account
    """
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view() #only GET by default
def user_info(request, id, format=None):
    """
	fetch user info
    """
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

