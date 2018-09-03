from rest_framework import serializers
from .models import ListObject, Item

class ListSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = ListObject
        fields = ('static_id', 'name', 'owner', 'collaborators')

class ItemSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    assigned_list = serializers.ReadOnlyField(source='assigned_list.static_id')

    class Meta:
        model = Item
        fields = ('static_id', 'name', 'description', 'owner', 'assigned_list')
