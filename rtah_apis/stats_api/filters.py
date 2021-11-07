import django_filters
from .models import Hike, Person

class HikerFilter(django_filters.FilterSet):
    hiker = django_filters.ModelChoiceFilter(field_name="hiker",
                                             queryset=Person.objects.all())
    class Meta:
        model = Hike
        fields = {
            'hiker': ['exact'],
            'hike_date': ['gte', 'lte', 'exact', 'gt', 'lt'],
            'distance_mi': ['gte', 'lte', 'exact', 'gt', 'lt'],
            'elevation_gain_ft': ['gte', 'lte', 'exact', 'gt', 'lt'],
            'highest_elev_ft': ['gte', 'lte', 'exact', 'gt', 'lt'],
            'state': ['exact'],
        }
