from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ListObject
from .serializers import *
from .permissions import *


# Create your views here.

"""
LIST VIEWS
"""
class GetListsView(generics.ListCreateAPIView):
    queryset = ListObject.objects.all()
    serializer_class = ListSerializer

    permission_classes = (permissions.IsAuthenticated, IsListAllowed)

    def get_queryset(self):
            user = self.request.user
            ownedLists = ListObject.objects.filter(owner=user)
            return ownedLists

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user)

class GetListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ListObject.objects.all()
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticated, IsListAllowed)



"""
ITEM VIEWS
"""
class CreateItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsAssignedToList)

    def get_queryset(self):
            list_id = self.request.META['HTTP_LIST_ID']
            listItems = Item.objects.filter(assigned_list=list_id)
            listItems = listItems.filter(assigned_list__owner=self.request.user)
            listItemsCollab = Item.objects.filter(assigned_list=list_id)
            listItemsCollab = listItemsCollab.filter(assigned_list__collaborators__contains=self.request.user.username)
            return listItemsCollab | listItems

    def perform_create(self, serializer):
            serializer.save(owner=self.request.user, assigned_list=ListObject.objects.get(static_id=self.request.META['HTTP_LIST_ID']))


class DetailsItemView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsAssignedToList)
