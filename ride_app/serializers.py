from rest_framework import serializers

from ride_app.models import *

# for creating ride only these fields are required
class RideCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = RideModel

        fields = ["pickup_location", "dropoff_location", "pickup_lat", "pickup_lng"]

# for listing rides / viewing ride

class RideSerializer(serializers.ModelSerializer):

    class Meta:

        model = RideModel

        fields = "__all__"

        read_only_fields = ["rider", "driver", "created_at", "updated_at"]

class RideStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(choices=RideModel.STATUS_CHOICES)

class TrackSerializer(serializers.Serializer):

    current_lat = serializers.FloatField()
    
    current_lng = serializers.FloatField()


  



