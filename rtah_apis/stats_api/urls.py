from django.urls import path

from . import views

app_name = 'stats_api'

urlpatterns = [
    path('', views.index, name='index'),
    path('for/', views.index, name='index'),
    path('for/<int:hiker_id>/', views.hiking_stats_for, name='hiking_stats_for_by_id'),
    path('for/<str:hiker_slug>/', views.hiking_stats_for_slug, name='hiking_stats_for_by_slug'),
]
