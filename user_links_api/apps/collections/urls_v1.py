from django.urls import path
from .views import *


urlpatterns = [
    path('collections/list/', CollectionsView.as_view()),
    path('collection/<int:collection_id>/', CollectionView.as_view()),
    path('collection/create/', CollectionCreateView.as_view()),
]
