from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer,UserSerializer,SetPasswordSerializer


User = get_user_model()

    
class CustomRegistrationSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (
            'username',
            'first_name', 
            'last_name', 
            'email', 
            'mobile',
            'password', 
            'confirm_password'
        )

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if data.get('is_student') and not data.get('student_number'):
            raise serializers.ValidationError("Student number is required for students.")
        return data
    
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        
        return user
    


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'first_name', 
            'last_name', 
            'mobile',
        )
        
        
class CustomSetPasswordSerializer(SetPasswordSerializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[...]) 

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        re_new_password = attrs.get('re_new_password')

        if new_password != re_new_password:
            raise serializers.ValidationError({"re_new_password": "Passwords do not match."})

        return attrs