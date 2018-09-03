from rest_framework import serializers
from .models import ListObject

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListObject
        fields = ("name", "owner", "static_id")
