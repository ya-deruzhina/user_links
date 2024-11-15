from apps.links.models import LinksModel
from apps.users.models import User

from apps.links.services import LinkService
from faker import Faker
fake = Faker()
import random

KIND_LINKS = [
   "WEBSITE",
   "BOOK",
   "ARTICLE",
   "MUSIC",
   "VIDEO"
]

def get_links_params(owner):
    return {
        "title": fake.city(),
        "description":fake.sentence(),
        "url_page":fake.url(),
        "kind_link":random.choice(KIND_LINKS),
        "owner":owner,
    }


def perform(*args, **kwargs):
    owners = User.objects.all()
    if len(LinksModel.objects.all()) == 0:
        for user in owners:
            LinkService.create(get_links_params(user.id))
        
