from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
urlpatterns = [
    path('lists/', GetListsView.as_view(), name="lists-all"),
    path('lists/<str:pk>/', GetListDetail.as_view(), name="lists-one"),
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),
]
urlpatterns = format_suffix_patterns(urlpatterns)
