from django.db import models
from django.contrib.auth.models import User, AbstractUser

class ListrUser(AbstractUser):
    def __str__(self):
        return "{}".format(self.username)

class Key(models.Model):
    code = models.CharField(max_length=16)
    uses = models.IntegerField()
    def __str__(self):
        return "{}".format(self.code)

class ListObject(models.Model):
    name = models.CharField(max_length=255, default="My List")
    static_id = models.CharField(max_length=6, primary_key=True, unique=True, null=False, blank=False)
    owner = models.ForeignKey(ListrUser,  # ADD THIS FIELD
        related_name='lists',
        on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(ListrUser, blank=True)
    readOnly = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.static_id)


class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    static_id = models.CharField(max_length=8, blank=False, primary_key=True, unique=True)
    description = models.TextField(max_length=512, blank=True)
    liked_users = models.ManyToManyField(ListrUser, blank=True)
    liked_guests = models.IntegerField(default=0)
    assigned_list = models.ForeignKey(ListObject, on_delete=models.CASCADE)
    owner = models.ForeignKey(ListrUser,  # ADD THIS FIELD
        related_name='items',
        on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {}".format(self.name, self.owner)
