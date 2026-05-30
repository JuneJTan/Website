from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render

from .models import Course, NewsItem, Person, Position, Publication, ResearchArea, SiteProfile


def home(request):
    profile = SiteProfile.objects.order_by("-updated_at").first()
    publication_query = request.GET.get("q", "").strip()
    publication_type = request.GET.get("type", "").strip()

    publications = Publication.objects.filter(is_visible=True)
    if publication_query:
        publications = publications.filter(
            Q(title__icontains=publication_query)
            | Q(authors__icontains=publication_query)
            | Q(venue__icontains=publication_query)
            | Q(raw_citation__icontains=publication_query)
            | Q(doi__icontains=publication_query)
        )
    if publication_type in dict(Publication.TYPE_CHOICES):
        publications = publications.filter(publication_type=publication_type)

    publication_params = request.GET.copy()
    publication_params.pop("page", None)
    publication_querystring = publication_params.urlencode()
    publication_page = Paginator(publications, 8).get_page(request.GET.get("page"))

    publication_counts = dict(
        Publication.objects.filter(is_visible=True)
        .values_list("publication_type")
        .annotate(total=Count("id"))
    )
    context = {
        "profile": profile,
        "research_areas": ResearchArea.objects.filter(is_visible=True)[:4],
        "people_groups": Person.objects.filter(is_visible=True).values("role").annotate(total=Count("id")),
        "courses": Course.objects.filter(is_visible=True)[:3],
        "news_items": NewsItem.objects.filter(is_visible=True)[:2],
        "open_positions": Position.objects.filter(is_visible=True, status="open")[:1],
        "publication_page": publication_page,
        "publication_query": publication_query,
        "selected_publication_type": publication_type,
        "publication_querystring": publication_querystring,
        "publication_type_choices": Publication.TYPE_CHOICES,
        "publication_counts": {
            "journal": publication_counts.get("journal", 110),
            "book": publication_counts.get("book", 4),
            "conference": publication_counts.get("conference", 135),
            "workshop": publication_counts.get("workshop", 35),
        },
    }
    return render(request, "home.html", context)
