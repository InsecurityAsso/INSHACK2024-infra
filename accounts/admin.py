from django.contrib import admin

# import models
from accounts.models import *

# Register your models here.
admin.site.register(player)
admin.site.register(team)
admin.site.register(token)