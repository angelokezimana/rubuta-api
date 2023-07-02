from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import services
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(required=False)
    phone = serializers.CharField(required=False)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.UserDataClass(**data)

    def validate(self, attrs):
        """
        attrs parameter comes from UserDataClass
        because we override to_internal_value function
        """
        if attrs.password != attrs.password2:
            raise serializers.ValidationError(
                {"password": "Password fields did not match."}
            )

        return attrs
