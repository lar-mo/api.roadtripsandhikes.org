from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bloggerApiGetLatestPost/', views.bloggerApiGetLatestPost, name='bloggerApiGetLatestPost'),
]
