from django.contrib import admin

from .models import (
    Course,
    NewsItem,
    Person,
    Position,
    Publication,
    ResearchArea,
    SiteProfile,
)


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic", {"fields": ("name_en", "name_cn", "subtitle_en", "subtitle_cn", "hero_title", "hero_text")}),
        ("Contact", {"fields": ("email", "orcid_url", "google_scholar_url", "address_en", "address_cn")}),
        ("Images", {"fields": ("sustech_logo", "department_logo", "lab_logo", "hero_image", "professor_photo", "professor_name_image", "orcid_icon")}),
    )


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_cn", "display_order", "is_visible")
    list_editable = ("display_order", "is_visible")
    search_fields = ("title_en", "title_cn", "summary_en", "summary_cn")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_cn", "role", "graduation_year", "display_order", "is_visible")
    list_filter = ("role", "is_visible", "graduation_year")
    list_editable = ("display_order", "is_visible")
    search_fields = ("name_en", "name_cn", "bio_en", "bio_cn", "current_position")


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("short_title", "publication_type", "year", "is_featured", "is_visible", "display_order")
    list_filter = ("publication_type", "year", "is_featured", "is_visible")
    list_editable = ("is_featured", "is_visible", "display_order")
    search_fields = ("title", "authors", "venue", "doi", "raw_citation")

    @admin.display(description="Title")
    def short_title(self, obj):
        return obj.title[:90]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_cn", "years", "display_order", "is_visible")
    list_editable = ("display_order", "is_visible")
    search_fields = ("name_en", "name_cn", "description_en", "description_cn")


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title_en", "publish_date", "is_pinned", "is_visible")
    list_filter = ("is_pinned", "is_visible", "publish_date")
    list_editable = ("is_pinned", "is_visible")
    search_fields = ("title_en", "title_cn", "body_en", "body_cn")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("title_en", "category", "status", "publish_date", "deadline", "is_visible")
    list_filter = ("status", "category", "is_visible")
    list_editable = ("status", "is_visible")
    search_fields = ("title_en", "title_cn", "description_en", "description_cn")
