import django_filters
from .models import Hike, Person

class HikerFilter(django_filters.FilterSet):
    hiker = django_filters.ModelChoiceFilter(field_name="hiker",
                                             queryset=Person.objects.all())
    class Meta:
        model = Hike
        fields = ('hiker',)