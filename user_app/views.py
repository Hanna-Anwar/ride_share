from django.shortcuts import render,get_object_or_404

from django.contrib.auth import authenticate

from user_app.models import *

from rest_framework.permissions import AllowAny,IsAuthenticated

from rest_framework import status,viewsets

from rest_framework.response import Response

from user_app.serializers import RegisterSerializer,ProfileSerializer

from rest_framework.decorators import action

from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication,BasicAuthentication

from rest_framework_simplejwt.tokens import RefreshToken

from  rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterLoginViewSet(viewsets.GenericViewSet):

     permission_classes = [AllowAny]

     serializer_class = RegisterSerializer

     @action(detail=False,methods=['post'],url_path="register")
     def register(self,request):

          user = self.get_serializer(data = request.data)

          user.is_valid(raise_exception = True)

          user.save()

               
          return Response(user.data,
                         status=status.HTTP_201_CREATED)
     
     @action(detail=False, methods=["post"], url_path="login")
     def login(self, request):
        
        username = request.data.get("username")

        password = request.data.get("password")

        if not username or not password:
            
            return Response(
                
                {"detail": "username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

     #    token,creates = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)

        return Response(
            
           
            {
                "message":"login success",
                "access_token":str(refresh.access_token),
                "refresh_token":str(refresh)
                
            },
            status=status.HTTP_200_OK,
        )
     
class ProfilViewSet(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    authentication_classes = [JWTAuthentication]

    serializer_class = ProfileSerializer

    @action(detail=False,methods=['get'],url_path="my_profile")
    def my_profile(self,request):

        profile = get_object_or_404(Profile,user=request.user)

        profile_serializer = self.get_serializer(profile)

        return Response(profile_serializer.data,
                        status=status.HTTP_200_OK)
    
   
    @action(detail=False, methods=["patch"], url_path="update_location")
    def update_location(self, request):
        
        profile = request.user.profile

        profile_serializer = self.get_serializer(profile, data=request.data, partial=True)

        profile_serializer.is_valid(raise_exception=True)

        profile_serializer.save()

        return Response(profile_serializer.data,
                        status=status.HTTP_200_OK)


# partial=True means user can send only one field (not all fields)


          
         


