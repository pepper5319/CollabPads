from django.shortcuts import render, render_to_response, redirect
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ListObject, ListrUser, OneOff
from .serializers import *
from .permissions import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
import random
import string
import json
from django.template import RequestContext
from rest_framework.permissions import AllowAny
import hashlib

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

    def put(self, request, pk):
        if(pk):
            currentList = ListObject.objects.get(static_id=pk)
            if(currentList):
                if(self.request.data['collabs']):
                    currentList.collaborators.clear()
                    if(len(self.request.data['collabs']) > 0):
                        for collab in self.request.data['collabs']:
                            try:
                                user = ListrUser.objects.get(username=collab);
                                if user not in currentList.collaborators.all():
                                    currentList.collaborators.add(user)
                            except ListrUser.DoesNotExist:
                                print("User %s does not exists" % (collab))
                    currentList.save()
                    return Response('Updated List {}'.format(pk))
            currentList = OneOff.objects.get(static_id=pk)
            if(currentList):
                if(self.request.data['name'] and self.request.data['name'].strip() != ''):
                    setattr(currentList, 'name', self.request.data['name'])
                if(self.request.data['private'] != None):
                    setattr(currentList, 'private', self.request.data['private'])
                    if(self.request.data['private'] == False):
                        currentList.password.clear()
                    else:
                        if(self.request.data['password']):
                            hashed = hashlib.md5(self.request.data['password'].encode('utf-8')).hexdigest()
                            setattr(currentList, 'private', hashed)
                currentList.save()
                return Response('Updated List {}'.format(pk))

            return Response('Updated List {}'.format(pk))


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
        list = None
        try:
            list = ListObject.objects.get(static_id=self.request.META['HTTP_LIST_ID'])
        except:
            try:
                list = OneOff.objects.get(static_id=self.request.META['HTTP_LIST_ID'])
            except:
                list = None
        if(list):
            serializer.save(owner=self.request.user, assigned_list=self.request.META['HTTP_LIST_ID'])




class DetailsItemView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsItemDetailAllowed)

    def put(self, request, pk):
        if(pk):
            currentItem = Item.objects.get(static_id=pk)
            if(currentItem):
                if('liked_users' in request.data):
                    if(len(self.request.data['liked_users']) > 0):
                        for collab in self.request.data['liked_users']:
                            try:
                                user = ListrUser.objects.get(username=collab);
                                if user not in currentItem.liked_users.all():
                                    currentItem.liked_users.add(user)
                            except ListrUser.DoesNotExist:
                                print("User %s does not exists" % (collab))
                    else:
                        currentItem.liked_users.remove(request.user)
                    currentItem.save()
                if('liked_guests' in request.data):
                    currentItem.liked_guests = self.request.data['liked_guests']
                    currentItem.save()

            return Response('Updated List {}'.format(pk))

class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = ListrUser.objects.all()
    serializer_class = UserSerializer


class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class KeyView(generics.UpdateAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = Key.objects.all()
    serializer_class = KeySerializer
    permission_classes = (permissions.AllowAny,)

    def put(self, request, pk):
        if(pk):
            currentKey = Key.objects.get(code=pk)
            if(currentKey):
                if(currentKey.uses > 0):
                    currentKey.uses = currentKey.uses - 1
                    currentKey.save()
                if(currentKey.uses <= 0):
                    currentKey.delete()
            return Response(pk)

def shared_list(request):
    listId = request.GET.get('l', '')

    #token = 'ce077fea6eab6d704138d9f271d37330f4b226a5' #dev
    token = 'd0b7b2803369922e5e8e2716ec4f296b2f224bed' #prod

    # itemUrl = 'https://collabpads.herokuapp.com/listr_api/items'
    # itemHeader = {'LIST-ID': listId, 'GUEST': 'True', 'Authorization': 'Token ' + token + ' '}

    itemUrl = 'http://localhost:8000/listr_api/items'
    itemHeader = {'LIST-ID': listId, 'GUEST': 'True', 'Authorization': 'Token ' + token + ' '}

    itemData = requests.get(itemUrl, headers=itemHeader)

    # listUrl = 'https://collabpads.herokuapp.com/listr_api/lists/%s/' % (listId)
    # listHeader = {'GUEST': 'True', 'Authorization': 'Token ' + token + ' '}

    listUrl = 'http://localhost:8000/listr_api/lists/%s/' % (listId)
    listHeader = {'GUEST': 'True', 'Authorization': 'Token ' + token + ' '}

    listData = requests.get(listUrl, headers=listHeader)

    if(request.method == 'POST'):
        try:
            itemName=request.POST['itemName']
            itemDescription=request.POST['itemDescription']
        except:
            print("Could not get item data")

        static_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        data = {
            "name": itemName,
            "description": itemDescription,
            "static_id": static_id
        }

        data = json.dumps(data)

        # itemUrl = 'https://collabpads.herokuapp.com/listr_api/items/'
        # postHeader = {'GUEST': 'True', 'Authorization': 'Token ' + token + ' ', 'LIST-ID': listId, 'content-type': 'application/json'}

        itemUrl = 'http://localhost:8000/listr_api/items/'
        postHeader = {'GUEST': 'True', 'Authorization': 'Token ' + token + ' ', 'LIST-ID': listId, 'content-type': 'application/json'}

        postData = requests.post(itemUrl, data=data, headers=postHeader)

        itemData = requests.get(itemUrl, headers=itemHeader)
        listData = requests.get(listUrl, headers=listHeader)


    ctx = {
        "list": listData.json(),
        "items": itemData.json(),
        "token": token
    }
    return render(request, "list.html", ctx)

def create_one_off(request):
        static_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(6))
        new_list = OneOff(static_id=static_id)
        new_list.save()
        return redirect('/lists?l={}'.format(static_id))

def handler404(request, exception, template_name='404.html'):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request, template_name='500.html'):
    listId = request.GET.get('l', '')
    if(listId):
        response = render(request, '500.html', {'list': True})
    else:
        response = render(request, '500.html', {'list': False})
    response.status_code = 500
    return response
