from django.contrib.auth.models import User, Group
from rest_framework import serializers
from ilmoitukset.models import Ilmoitus
from user.serializers import UserSerializer

class IlmoitusSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    points = serializers.ReadOnlyField(source='owner.profile.points')
    class Meta:
        model = Ilmoitus
        fields = ('id', 'owner', 'points', 'title', 'time', 'place',)
        extra_kwargs = { 'points': {'read_only': True}, 'owner': {'read_only': True},}