from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "birthdate",
        "phone",
        "date_joined",
        "image",
    )


admin.site.register(User, UserAdmin)
