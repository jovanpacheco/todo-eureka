from rest_framework import serializers
from ..models import List,Item

# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')

# class RegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'password')

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('uuid', 'name','priority','active')     