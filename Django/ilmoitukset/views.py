from django.shortcuts import render
from ilmoitukset.serializers import IlmoitusSerializer
from ilmoitukset.models import Ilmoitus
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import permissions
from ilmoitukset.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


#GET tähän viewiin --> Lista ilmoista
#POST tähän viewiin --> uuden ilmon luonti
#Tokenit käytössä eli ei tarvita mitään csrf token suojia.
class IlmoitusList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    #def perform_create(self, request, serializer):
    #    serializer.save(owner=request.user)
    
    def get(self, request):
        queryset = Ilmoitus.objects.all()
        serializer = IlmoitusSerializer(queryset, many=True)
        return Response(serializer.data)
	
    def post(self, request):
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
    
class IlmoitusDetail(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
	
    def get(self, request):
        ilmoitus = Ilmoitus.objects.filter(owner=request.user)
        if not ilmoitus.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = IlmoitusSerializer(ilmoitus, many=True)
        return Response(serializer.data)
	
    def delete(self, request):
        ilmo = Ilmoitus.objects.filter(owner=request.user)
        if not ilmo.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ilmo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
		