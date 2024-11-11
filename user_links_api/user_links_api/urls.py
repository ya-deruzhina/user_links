"""
URL configuration for user_links_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

from swagger import SwaggerView
from .helpers import GetViewsService

paths = []

for version in settings.API_VERSIONS:
    views_modules = GetViewsService.call(version)
    paths += [path(f'api/{version}/', include(view_module)) for view_module in views_modules]
    paths += [path(f'api/{version}/', include(view_module)) for view_module in views_modules]

urlpatterns = paths + [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # For Swagger auth
    path('doc', login_required(SwaggerView.as_view())),
    path('admin/', admin.site.urls),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)