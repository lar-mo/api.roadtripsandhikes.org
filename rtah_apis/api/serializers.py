from rest_framework import serializers
from django.db.models import Sum, Max, Count

from .models import Hike, Person

class PersonSerializer(serializers.ModelSerializer):
    hikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Person
        # fields = ('id','first_name','last_name','join_date','email','profile_img',)
        fields = '__all__'
        read_only_fields = ('join_date',)

class HikeSerializer(serializers.ModelSerializer):
    all_hikes = Hike.objects.all()
    total_hikes = serializers.SerializerMethodField('totalhikes')
    total_miles = serializers.SerializerMethodField('total_mi')
    total_elev_feet = serializers.SerializerMethodField('total_elev_ft')
    highest_elev_feet = serializers.SerializerMethodField('highest_elev_ft')

    # These are the statistics for ALL HIKERS
    # Need to figure out how to filter by Hiker
    def totalhikes(self, obj):
        result = self.all_hikes.aggregate(Count('id'))
        return result['id__count']

    def total_mi(self, obj):
        result = self.all_hikes.aggregate(Sum('distance_mi'))
        return round(result['distance_mi__sum'], 2)

    def total_elev_ft(self, obj):
        result = self.all_hikes.aggregate(Sum('elevation_gain_ft'))
        return result['elevation_gain_ft__sum']

    def highest_elev_ft(self, obj):
        result = self.all_hikes.aggregate(Max('highest_elev_ft'))
        return result['highest_elev_ft__max']

    class Meta:
        model = Hike
        # fields = '__all__'
        fields = ('id', 'hike_date', 'location', 'state', 'distance_mi', 'elevation_gain_ft', 'highest_elev_ft', 'alltrails_url', 'blogger_url', 'hiker', 'total_hikes', 'total_miles', 'total_elev_feet', 'highest_elev_feet')
        depth = 1

    def to_representation(self, instance):
        self.fields['hiker'] =  PersonSerializer(read_only=True)
        return super(HikeSerializer, self).to_representation(instance)
