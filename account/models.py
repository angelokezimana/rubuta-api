from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str = None,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> "User":
        if not first_name:
            raise ValueError("First name is required")
        if not last_name:
            raise ValueError("Last name is required")
        if not email:
            raise ValueError("Email is required")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(
        self, first_name: str, last_name: str, email: str, password: str = None
    ) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user


class User(AbstractUser):
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=100, unique=True)
    password = models.CharField(max_length=255)
    username = None
    birthdate = models.DateField(verbose_name="Birth date", blank=True, null=True)
    phone = models.CharField(
        verbose_name="Mobile phone number",
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    image = models.ImageField(upload_to="images/", blank=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
