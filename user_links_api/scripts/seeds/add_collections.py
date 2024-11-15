from apps.links.models import LinksModel
from apps.collections.models import CollectionModel
from apps.users.models import User

import random

def perform(*args, **kwargs):
    users = User.objects.all()

    for user in users:
        links = LinksModel.objects.filter(owner=user.id)

        collections = CollectionModel.objects.filter(owner=user.id)
        collections_id =  list(filter(None, [collection.id for collection in collections]))
        
        for link in links:
            id_collection = random.choice(collections_id)
            link.collection.add(id_collection)