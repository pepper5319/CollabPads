from django.contrib import admin
from .models import ListObject, Item, ListrUser, Key, OneOff
# Register your models here.
admin.site.register(ListObject)
admin.site.register(Item)
admin.site.register(ListrUser)
admin.site.register(Key)
admin.site.register(OneOff)
