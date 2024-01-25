from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Address, Distance, UserProfile

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'street_number', 'zip_code', 'city', 'country', 'latitude', 'longitude']

class PatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'gender', 'firstname', 'lastname', 'birth_date', 'address', 'creator', 'last_editor']
        
class DistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distance
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_editor = serializers.BooleanField(source='userprofile.is_editor')

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_editor')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.create(user=user, is_editor=validated_data['userprofile']['is_editor'])
        return user