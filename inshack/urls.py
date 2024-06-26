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

from accounts.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('index', index, name='index_alt'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('register/verified/<str:email>/<str:token>', register_verified, name='register_verified'),
    path('register/create_account', create_account, name='create_account'),
    path('user_checkup', user_checkup, name='user_checkup'),
    path('418', teapot, name='teapot'),
    path('myspace', myspace, name='personal_space'),
    path('dangerzone/delete', delete_account, name='delete_account'),
    path('dangerzone/reset', change_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
