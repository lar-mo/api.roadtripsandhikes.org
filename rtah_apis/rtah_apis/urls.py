from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from stats_api import views

router = routers.DefaultRouter()
router.register('hikes', views.HikeViewSet)
router.register('persons', views.PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('hiking-stats/', include('stats_api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('', include('api_wrapper.urls')),
    path('wrapper/', include('api_wrapper.urls')),
]
