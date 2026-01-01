from django.db.models import Q

from django.contrib.auth import get_user_model

from rest_framework import status, viewsets

from rest_framework.decorators import action

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from ride_app.models import RideModel

from ride_app.serializers import * 


from ride_app.permissions import IsDriver

from ride_app.utils import distance_km

User = get_user_model()


class RideViewSet(viewsets.ModelViewSet):

    authentication_classes = [JWTAuthentication]

    permission_classes = [IsAuthenticated]

    queryset = RideModel.objects.all()

    def get_queryset(self):

        user = self.request.user

        qs = self.queryset.filter(Q(rider=user) | Q(driver=user))

        if hasattr(user, "profile") and getattr(user.profile, "is_driver", False):

          qs = qs | self.queryset.filter(driver__isnull=True, status="requested")

        return qs


    def get_serializer_class(self):

        if self.action == "create":

            return RideCreateSerializer
        
        return RideSerializer

    def perform_create(self, serializer):

        serializer.save(rider=self.request.user)

    # Ride Status Updates 
    @action(detail=True, methods=["patch"], url_path="status")

    def status(self, request, pk=None):

        ride = self.get_object()

        if request.user.id not in [ride.rider_id, ride.driver_id]:

            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        user = RideStatusSerializer(data=request.data)

        user.is_valid(raise_exception=True)

        if ride.status in ["completed", "cancelled"]:

            return Response({"detail": "Ride already ended."}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = user.validated_data["status"]

        ride.save(update_fields=["status", "updated_at"])

        return Response(RideSerializer(ride).data)

    # Driver accepts a ride manually
    @action(detail=True, methods=["post"], url_path="accept", permission_classes=[IsDriver])
    def accept(self, request, pk=None):

        ride = self.get_object()

        if ride.status != "requested":

            return Response({"detail": "Not available"}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver = request.user

        ride.status = "accepted"

        plat = getattr(request.user.profile, "current_latitude", None)

        plng = getattr(request.user.profile, "current_longitude", None)

        if plat is not None and plng is not None:

            ride.current_lat = float(plat)

            ride.current_lng = float(plng)

        ride.save(update_fields=["driver", "status", "current_lat", "current_lng", "updated_at"])

        return Response(RideSerializer(ride).data)

    # Match nearest driver driver assignining
    @action(detail=True, methods=["post"], url_path="match")
    def match(self, request, pk=None):

        ride = self.get_object()

        if ride.status != "requested":

            return Response({"detail": "Ride not in requested state."}, status=status.HTTP_400_BAD_REQUEST)

        if ride.pickup_lat is None or ride.pickup_lng is None:

            return Response({"detail": "pickup_lat & pickup_lng required."}, status=status.HTTP_400_BAD_REQUEST)

        #  busy  drivers
        active_driver_ids = RideModel.objects.filter(
            status__in=["accepted", "started"]
        ).exclude(driver=None).values_list("driver_id", flat=True)

        drivers = User.objects.filter(profile__is_driver=True).exclude(id__in=active_driver_ids)

        best_driver, best_dist = None, None

        best_lat, best_lng = None, None

        for d in drivers:

            plat = getattr(d.profile, "current_latitude", None)

            plng = getattr(d.profile, "current_longitude", None)

            if plat is None or plng is None:
                continue

            dist = distance_km(ride.pickup_lat, ride.pickup_lng, plat, plng)

            if best_driver is None or dist < best_dist:

                best_driver, best_dist = d, dist

                best_lat, best_lng = plat, plng

        if not best_driver:

            return Response({"detail": "No available drivers found."}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver = best_driver

        ride.status = "accepted"

        ride.current_lat = float(best_lat)

        ride.current_lng = float(best_lng)

        ride.save(update_fields=["driver", "status", "current_lat", "current_lng", "updated_at"])

        return Response(
            {
                "ride_id": ride.id,
                "status": ride.status,
                "matched_driver_id": best_driver.id,
                "matched_driver_username": best_driver.username,
                "distance_km": round(best_dist, 2),
            },
            status=200
        )

    # Rider/Driver can view tracking
    @action(detail=True, methods=["get"], url_path="track")
    def track(self, request, pk=None):

        ride = self.get_object()

        if request.user.id not in [ride.rider_id, ride.driver_id]:

            return Response({"detail": "Not allowed."}, status=403)

        return Response(
            {
                "status": ride.status,
                "current_lat": ride.current_lat,
                "current_lng": ride.current_lng
            },
            status=200
        )

    # Driver updates live location
    @action(detail=True, methods=["post"], url_path="track/update", permission_classes=[IsDriver])
    def track_update(self, request, pk=None):

        ride = self.get_object()

        if ride.driver_id != request.user.id:

            return Response({"detail": "Only assigned driver can update."}, status=403)

        user = TrackSerializer(data=request.data)

        user.is_valid(raise_exception=True)

        lat = user.validated_data["current_lat"]

        lng = user.validated_data["current_lng"]

        # update ride tracking
        ride.current_lat = lat

        ride.current_lng = lng

        ride.save(update_fields=["current_lat", "current_lng", "updated_at"])

        # ALSO update driver PROFILE location (so next match uses latest)
        request.user.profile.current_latitude = lat
        
        request.user.profile.current_longitude = lng

        request.user.profile.save(update_fields=["current_latitude", "current_longitude"])

        return Response({"detail": "Location updated."}, status=200)
