from rest_framework import serializers
from ..models import List,Item

class FlavorSerializer(serializers.ModelSerializer):
	class Meta:
	model = Flavor
	fields = ['name', 'slug', 'uuid', 'priority','active']




    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=100)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICE)
    active = models.BooleanField(default=True)
    uuid = models.UUIDField( # Used by the API to look up the record
        db_index=True,
        default=uuid_lib.uuid4,
        editable=False)