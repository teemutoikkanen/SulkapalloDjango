from django.contrib.auth.models import User, Group
from rest_framework import serializers
from haasteet.models import Haaste
from user.serializers import UserSerializer

class HaasteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    points = serializers.ReadOnlyField(source='owner.profile.points')
    ilmoitus = serializers.ReadOnlyField(source='ilmoitus.id')
    class Meta:
        model = Haaste
        fields = ('id', 'owner', 'points', 'ilmoitus', 'time', 'place',)
        extra_kwargs = { 'points': {'read_only': True} }