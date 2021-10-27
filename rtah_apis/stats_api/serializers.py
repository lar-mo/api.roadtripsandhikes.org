from rest_framework import serializers
from django.db.models import Sum, Max, Count

from .models import Hike, Person

class PersonSerializer(serializers.ModelSerializer):
    hikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    all_hikes = Hike.objects.all()
    def totalhikes(self,obj):
        result = self.all_hikes.filter(hiker__id=obj.id).aggregate(Count('id'))
        return result['id__count']

    def total_mi(self, obj):
        result = self.all_hikes.filter(hiker__id=obj.id).aggregate(Sum('distance_mi'))
        try:
            return round(result['distance_mi__sum'], 2)
        except:
            return 0

    def total_elev_ft(self, obj):
        result = self.all_hikes.filter(hiker__id=obj.id).aggregate(Sum('elevation_gain_ft'))
        res = result['elevation_gain_ft__sum']
        if not res:
            return 0
        return res

    def highest_elev_ft(self, obj):
        result = self.all_hikes.filter(hiker__id=obj.id).aggregate(Max('highest_elev_ft'))
        res = result['highest_elev_ft__max']
        if not res:
            return 0
        return res

    total_hikes = serializers.SerializerMethodField('totalhikes')
    total_miles = serializers.SerializerMethodField('total_mi')
    total_elev_feet = serializers.SerializerMethodField('total_elev_ft')
    highest_elev_feet = serializers.SerializerMethodField('highest_elev_ft')

    class Meta:
        model = Person
        fields = ('id','first_name','last_name','slug','join_date','email','profile_img','hikes','total_hikes','total_miles','total_elev_feet','highest_elev_feet')
        # fields = '__all__'

class HikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hike
        fields = '__all__'
        # fields = ('id', 'hike_date', 'location', 'state', 'distance_mi', 'elevation_gain_ft', 'highest_elev_ft', 'alltrails_url', 'blogger_url', 'hiker',)

    def to_representation(self, instance):
        self.fields['hiker'] =  PersonSerializer(read_only=True)
        return super(HikeSerializer, self).to_representation(instance)
