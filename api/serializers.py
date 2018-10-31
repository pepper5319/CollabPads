from rest_framework import serializers
from .models import ListObject, Item, ListrUser

class ListSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    collaborators = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = ListObject
        fields = ('static_id', 'name', 'owner', 'collaborators', 'readOnly')

class ItemSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    assigned_list = serializers.ReadOnlyField(source='assigned_list.static_id')
    liked_users = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Item
        fields = ('static_id', 'name', 'description', 'owner', 'assigned_list', 'liked_users', 'liked_guests')


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    class Meta:
        """Map this serializer to the default django user model."""
        model = ListrUser
        fields = ('id', 'username')
