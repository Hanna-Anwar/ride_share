from django.conf import settings

from user_app.models import *

from django.db import models

class RideModel(models.Model):

    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("started", "Started"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides_as_rider"
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rides_as_driver"
    )

    pickup_location = models.CharField(max_length=300)

    dropoff_location = models.CharField(max_length=300)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="requested"
    )

   
    pickup_lat = models.FloatField(null=True, blank=True)

    pickup_lng = models.FloatField(null=True, blank=True)

    current_lat = models.FloatField(null=True, blank=True)

    current_lng = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

   
