from rest_framework.permissions import BasePermission
from .models import ListObject, Item

class IsListAllowed(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, ListObject):
            return obj.owner == request.user
        return obj.owner == request.user

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if(str(request.user.username) in str(obj.assigned_list.owner)):
            return True
        if isinstance(obj, Item):
            return obj.owner == request.user
        return obj.owner == request.user

class IsAssignedToList(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_list.static_id == request.META['HTTP_LIST_ID']
