from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect

from .models import Hike, Person
from .serializers import HikeSerializer, PersonSerializer

class HikeViewSet(viewsets.ModelViewSet):
    queryset = Hike.objects.order_by('-hike_date')
    serializer_class = HikeSerializer
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
