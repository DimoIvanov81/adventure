# adventure/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import AppUserCreationForm, AppUserChangeForm
from .models import AppProfile

UserModel = get_user_model()
USERNAME_FIELD = UserModel.USERNAME_FIELD


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    add_form = AppUserCreationForm
    form = AppUserChangeForm
    model = UserModel

    list_display = ("pk", USERNAME_FIELD, "is_active", "is_staff", "is_superuser")
    search_fields = (USERNAME_FIELD,)
    ordering = ("pk",)

    fieldsets = (
        (None, {"fields": (USERNAME_FIELD, "password")}),
        ("Status", {"fields": ("is_active", "is_staff")}),
        ("Permissions", {"fields": ("is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (USERNAME_FIELD, "password1", "password2", "is_staff"),
        }),
    )

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_model_perms(request)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj is None:
            return True
        return bool(obj.is_staff or obj.is_superuser)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj is None:
            return True
        return bool(not obj.is_staff and not obj.is_superuser)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        if obj is None:
            return ()
        return "last_login", "date_joined"


@admin.register(AppProfile)
class AppProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "date_of_birth")
    search_fields = ("first_name", "last_name", "user__email")

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj is None:
            return True
        return bool(obj.user.is_staff or obj.user.is_superuser)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        if obj is None:
            return True
        return bool(not obj.user.is_staff and not obj.user.is_superuser)

