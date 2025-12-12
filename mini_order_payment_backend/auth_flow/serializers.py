from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = CustomUser
        fields = [ 'email', 'password']


    def create(self, validated_data):
        return CustomUser.objects.create_user(
        email=validated_data.get('email',''),
        password=validated_data['password']
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        data['user'] = user
        return data