from rest_framework.permissions import BasePermission
from .models import ListObject

class IsListAllowed(BasePermission):
    """Custom permission class to allow only list owners to edit them."""

    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the list owner."""
        if isinstance(obj, ListObject):
            return obj.owner == request.user
        return obj.owner == request.user
