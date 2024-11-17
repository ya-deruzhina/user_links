from django.db import models
from apps.users.models import User
from apps.collections.models import CollectionModel

class LinksModel (models.Model):

    WEBSITE = "WEBSITE"
    BOOK = "BOOK"
    ARTICLE = "ARTICLE"
    MUSIC = "MUSIC"
    VIDEO = "VIDEO"

    KIND_LINKS = [
    (WEBSITE, "WEBSITE"),
    (BOOK, "BOOK"),
    (ARTICLE, "ARTICLE"),
    (MUSIC, "MUSIC"),
    (VIDEO, "VIDEO"),
    ]

    title = models.CharField(null=False)
    description = models.TextField(null=False)
    url_page = models.URLField(null=False, max_length=500)
    image = models.ImageField(upload_to='images/', null=True)
    kind_link = models.CharField (choices=KIND_LINKS, default=WEBSITE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    collection = models.ManyToManyField(CollectionModel,null=True)
