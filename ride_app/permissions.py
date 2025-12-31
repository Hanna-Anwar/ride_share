from rest_framework.permissions import BasePermission

class IsDriver(BasePermission):

    def has_permission(self,request,view):

        return bool(
                    request.user.is_authenticated and
                    request.user.profile.is_driver
)
    

# this file is used to makesure that the user must logged in and must be a driver