from django.urls import path

from . import views

app_name = 'stats_api'

urlpatterns = [
    path('', views.index, name='index'),
]
