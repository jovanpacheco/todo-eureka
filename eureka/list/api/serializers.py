from rest_framework import serializers
from ..models import List,Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('uuid', 'name','priority','active')     

class ItemSerializer(serializers.HyperlinkedModelSerializer):

    uuid_list = serializers.CharField(source='list.uuid') 
    assigned_to = serializers.CharField(source='assigned_to.username') 

    class Meta:
        model = Item
        fields = ('uuid', 'title','priority','uuid_list','due_date','completed','completed_date',
        'note','active','assigned_to')  #
        extra_kwargs = {
            'list': {'lookup_field': 'uuid'}
        }
