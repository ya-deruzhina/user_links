from django.contrib import admin
from .models import *
from apps.users.models import User

# Register your models here.

admin.site.register(User)