from django.db import models
from apps.users.models import User

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
    url_page = models.URLField(unique=True, null=False)
    #Картинка превью берется из поля og:image.
    # image = models.ImageField(upload_to='images/')
    kind_link = models.CharField (choices=KIND_LINKS, default=WEBSITE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
