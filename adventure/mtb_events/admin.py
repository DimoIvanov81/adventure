from django.contrib import admin
from .models import MtbEvent, MtbEventImage, Participation


@admin.register(MtbEvent)
class MtbEventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "date_created", "is_published", "date_created")
    list_filter = ("is_published", "date_created")
    search_fields = ("title", "organizer__email")
    list_editable = ("is_published",)


@admin.register(MtbEventImage)
class MtbEventImageAdmin(admin.ModelAdmin):
    list_display = ("event", "description")
    search_fields = ("event__title",)


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "contact_email", "contact_phone")
    search_fields = ("event__title", "user__email")
