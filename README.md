# Ride Sharing API – Django REST Framework

This project is a Basic Ride Sharing API built using Django Rest Framework (DRF) as part of an assignment.  
It supports user authentication, ride requests, ride status updates, driver acceptance, and simulated real-time ride tracking.

 Features Implemented

 User API
- User registration
- User login using JWT authentication
- profile creation via signals

Ride API
- Create a ride request
- View ride details
- List all rides for a user (rider or driver)

Ride Status Updates
- Update ride status:
  - requested
  - accepted
  - started
  - completed
  - cancelled(only rider can)

 Ride Matching 
- Drivers can accept available ride requests
- Basic matching logic based on availability

Real-time Ride Tracking 
- Simulated tracking by periodically updating current latitude and longitude of the ride

Testing
- Basic unit tests for models and API endpoints

Endpoints list:

-POST /api/auth/register/

-POST /api/auth/login/

-GET /api/profile/my_profile/

-PATCH /api/profile/update_location/

-POST /api/rides/ (create ride)

-GET /api/rides/ (list)

-GET /api/rides/{id}/ (detail)

-POST /api/rides/{id}/match/

-PATCH /api/rides/{id}/status/

-POST /api/rides/{id}/track/update/

-GET /api/rides/{id}/track
