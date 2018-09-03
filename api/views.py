from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ListObject
from .serializers import ListSerializer
from .permissions import *


# Create your views here.
class GetListsView(generics.ListCreateAPIView):
    queryset = ListObject.objects.all()
    serializer_class = ListSerializer

    permission_classes = (permissions.IsAuthenticated, IsListAllowed)

    def get_queryset(self):
            """
            This view should return a list of all the purchases
            for the currently authenticated user.
            """
            user = self.request.user
            ownedLists = ListObject.objects.filter(owner=user)
            return ownedLists

    def perform_create(self, serializer):
            """Save the post data when creating a new list."""
            serializer.save(owner=self.request.user)

class GetListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ListObject.objects.all()
    serializer_class = ListSerializer
    permission_classes = (permissions.IsAuthenticated, IsListAllowed)
