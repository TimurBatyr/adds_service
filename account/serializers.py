from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .utils import send_new_password

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(min_length=6, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm',)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email has already been taken')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_mail()

class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(max_length=8,
                                            min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')

        if not User.objects.filter(email=email,
                                   activation_code=activation_code).exists():
            raise serializers.ValidationError('User not found')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Type correct password')
        return old_password

    def validate(self, attrs):
         password = attrs.get('new_password')
         password_confirm = attrs.get('password_confirm')
         if password != password_confirm:
             raise serializers.ValidationError('Passwords do not match')
         return attrs

    def set_new_password(self):
         user = self.context['request'].user
         password = self.validated_data.get('new_password')
         user.set_password(password)
         user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        return email

    def create_new_password(self, email):

        user = User.objects.get(email=email)
        random_password = get_random_string(8)
        user.set_password(random_password)
        user.save()
        send_new_password(random_password, email)