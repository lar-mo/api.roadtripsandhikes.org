import django_filters
from .models import Hike, Person

class HikerFilter(django_filters.FilterSet):
    hiker = django_filters.ModelChoiceFilter(field_name="hiker",
                                             queryset=Person.objects.all())

    start_date = django_filters.DateFilter(field_name='hike_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='hike_date', lookup_expr='lt')
    year = django_filters.NumberFilter(field_name='hike_date', lookup_expr='year')

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
