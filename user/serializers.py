from django.contrib.auth.models import User, Group
from rest_framework import serializers
from user.models import Profile

# class UserSerializer(serializers.ModelSerializer):
    # class Meta:
        # model = User
        # fields = ('username','password',)
        # extra_kwargs = {'password': {'write_only': True}}
		
class ProfileSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Profile
        fields = ('points', 'phone',)
        extra_kwargs = {'points': {'default': 1000, 'read_only': True,}}

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
    '''
    For updates you'll want to think carefully about how to handle updates to relationships.
	For example if the data for the relationship is None, or not provided, which of the following should occur?

    Set the relationship to NULL in the database.
    Delete the associated instance.
    Ignore the data and leave the instance as it is.
    Raise a validation error
    '''
	#Currently all field values must be provided when updating. Even ones that do not change
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        # Unless the application properly enforces that this field is
        # always set, the follow could raise a `DoesNotExist`, which
        # would need to be handled.
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        profile.points = profile_data.get(
            'points',
            profile.points
        )
        profile.phone = profile_data.get(
            'phone',
            profile.phone
         )
        profile.save()

        return instance