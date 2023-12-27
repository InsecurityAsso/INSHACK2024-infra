"""
URL configuration for inshack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path


from inshack import settings
from django.conf.urls.static import static

from ctf.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('register/verified/<str:email>/<str:token>', register_verified, name='register_verified'),
    path('register/create_account', create_account, name='create_account'),
    path('user_checkup', user_checkup, name='user_checkup'),
    path('user_checkup_done', user_checkup_done, name='user_checkup_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
