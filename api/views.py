from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ListObject, ListrUser
from .serializers import *
from .permissions import *
from django.contrib.auth.models import User

# Create your views here.

"""
LIST VIEWS
"""
class GetListsView(generics.ListCreateAPIView):
    serializer_class = ListSerializer

    permission_classes = (permissions.IsAuthenticated, IsListAllowed)

    def get_queryset(self):
        user = self.request.user
        ownedLists = ListObject.objects.filter(owner=user)
        return ownedLists

    def perform_create(self, serializer):
        newList = serializer.save(owner=self.request.user)
        if(self.request.data['collabs']):
            for collab in self.request.data['collabs']:
                try:
                    user = ListrUser.objects.get(username=collab);
                    newList.collaborators.add(user)
                except ListrUser.DoesNotExist:
                    print("User %s does not exists" % (collab))

            newList.save()


class GetSharedListView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticated, IsListAllowed)

    def get_queryset(self):
            """
            This view should return a list of all the purchases
            for the currently authenticated user.
            """
            user = self.request.user
            collabLists = ListObject.objects.filter(collaborators__id=user.id)
            return collabLists

class GetListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ListObject.objects.all()
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticated, IsListAllowed)



"""
ITEM VIEWS
"""
class CreateItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsItemAllowed)

    def get_queryset(self):
            list_id = self.request.META['HTTP_LIST_ID']
            listItems = Item.objects.filter(assigned_list=list_id)
            return listItems

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user, assigned_list=ListObject.objects.get(static_id=self.request.META['HTTP_LIST_ID']))


class DetailsItemView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsItemDetailAllowed)
