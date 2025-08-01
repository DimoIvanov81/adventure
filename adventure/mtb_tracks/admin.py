from django.contrib import admin
from .models import MtbTracks, TrackImages, Comment


@admin.register(MtbTracks)
class MtbTracksAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "difficulty", "date_created", "is_published")
    list_filter = ("difficulty", "is_published", "date_created")
    search_fields = ("title", "author__email")
    list_editable = ("is_published",)


@admin.register(TrackImages)
class TrackImagesAdmin(admin.ModelAdmin):
    list_display = ("track", "description")
    search_fields = ("track__title",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("track", "author", "is_visible", "date_created")
    list_filter = ("is_visible", "date_created")
    search_fields = ("author__email", "track__title")
    list_editable = ("is_visible",)
