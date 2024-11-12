from django.db import models
from apps.users.models import User

class CollectionModel (models.Model):
    name = models.CharField(null=False)
    short_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
