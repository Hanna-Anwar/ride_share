from django.shortcuts import render,get_object_or_404

from rest_framework.permissions import AllowAny,IsAuthenticated

from rest_framework import status,viewsets

from rest_framework.response import Response

from user_app.serializers import RegisterSerializer

from rest_framework.decorators import action

from rest_framework.authentication import TokenAuthentication,BasicAuthentication

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
          
         


