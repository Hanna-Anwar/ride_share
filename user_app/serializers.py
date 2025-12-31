from rest_framework import serializers

from user_app.models import *

class RegisterSerializer(serializers.ModelSerializer):

    password  = serializers.CharField(write_only = True,min_length =6)

    is_driver = serializers.BooleanField(write_only = True,default=False)

    class Meta:

        model = User

        fields = ['username','email',"password","is_driver"]

    def create(self, validated_data):

        is_driver = validated_data.pop('is_driver',False)

        user = User.objects.create_user(

            username= validated_data['username'],

            email =validated_data.get('email',""),
            
            password=validated_data['password']

        )
        
        # profile already created by signal, just update it
        user.profile.is_driver = is_driver

        user.profile.save()

        return user
        

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        exclude = ("user",)

        