from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "birthdate",
            "phone",
            "image",
        )


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birthdate",
            "phone",
            "image",
            "is_superuser",
            "is_staff",
            "is_active",
            "password",
            "groups",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            birthdate=validated_data["birthdate"],
            phone=validated_data["phone"],
            image=validated_data["image"],
            is_superuser=validated_data["is_superuser"],
            is_staff=validated_data["is_staff"],
            is_active=validated_data["is_active"],
        )
        user.set_password(validated_data["password"])
        user.save()
        groups = validated_data.get("groups", [])
        user.groups.add(*groups)
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True, slug_field="codename", queryset=Permission.objects.all()
    )

    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]


class ContentTypeSerializer(serializers.ModelSerializer):
    permission_set = PermissionSerializer(many=True)

    class Meta:
        model = ContentType
        fields = ["model", "permission_set"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["model"] = representation["model"].capitalize()

        representation["permission_set"] = [
            {**permission, "action": permission["codename"].split("_")[0]}
            for permission in representation["permission_set"]
        ]

        return representation
