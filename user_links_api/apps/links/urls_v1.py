from django.urls import path
from .views import *


urlpatterns = [
    path('links/list/', LinksView.as_view()),
    path('link/<int:link_id>/', LinkView.as_view()),
    path('link/create/', LinkCreateView.as_view()),
]
