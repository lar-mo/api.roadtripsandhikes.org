from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers

# from pmd_strings import views

# router = routers.DefaultRouter()
# router.register('strings/v1', views.StringViewSetv1)
# router.register('strings/v2', views.StringViewSetv2)
# router.register('strings/v3', views.StringViewSetv3)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls')),
    # path('', include('api_wrapper.urls')),
    path('wrapper/', include('api_wrapper.urls'))
]
