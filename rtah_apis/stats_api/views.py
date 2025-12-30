from rest_framework import viewsets, permissions, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Max, Count

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
    try:
        # Determine year filter from query params
        year = "All"
        for i in range(1970, 2050):
            if str(i) in request.GET:
                year = str(i)
                break
        
        # Get hiker
        try:
            hiker = Person.objects.get(slug=hiker_slug)
            hiker_name = hiker.fullname()
        except Person.DoesNotExist:
            overalls = {'total_hikes': 0, 'total_miles': 0, 'total_elev_feet': 0, 'highest_elev_feet': 0}
            context = {
                "overalls": overalls,
                "error": "invalid_slug",
            }
            return render(request, 'stats_api/hiking_stats_for.html', context)

        # Build query for hikes
        hikes_query = Hike.objects.filter(hiker=hiker)
        if year != "All":
            hikes_query = hikes_query.filter(hike_date__year=year)

        # Get stats with single database query
        stats = hikes_query.aggregate(
            total_hikes=Count('id'),
            total_miles=Sum('distance_mi'),
            total_elev_feet=Sum('elevation_gain_ft'),
            highest_elev_feet=Max('highest_elev_ft')
        )

        # Extract values with defaults
        total_hikes = stats['total_hikes'] or 0
        total_miles = round(stats['total_miles'] or 0, 2)
        total_elev_feet = stats['total_elev_feet'] or 0
        highest_elev_feet = stats['highest_elev_feet'] or 0

        # Set goals based on year
        if year == "2021":
            hikes_goal = 75
            miles_goal = 500
            elev_goal = 120000
        else:
            hikes_goal = 52
            miles_goal = 365
            elev_goal = 84000

        # Calculate percentages and differences
        total_hikes_diff = max(0, hikes_goal - total_hikes)
        total_hikes_pct = round((total_hikes/hikes_goal) * 100, 1)
        if total_hikes_pct.is_integer():
            total_hikes_percentage = str(int(total_hikes_pct)) + "%"
        else:
            total_hikes_percentage = str(total_hikes_pct) + "%"

        total_miles_diff = max(0, round(miles_goal - total_miles, 1))
        total_miles_pct = round((total_miles/miles_goal) * 100, 1)
        if total_miles_pct.is_integer():
            total_miles_percentage = str(int(total_miles_pct)) + "%"
        else:
            total_miles_percentage = str(total_miles_pct) + "%"

        total_elev_diff = max(0, round(elev_goal - total_elev_feet, 0))
        total_elev_pct = round((total_elev_feet/elev_goal) * 100, 1)
        if total_elev_pct.is_integer():
            total_elev_percentage = str(int(total_elev_pct)) + "%"
        else:
            total_elev_percentage = str(total_elev_pct) + "%"

        overalls = {
            'total_hikes': total_hikes,
            'total_miles': total_miles,
            'total_elev_feet': total_elev_feet,
            'highest_elev_feet': highest_elev_feet,
            'total_hikes_percentage': total_hikes_percentage,
            'total_miles_percentage': total_miles_percentage,
            'total_elev_percentage': total_elev_percentage,
            'goal_hikes': hikes_goal,
            'goal_miles': miles_goal,
            'goal_elevation': elev_goal,
            'total_hikes_diff': total_hikes_diff,
            'total_miles_diff': total_miles_diff,
            'total_elev_diff': total_elev_diff
        }
        
        context = {
            "hiker_id": hiker.id,
            "hiker_name": hiker_name,
            "year": year,
            "overalls": overalls,
        }
        return render(request, 'stats_api/hiking_stats_for.html', context)
    except Exception as e:
        # Return empty response on error - iframe will stay hidden
        return HttpResponse('', content_type='text/html', status=503)

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
