
# Create your tests here.
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase

from rest_framework import status

from .models import RideModel

User = get_user_model()

class RideAPITests(APITestCase):

    def setUp(self):
        self.rider = User.objects.create_user(username="rider", password="pass1234")

        self.driver = User.objects.create_user(username="driver", password="pass1234")

        self.driver.profile.is_driver = True

        self.driver.profile.current_lat = 9.93

        self.driver.profile.current_lng = 76.26

        self.driver.profile.save()

    def login(self, username, password="pass1234"):

        res = self.client.post("/api/jwt/login/", {"username": username, "password": password}, format="json")

        self.assertEqual(res.status_code, 200,msg=res.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")

    def test_create_ride(self):
        self.login("rider")

        res = self.client.post("/api/rides/", {"pickup_location":"A","dropoff_location":"B"}, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(RideModel.objects.count(), 1)

    def test_status_update(self):

        self.login("rider")

        self.client.post("/api/rides/", {"pickup_location":"A","dropoff_location":"B"}, format="json")

        ride_id = RideModel.objects.first().id

        res = self.client.patch(f"/api/rides/{ride_id}/status/", {"status":"cancelled"}, format="json")

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.data["status"], "cancelled")

    def test_driver_accept(self):

        self.login("rider")

        self.client.post("/api/rides/", {"pickup_location":"A","dropoff_location":"B"}, format="json")

        ride_id = RideModel.objects.first().id

        self.login("driver")

        res = self.client.post(f"/api/rides/{ride_id}/accept/", {}, format="json")

        self.assertEqual(res.status_code, 200)

        self.assertEqual(res.data["status"], "accepted")
