"""listr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from api import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('login/', TemplateView.as_view(template_name='login.html')),
    path('register/', TemplateView.as_view(template_name='register.html')),
    path('admin/', admin.site.urls),
    path('dashboard/', TemplateView.as_view(template_name='index.html')),
    path('listr_api/', include('api.urls')),
    path('lists', TemplateView.as_view(template_name='oneoff.html'))
]

handler404 = views.handler404
handler500 = views.handler500
