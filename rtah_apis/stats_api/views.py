from rest_framework import viewsets, permissions, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.rest_framework import DjangoFilterBackend

import django_filters

from .models import Hike, Person
from .serializers import HikeSerializer, PersonSerializer
from .filters import HikerFilter

class HikeViewSet(viewsets.ModelViewSet):
    hiker = PersonSerializer
    queryset = Hike.objects.order_by('-hike_date')
    serializer_class = HikeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = HikerFilter
    # filter_fields = ('hiker__id',)
    # permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.order_by('last_name')
    serializer_class = PersonSerializer
    # permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly]

def index(request):
    # return HttpResponse("Hello world!")
    context = {}
    return render(request, 'stats_api/index.html', context)


# class HikesByHikerList(generics.ListAPIView):
#     serializer_class = HikeSerializer
#
#     def get_queryset(self):
#         """
#         This view should return a list of all hikes by
#         the hiker passed in the URL
#         """
#         hiker = self.kwargs['hiker']
#         print(hiker)
#         my_hikes = Hike.objects.filter(hiker=hiker)
#         print(my_hikes)
#         return my_hikes
