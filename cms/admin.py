from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from .bibtex import parse_bibtex, publication_defaults
from .forms import BibTeXImportForm

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
        ("Basic", {"fields": ("name_en", "name_cn", "subtitle_en", "subtitle_cn")}),
        ("Hero - English", {"fields": ("hero_title", "hero_text")}),
        ("Hero - Chinese", {"fields": ("hero_title_cn", "hero_text_cn")}),
        ("Professor - English", {"fields": ("professor_name_en", "professor_title_en", "biography_en", "research_focus_en")}),
        ("Professor - Chinese", {"fields": ("professor_name_cn", "professor_title_cn", "biography_cn", "research_focus_cn")}),
        ("Biography Cards - English", {"fields": ("bio_academic_path_en", "bio_sustech_appointment_en", "bio_professional_service_en", "bio_conference_activity_en", "bio_impact_en")}),
        ("Biography Cards - Chinese", {"fields": ("bio_academic_path_cn", "bio_sustech_appointment_cn", "bio_professional_service_cn", "bio_conference_activity_cn", "bio_impact_cn")}),
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
    change_list_template = "admin/cms/publication/change_list.html"
    list_display = ("short_title", "publication_type", "year", "is_featured", "is_visible", "display_order")
    list_filter = ("publication_type", "year", "is_featured", "is_visible")
    list_editable = ("is_featured", "is_visible", "display_order")
    search_fields = ("title", "authors", "venue", "doi", "raw_citation")

    @admin.display(description="Title")
    def short_title(self, obj):
        return obj.title[:90]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-bibtex/",
                self.admin_site.admin_view(self.import_bibtex_view),
                name="cms_publication_import_bibtex",
            ),
        ]
        return custom_urls + urls

    def import_bibtex_view(self, request):
        if request.method == "POST":
            form = BibTeXImportForm(request.POST, request.FILES)
            if form.is_valid():
                text = form.cleaned_data.get("bibtex_text") or ""
                upload = form.cleaned_data.get("bibtex_file")
                if upload:
                    text += "\n" + upload.read().decode("utf-8", errors="replace")

                entries = parse_bibtex(text)
                created = 0
                skipped = 0
                for entry in entries:
                    defaults = publication_defaults(entry)
                    if not defaults["raw_citation"]:
                        skipped += 1
                        continue
                    Publication.objects.create(**defaults)
                    created += 1

                if created:
                    self.message_user(request, f"已成功导入 {created} 条论文。", messages.SUCCESS)
                if skipped:
                    self.message_user(request, f"{skipped} 条 BibTeX 未能生成有效引用，已跳过。", messages.WARNING)
                if not entries:
                    self.message_user(request, "没有解析到有效 BibTeX 条目。", messages.ERROR)
                return redirect("..")
        else:
            form = BibTeXImportForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "导入 BibTeX",
            "opts": self.model._meta,
            "form": form,
        }
        return render(request, "admin/cms/publication/import_bibtex.html", context)


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
