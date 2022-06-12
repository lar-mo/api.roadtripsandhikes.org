from rest_framework import viewsets, permissions, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.rest_framework import DjangoFilterBackend

import django_filters
import requests

import json
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

from .models import Hike, Person
from .serializers import HikeSerializer, PersonSerializer
from .filters import HikerFilter

BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

class HikeViewSet(viewsets.ModelViewSet):
    hiker = PersonSerializer
    queryset = Hike.objects.order_by('-hike_date')
    serializer_class = HikeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = HikerFilter
    # filter_fields = ('hiker__id',) # first implementation - replaced by filters.py + filter_class
    permission_classes = [ HasAPIKey | IsAuthenticated ]
    # permission_classes = [IsAuthenticatedOrReadOnly]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.order_by('id') # this is default sort but included here for syntax only
    serializer_class = PersonSerializer
    permission_classes = [ HasAPIKey | IsAuthenticated ]
    # permission_classes = [IsAuthenticatedOrReadOnly]

def index(request):
    # return HttpResponse("Hello world!")
    context = {}
    return render(request, 'stats_api/index.html', context)

def hiking_stats_for(request, hiker_id):
    hiker = Person.objects.get(id=hiker_id)
    # return hiking_stats_for_slug(request, hiker_slug=hiker.slug) # when using **kwargs (line 60, 75)
    return hiking_stats_for_slug(request, hiker.slug)

@xframe_options_exempt
def hiking_stats_for_slug(request, hiker_slug, **kwargs): # **kwargs: see lines 56, 75
    my_hiking_stats = get_secret('my_hiking_stats')
    # headers = {"Referer": "https://api.roadtripsandhikes.org"}
    year_filter = "/?format=json"
    year = "All"
    for i in range(1970, 2050):
        if str(i) in request.GET:
            year_filter = "/?year={}&format=json".format(i)
            year = str(i)
    host = request.get_host()
    if host == 'localhost:8000':
        host_protocol = 'http://localhost:8000'
    else:
        host_protocol = 'https://api.roadtripsandhikes.org'
    try:
        # hiker = Person.objects.get(slug=kwargs['hiker_slug']) # when using **kwwargs (line 56, 60)
        hiker = Person.objects.get(slug=hiker_slug)
        hiker_name = hiker.fullname()
    except:
        hiker_id = 0
        overalls = {'total_hikes': 0, 'total_miles': 0, 'total_elev_feet': 0, 'highest_elev_feet': 0}
        context = {
            "overalls": overalls,
            "error": "invalid_slug",
            }
        return render(request, 'stats_api/hiking_stats_for.html', context)

    response = requests.get(host_protocol + "/persons/" + str(hiker.id) + year_filter,
        headers={'Authorization': 'Api-Key '+my_hiking_stats}
    )

    # The code below replaces template > mathfilters > widthratio which returns integers
    # e.g.
    #   {% widthratio overalls.total_hikes 75 100 %}%
    #   {% widthratio overalls.total_miles 500 100 %}%
    #   {% widthratio overalls.total_elev_feet 120000 100 %}%

    # 1. Get Total Hikes from API JSON response
    # 2. Round to one decimal place
    # 3. Multiply by 100
    # 4. If float ends with 0, convert to integer
    # 5. Convert to string and add percent symbol

    if year == "2022":
        hikes_goal = 50
        miles_goal = 350
        elev_goal = 80000
    else:
        hikes_goal = 75
        miles_goal = 500
        elev_goal = 120000

    print(hikes_goal, miles_goal, elev_goal)

    total_hikes = response.json().pop('total_hikes')
    total_hikes_pct = round((total_hikes/hikes_goal) * 100, 1)
    if total_hikes_pct.is_integer():
        total_hikes_percentage = str(int(total_hikes_pct)) + "%"
    else:
        total_hikes_percentage = str(total_hikes_pct) + "%"

    total_miles = response.json().pop('total_miles')
    total_miles_pct = round((total_miles/miles_goal) * 100, 1)
    if total_miles_pct.is_integer():
        total_miles_percentage = str(int(total_miles_pct)) + "%"
    else:
        total_miles_percentage = str(total_miles_pct) + "%"

    total_elev_feet = response.json().pop('total_elev_feet')
    total_elev_pct =  round((total_elev_feet/elev_goal) * 100, 1)
    if total_elev_pct.is_integer():
        total_elev_percentage = str(int(total_elev_pct)) + "%"
    else:
        total_elev_percentage = str(total_elev_pct) + "%"

    highest_elev_feet = response.json().pop('highest_elev_feet')

    overalls = {'total_hikes': total_hikes, 'total_miles': total_miles, 'total_elev_feet': total_elev_feet, 'highest_elev_feet': highest_elev_feet, 'total_hikes_percentage': total_hikes_percentage, 'total_miles_percentage': total_miles_percentage, 'total_elev_percentage': total_elev_percentage, 'goal_hikes': hikes_goal, 'goal_miles': miles_goal, 'goal_elevation': elev_goal}
    context = {
        "hiker_id": hiker.id,
        "hiker_name": hiker_name,
        "year": year,
        "overalls": overalls,
        }
    return render(request, 'stats_api/hiking_stats_for.html', context)

##
## https://stackoverflow.com/questions/24861252/django-rest-framework-foreign-keys-and-filtering
##
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
