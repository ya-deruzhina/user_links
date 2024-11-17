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
    owners_id = list(filter(None, [owner.id for owner in owners]))
    for n in range(100):
        user_id = random.choice(owners_id)
        LinkService.create(get_links_params(user_id))
        
