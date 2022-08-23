from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistrationSerializer, ActivationSerializer, ForgotPasswordSerializer, \
    ChangePasswordSerializer, LoginSerializer


class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Successfully registered. Check your email to confirm', status=status.HTTP_201_CREATED)


class ActivateView(APIView):

    serializer_class = ActivationSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Your account successfully activated!', status=status.HTTP_200_OK)


# class LoginView(ObtainAuthToken):
#     serializer_class = LoginSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create_new_password()
            return Response('New password has been sent to your email')

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('You have successfully updated your password')