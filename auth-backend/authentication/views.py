import logging
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username', None)  # Optional username field

        # Check if email is already registered
        if User.objects.filter(email=email.lower()).exists():
            return Response(
                {"error": "Email ID already exists. Please log in instead."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"error": " ".join(e.messages)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if username is unique (if provided)
        if username and User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists. Please choose a different one."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Proceed with registration
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {"message": "User created successfully", "email": user.email},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.error(f"Error saving user: {e}")
                return Response(
                    {"error": "Database error occurred while saving the user."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authenticate user
        user = authenticate(request, email=email.lower(), password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful','user_id': user.email}, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials. Please check your email and password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
