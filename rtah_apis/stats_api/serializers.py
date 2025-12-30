from rest_framework import serializers
from django.db.models import Sum, Max, Count

from .models import Hike, Person

class PersonSerializer(serializers.ModelSerializer):

    # hikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    def get_user_hikes(self, obj):
        all_hikes = Hike.objects.filter(hiker__id=obj.id)
        year = self.context["request"].GET.get("year")
        if year:
            all_hikes = all_hikes.filter(hike_date__year=year)
        result = all_hikes.values_list('pk', flat=True)
        return list(result)

    def totalhikes(self,obj):
        all_hikes = Hike.objects.all()
        year = self.context["request"].GET.get("year")
        if year:
            all_hikes = all_hikes.filter(hike_date__year=year)
        result = all_hikes.filter(hiker__id=obj.id).aggregate(Count('id'))
        return result['id__count']

    def total_mi(self, obj):
        all_hikes = Hike.objects.all()
        year = self.context["request"].GET.get("year")
        if year:
            all_hikes = all_hikes.filter(hike_date__year=year)
        result = all_hikes.filter(hiker__id=obj.id).aggregate(Sum('distance_mi'))
        try:
            return round(result['distance_mi__sum'], 2)
        except:
            return 0

    def total_elev_ft(self, obj):
        all_hikes = Hike.objects.all()
        year = self.context["request"].GET.get("year")
        if year:
            all_hikes = all_hikes.filter(hike_date__year=year)
        results = all_hikes.filter(hiker__id=obj.id).aggregate(Sum('elevation_gain_ft'))
        res = results['elevation_gain_ft__sum']
        if not res:
            return 0
        return res

    def highest_elev_ft(self, obj):
        all_hikes = Hike.objects.all()
        year = self.context["request"].GET.get("year")
        if year:
            all_hikes = all_hikes.filter(hike_date__year=year)
        result = all_hikes.filter(hiker__id=obj.id).aggregate(Max('highest_elev_ft'))
        res = result['highest_elev_ft__max']
        if not res:
            return 0
        return res

    # hikes = serializers.SerializerMethodField('get_user_hikes')
    total_hikes = serializers.SerializerMethodField('totalhikes')
    total_miles = serializers.SerializerMethodField('total_mi')
    total_elev_feet = serializers.SerializerMethodField('total_elev_ft')
    highest_elev_feet = serializers.SerializerMethodField('highest_elev_ft')

    class Meta:
        model = Person
        # fields = ('id','first_name','last_name','slug','join_date','email','profile_img','hikes','total_hikes','total_miles','total_elev_feet','highest_elev_feet')
        fields = ('id','first_name','last_name','slug','join_date','email','profile_img','total_hikes','total_miles','total_elev_feet','highest_elev_feet')
        # fields = '__all__'

class HikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hike
        fields = '__all__'
        # fields = ('id', 'hike_date', 'location', 'state', 'distance_mi', 'elevation_gain_ft', 'highest_elev_ft', 'alltrails_url', 'blogger_url', 'hiker',)

    def to_representation(self, instance):
        self.fields['hiker'] = PersonSerializer(read_only=True)
        return super(HikeSerializer, self).to_representation(instance)
