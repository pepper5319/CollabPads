from rest_framework.permissions import BasePermission
from .models import ListObject, Item

class IsListAllowed(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, ListObject):
            if(str(request.user.username) in str(obj.collaborators)):
                if(request.method == "GET" or request.method == "PATCH"):
                    return True
            return obj.owner == request.user
        return obj.owner == request.user

class IsItemAllowed(BasePermission):
    def has_permission(self, request, view):
        listId = request.META['HTTP_LIST_ID']
        currentList = ListObject.objects.get(static_id=listId)
        if(currentList):
            return request.user.username == currentList.owner.username or request.user.username in str(currentList.collaborators)
        return False

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if(str(request.user.username) in str(obj.assigned_list.owner)):
            return True
        if isinstance(obj, Item):
            return obj.owner == request.user
        return obj.owner == request.user
