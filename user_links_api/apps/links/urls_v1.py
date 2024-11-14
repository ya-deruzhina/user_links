from django.urls import path
from .views import *


urlpatterns = [
    path('links/list/', LinksView.as_view()),
    path('links/<int:link_id>/', LinkView.as_view()),
    path('links/create/', LinkCreateView.as_view()),
]
