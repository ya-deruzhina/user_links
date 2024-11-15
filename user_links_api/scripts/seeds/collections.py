from apps.users.models import User
from apps.collections.models import CollectionModel

from apps.collections.services import CollectionService
from faker import Faker
fake = Faker()


def get_collections_params(owner):
    return {
        "name": fake.name(),
        "description": fake.sentence(),
        "owner":owner
    }


def perform(*args, **kwargs):
    owner = User.objects.all()
    if len(CollectionModel.objects.all()) == 0:
        for i in owner:
            for number in range(5):
                CollectionService.create(get_collections_params(i.id))