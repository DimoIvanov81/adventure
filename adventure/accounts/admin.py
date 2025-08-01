from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppProfile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = UserModel

    list_display = ("pk", "email", "is_active", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("pk",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Status", {"fields": ("is_active",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):

        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        else:
            readonly = [f.name for f in self.model._meta.fields if f.name != "is_active"]
            return readonly


@admin.register(AppProfile)
class AppProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "date_of_birth")
    search_fields = ("first_name", "last_name", "user__email")

    def get_readonly_fields(self, request, obj=None):

        return [f.name for f in self.model._meta.fields]
