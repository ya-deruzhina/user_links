from django.urls import path
from .views import *


urlpatterns = [
    path('collections/list/', CollectionsView.as_view()),
    path('collections/<int:collection_id>/', CollectionView.as_view()),
    path('collections/create/', CollectionCreateView.as_view()),
]
