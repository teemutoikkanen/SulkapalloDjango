from django.shortcuts import render
from haasteet.serializers import HaasteSerializer
from haasteet.models import Haaste
from ilmoitukset.serializers import IlmoitusSerializer
from ilmoitukset.models import Ilmoitus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from haasteet.permissions import IsOwnerOrReadOnly
# Create your views here.


#GET tähän viewiin --> Haaste lista jos oot ilmon omistaja
#POST tähän viewiin --> Uus haaste jos oot kirjautunut ja ilmo on vielä haastettavissa
#Tokenit käytössä eli ei tarvita mitään csrf token suojia.
class IlmonHaasteList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        haasteet = Haaste.objects.filter(ilmoitus__owner=request.user)
        if not haasteet.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HaasteSerializer(haasteet, many=True)
        return Response(serializer.data)
        
class LuoHaaste(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    #def perform_create(self, request, serializer):
    #    serializer.save(owner=request.user)
	
    def post(self, request, ilmo_id):
        try:
            ilmo = Ilmoitus.objects.get(pk=ilmo_id)
        except Ilmoitus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if ilmo.owner == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = HaasteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.validated_data['points'] = request.user.profile.points
            serializer.validated_data['ilmoitus'] = ilmo
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserHaasteDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
	
    def get(self, request):
        haasteet = Haaste.objects.filter(owner=request.user)
        serializer = HaasteSerializer(haasteet, many=True)
        return Response(serializer.data)

class DelHaaste(APIView):        
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    
    def delete(self, request, id):
        try:
            haaste = Haaste.objects.get(pk=id)
        except Haaste.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        haaste.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
		