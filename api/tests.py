from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import ListObject
from .serializers import ListSerializer

# Create your tests here.

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_list(name="", owner="", static_id=""):
        if(name != "" and owner != "" and static_id != ""):
            ListObject.objects.create(name=name, owner=owner, static_id=static_id)

    def setUp(self):
        self.create_list("List 1", "testUser", "123456")
        self.create_list("List 2", "testUser2", "abcdef")
        self.create_list("List 3", "testUser3", "1a2b3c")

class GetAllLists(BaseViewTest):
    def test_get_all_lists(self):
        response = self.client.get(
            reverse("lists-all", kwargs={})
        )
        expected = ListObject.objects.all()
        serialized = ListSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
