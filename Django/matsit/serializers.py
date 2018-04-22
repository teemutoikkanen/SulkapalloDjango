from django.contrib.auth.models import User, Group
from rest_framework import serializers
from matsit.models import Matsi, Result
from user.serializers import UserSerializer
from ilmoitukset.models import Ilmoitus

class MatsiSerializer(serializers.ModelSerializer):
    playerone = serializers.ReadOnlyField(source='playerone.username')
    playertwo = serializers.ReadOnlyField(source='playertwo.username')
    pointsone = serializers.ReadOnlyField(source='playerone.profile.points')
    pointstwo = serializers.ReadOnlyField(source='playertwo.profile.points')
    # Voi olla et joudun erikseen asettaa read_only=True, koska en oo iha varma
    # et onko tää ReadOnlyField sama asia.
    result_1 = serializers.ReadOnlyField(default=None)
    result_2 = serializers.ReadOnlyField(default=None)
    class Meta:
        model = Matsi
        fields = ('id', 'playerone', 'playertwo', 'pointsone', 'pointstwo', 'time', 'place', 'completed', 'result_1', 'result_2',)
        extra_kwargs = {
            'time': {'read_only': True},
            'place': {'read_only': True},
            'completed': {'default': False},
            'pointsone': {'read_only': True},
            'pointstwo': {'read_only': True},
            'playerone': {'read_only': True},
            'playertwo': {'read_only': True},
            }
        
class ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Result
        fields = ('id', 'result_round_1_player_1', 'result_round_1_player_2', 'result_round_2_player_1', 'result_round_2_player_2', 'result_round_3_player_1', 'result_round_3_player_2', 'winner', 'loser',)