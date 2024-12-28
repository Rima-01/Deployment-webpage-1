import logging
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
     #       user = serializer.save()
     #       login(request, user)  # Log in the newly created user
     #       return Response(serializer.data, status=status.HTTP_201_CREATED)
     #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {"message": "User created successfully", "email": user.email},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                logger.error(f"Error saving user: {e}")
                return Response({"error": "Database error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)