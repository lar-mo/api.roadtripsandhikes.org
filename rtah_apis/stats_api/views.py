from rest_framework import viewsets, permissions, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_api_key.permissions import HasAPIKey
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.rest_framework import DjangoFilterBackend

import django_filters
import requests

from .models import Hike, Person
from .serializers import HikeSerializer, PersonSerializer
from .filters import HikerFilter

class HikeViewSet(viewsets.ModelViewSet):
    hiker = PersonSerializer
    queryset = Hike.objects.order_by('-hike_date')
    serializer_class = HikeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = HikerFilter
    # filter_fields = ('hiker__id',) # first implementation - replaced by filters.py + filter_class
    # permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly]

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.order_by('id') # this is default sort but included here for syntax only
    serializer_class = PersonSerializer
    # permission_classes = [HasAPIKey & IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticatedOrReadOnly]

def index(request):
    # return HttpResponse("Hello world!")
    context = {}
    return render(request, 'stats_api/index.html', context)

@xframe_options_exempt
def hiking_stats_for(request, hiker_id):
    # return HttpResponse("Hello world!")
    # overalls = Person.objects.get(id=hiker_id)
    # blogger_apiv3 = get_secret('blogger_apiv3')
    # headers = {"Referer": "https://api.roadtripsandhikes.org"}
    host = request.get_host()
    if host == 'localhost:8000':
        host_protocol = 'http://localhost:8000'
    else:
        host_protocol = 'https://api.roadtripsandhikes.org'
    response = requests.get(host_protocol + "/persons/" + str(hiker_id) + "/?",
        params = {
            # '': hiker_id,
            'format': 'json',
            # 'key': blogger_apiv3,
            # 'fetchBodies': 'true',
            # 'fetchImages': 'true',
            # 'maxResults': 1,
            # 'orderBy': 'PUBLISHED',
        },
        # headers=headers
    )
    total_hikes = response.json().pop('total_hikes')
    total_miles = response.json().pop('total_miles')
    total_elev_feet = response.json().pop('total_elev_feet')
    highest_elev_feet = response.json().pop('highest_elev_feet')
    overalls = {'total_hikes': total_hikes, 'total_miles': total_miles, 'total_elev_feet': total_elev_feet, 'highest_elev_feet': highest_elev_feet}
    context = {
        "hiker_id": hiker_id,
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
