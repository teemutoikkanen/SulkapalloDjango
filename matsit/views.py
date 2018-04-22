from django.shortcuts import render
from matsit.serializers import MatsiSerializer, ResultSerializer
from haasteet.serializers import HaasteSerializer
from matsit.models import Matsi, Result
from ilmoitukset.models import Ilmoitus
from haasteet.models import Haaste
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
#from ilmoitukset.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class MatsiAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, haaste_id):
        ilmo = Ilmoitus.objects.get(owner=request.user)
        haaste = Haaste.objects.get(pk=haaste_id)
        if not (haaste.ilmoitus == ilmo):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if ilmo.owner == haaste.owner:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = MatsiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['playerone'] = request.user
            serializer.validated_data['playertwo'] = haaste.owner
            serializer.validated_data['pointsone'] = request.user.profile.points
            serializer.validated_data['pointstwo'] = haaste.owner.profile.points
            serializer.validated_data['time'] = haaste.time
            serializer.validated_data['place'] = haaste.place
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class MatsiGET(APIView):
    permission_classes = (permissions.IsAuthenticated,)    
    
    def get(self, request):
        matches_p1 = Matsi.objects.filter(playerone=request.user)
        matches_p2 = Matsi.objects.filter(playertwo=request.user)
        matsit = matches_p1 | matches_p2 #merging querysets
        serializer = MatsiSerializer(matsit, many=True)
        return Response(serializer.data)

class ResultAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
     
    def get(self, request):
        queryset = Ilmoitus.objects.all()
        serializer = IlmoitusSerializer(queryset, many=True)
        return Response(serializer.data)
	
    def post(self, request, matsi_id):
        try:
            matsi = Matsi.objects.get(pk=matsi_id)
        except matsi.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        
        olemassa_olevia_ilmoja = Ilmoitus.objects.filter(owner=request.user)
        if olemassa_olevia_ilmoja.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = IlmoitusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.validated_data['points'] = request.user.profile.points
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class IlmoitusDetail(APIView):
    # permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
	
    # def get(self, request):
        # ilmoitus = Ilmoitus.objects.filter(owner=request.user)
        # if not ilmoitus.exists():
            # return Response(status=status.HTTP_400_BAD_REQUEST)
        # serializer = IlmoitusSerializer(ilmoitus, many=True)
        # return Response(serializer.data)
	
    # def delete(self, request):
        # ilmo = Ilmoitus.objects.filter(owner=request.user)
        # if not ilmo.exists():
            # return Response(status=status.HTTP_400_BAD_REQUEST)
        # ilmo.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
		