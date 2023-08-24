from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .serializers import (
                          CustomRegistrationSerializer,
                          UserUpdateSerializer,
                          CustomSetPasswordSerializer,
                        )
from rest_framework.permissions import AllowAny

from djoser.serializers import UserDeleteSerializer,UserSerializer

User = get_user_model()

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        is_student = serializer.validated_data.get('is_student')
        student_number = serializer.validated_data.get('student_number')
        if is_student and student_number is None:
            return Response(
                {"error": "Student number is required for students."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            validate_password(serializer.validated_data.get('password'))
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.save()
        if user is None:
            return Response(
                {"error": "User registration failed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"message": "User registered successfully."},
            status=status.HTTP_201_CREATED
        )



class UserUpdateView(APIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CustomSetPasswordView(APIView):
    serializer_class = CustomSetPasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserDeleteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)