from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class RegisterUserView(generics.CreateAPIView):
    """
        API endpoint for registering a new user.

        Request Method: POST

        Parameters:
        - username (str): Username of the new user.
        - password (str): Password of the new user.

        Returns:
        - If successful, returns a success message with status code 201 (Created).
        - If validation fails, returns error messages with status code 400 (Bad Request).
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
        API endpoint for user login.

        Request Method: POST

        Parameters:
        - username (str): Username of the user.
        - password (str): Password of the user.

        Returns:
        - If login is successful, returns a success message with an access token and status code 200 (OK).
        - If invalid credentials are provided, returns an error message with status code 400 (Bad Request).
        - If validation fails, returns error messages with status code 400 (Bad Request).
    """

    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'message': 'Login successful',
                    'access_token': str(refresh.access_token),
                }
                return Response(response_data)
            else:
                return Response({'message': 'Invalid credentials'}, status=400)
        else:
            return Response(serializer.errors, status=400)
