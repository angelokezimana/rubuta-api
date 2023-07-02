import dataclasses
import jwt
from typing import TYPE_CHECKING

from django.utils import timezone
from django.conf import settings

from .models import User

if TYPE_CHECKING:
    from datetime import date
    from .models import User


@dataclasses.dataclass
class UserDataClass:
    first_name: str
    last_name: str
    email: str
    birthdate: "date" = None
    phone: str = None
    id: int = None
    password: str = None
    password2: str = None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            birthdate=user.birthdate,
            phone=user.phone,
        )


def create_user(user: "UserDataClass") -> "UserDataClass":
    instance = User(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        birthdate=user.birthdate,
        phone=user.phone,
    )

    if user.password is not None:
        instance.set_password(user.password)

    instance.save()

    return UserDataClass.from_instance(user=instance)


def create_token(user_id: int) -> str:
    payload = dict(
        id = user_id,
        exp=timezone.datetime.utcnow() + timezone.timedelta(hours=24),
        iat=timezone.datetime.utcnow()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token
