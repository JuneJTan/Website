from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render

from .models import Course, NewsItem, Person, Position, Publication, ResearchArea, SiteProfile


def localized(value_cn, value_en, is_zh):
    if is_zh and value_cn:
        return value_cn
    return value_en


def int_param(request, name):
    value = request.GET.get(name, "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def home(request, lang="en"):
    is_zh = lang == "zh"
    profile = SiteProfile.objects.order_by("-updated_at").first()
    publication_query = request.GET.get("q", "").strip()
    publication_type = request.GET.get("type", "").strip()
    year = int_param(request, "year")
    year_from = int_param(request, "year_from")
    year_to = int_param(request, "year_to")
    per_page = int_param(request, "per_page") or 10
    if per_page not in {5, 10, 20}:
        per_page = 10

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
    if year:
        publications = publications.filter(year=year)
    else:
        if year_from:
            publications = publications.filter(year__gte=year_from)
        if year_to:
            publications = publications.filter(year__lte=year_to)

    publication_params = request.GET.copy()
    publication_params.pop("page", None)
    publication_querystring = publication_params.urlencode()
    publication_page = Paginator(publications, per_page).get_page(request.GET.get("page"))
    publication_elided_page_range = publication_page.paginator.get_elided_page_range(
        number=publication_page.number,
        on_each_side=1,
        on_ends=2,
    )

    publication_counts = dict(
        Publication.objects.filter(is_visible=True)
        .values_list("publication_type")
        .annotate(total=Count("id"))
    )
    years = [
        value
        for value in Publication.objects.filter(is_visible=True, year__isnull=False)
        .order_by("-year")
        .values_list("year", flat=True)
        .distinct()
    ]

    labels = {
        "research": "研究方向" if is_zh else "Research",
        "people": "团队成员" if is_zh else "People",
        "publications": "论文成果" if is_zh else "Publications",
        "teaching": "教学课程" if is_zh else "Teaching",
        "news": "新闻动态" if is_zh else "News",
        "join_us": "加入我们" if is_zh else "Join Us",
        "biography": "个人简介" if is_zh else "Biography",
        "search": "搜索" if is_zh else "Search",
        "all_categories": "全部分类" if is_zh else "All categories",
        "all_publications": "全部论文" if is_zh else "All Publications",
        "journal": "期刊论文" if is_zh else "Journal Papers",
        "book": "书籍与章节" if is_zh else "Books and Chapters",
        "conference": "会议论文" if is_zh else "Conference Proceedings",
        "workshop": "特邀报告与研讨会" if is_zh else "Invited Seminars",
        "contact_email": "邮件联系" if is_zh else "Contact by Email",
        "email": "邮箱" if is_zh else "Email",
        "homepage": "主页" if is_zh else "Homepage",
        "view_team": "查看团队" if is_zh else "View Team",
        "download_details": "下载详情" if is_zh else "Download Details",
        "prev": "上一页" if is_zh else "Prev",
        "next": "下一页" if is_zh else "Next",
        "no_publications": "没有符合当前条件的论文。" if is_zh else "No publications match the current filters.",
        "no_results": "无结果" if is_zh else "No results",
        "no_publications_found": "未找到论文" if is_zh else "No publications found",
        "try_different_search": "请尝试其他关键词或分类。" if is_zh else "Try a different keyword or category.",
        "bio_academic_path": "学术经历" if is_zh else "Academic Path",
        "bio_sustech_appointment": "南科大任职" if is_zh else "SUSTech Appointment",
        "bio_professional_service": "学术服务" if is_zh else "Professional Service",
        "bio_conference_activity": "会议活动" if is_zh else "Conference Activity",
        "items_per_page": "每页显示" if is_zh else "Items per page",
        "year": "年份" if is_zh else "Year",
        "year_from": "起始年份" if is_zh else "From year",
        "year_to": "结束年份" if is_zh else "To year",
        "all_years": "全部年份" if is_zh else "All years",
        "search_placeholder": "搜索标题、作者、期刊/会议或 DOI" if is_zh else "Search title, author, venue, DOI",
        "per_page_suffix": "条/页" if is_zh else "/page",
    }
    defaults = {
        "hero_text": "研究方向包括空间映射、代理模型、仿真驱动优化、微波电路、天线和射频工程。" if is_zh else "Research in space mapping, surrogate modeling, simulation-driven optimization, microwave circuits, antennas, and RF engineering.",
        "biography": "程庆沙教授本科和硕士毕业于重庆大学自动化专业，2004 年获加拿大麦克马斯特大学博士学位，现任南方科技大学副教授。" if is_zh else "Qingsha (Shasha) Cheng received the B.Eng. and M.Eng. degrees in automation from Chongqing University, China, and the Ph.D. degree from McMaster University, Canada, in 2004. He is currently an associate professor at Southern University of Science and Technology in Shenzhen, China.",
        "research_focus": "他的研究聚焦于空间映射、代理模型、基于仿真的调谐、计算机辅助设计，以及微波电路、天线和射频系统的快速建模与优化。" if is_zh else "His research focuses on space mapping, surrogate modeling, simulator-based tuning, computer-aided design, and fast modeling and optimization methods for microwave circuits, antennas, and RF systems.",
        "bio_academic_path": "曾于 1998 年在北京大学计算机科学技术系工作，1999 年加入麦克马斯特大学电气与计算机工程系 Simulation Optimization Systems Research Laboratory，之后担任博士后、研究助理、研究工程师和兼职讲师。" if is_zh else "He worked with Peking University in 1998 and joined the Simulation Optimization Systems Research Laboratory at McMaster University in 1999, later serving as a postdoctoral fellow, research associate, research engineer, and sessional lecturer.",
        "bio_sustech_appointment": "2014 年加入南方科技大学任助理教授，后成为长聘副教授。2018 年受聘为加拿大里贾纳大学 Adjunct Professor。" if is_zh else "He joined SUSTech in 2014 as an assistant professor and later became a tenured associate professor. He was appointed Adjunct Professor with the University of Regina, Canada, in 2018.",
        "bio_professional_service": "担任 International Journal of Numerical Modelling: Electronic Networks, Devices and Fields 副主编，并长期为微波、天线等领域重要期刊审稿。" if is_zh else "He has served as an associate editor of the International Journal of Numerical Modelling: Electronic Networks, Devices and Fields, and has reviewed for major microwave and antenna journals.",
        "bio_conference_activity": "组织或主持 SMSMEO、IEEE IMS、IEEE NEMO、IEEE ICCS、IEEE ACES、IEEE ICCEM 和 ACES-China 等会议、研讨会和专题活动。" if is_zh else "He has organized or chaired workshops and sessions for SMSMEO, IEEE IMS, IEEE NEMO, IEEE ICCS, IEEE ACES, IEEE ICCEM, and ACES-China, including electromagnetic modeling and optimization activities for IEEE MTT-S Young Professionals.",
        "bio_impact": "空间映射算法的早期贡献者之一，拥有 25 年以上研究经验。截至 2026 年 4 月，Google Scholar 引用超过 5800 次。" if is_zh else "One of the original contributors to the Space Mapping algorithm, with more than 25 years of research experience and more than 5800 Google Scholar citations as of April 2026.",
    }
    site = {
        "name": localized(profile.name_cn, profile.name_en, is_zh) if profile else ("程庆沙课题组" if is_zh else "em+ Lab"),
        "subtitle": localized(profile.subtitle_cn, profile.subtitle_en, is_zh) if profile else ("南方科技大学" if is_zh else "Southern University of Science and Technology"),
        "hero_title": localized(profile.hero_title_cn, profile.hero_title, is_zh) if profile else ("程庆沙课题组" if is_zh else "em+ Lab"),
        "hero_text": (localized(profile.hero_text_cn, profile.hero_text, is_zh) if profile else "") or defaults["hero_text"],
        "professor_name": localized(profile.professor_name_cn, profile.professor_name_en, is_zh) if profile else ("程庆沙" if is_zh else "Qingsha S. Cheng"),
        "professor_title": localized(profile.professor_title_cn, profile.professor_title_en, is_zh) if profile else ("南方科技大学副教授" if is_zh else "Associate Professor, SUSTech"),
        "biography": (localized(profile.biography_cn, profile.biography_en, is_zh) if profile else "") or defaults["biography"],
        "research_focus": (localized(profile.research_focus_cn, profile.research_focus_en, is_zh) if profile else "") or defaults["research_focus"],
        "bio_academic_path": (localized(profile.bio_academic_path_cn, profile.bio_academic_path_en, is_zh) if profile else "") or defaults["bio_academic_path"],
        "bio_sustech_appointment": (localized(profile.bio_sustech_appointment_cn, profile.bio_sustech_appointment_en, is_zh) if profile else "") or defaults["bio_sustech_appointment"],
        "bio_professional_service": (localized(profile.bio_professional_service_cn, profile.bio_professional_service_en, is_zh) if profile else "") or defaults["bio_professional_service"],
        "bio_conference_activity": (localized(profile.bio_conference_activity_cn, profile.bio_conference_activity_en, is_zh) if profile else "") or defaults["bio_conference_activity"],
        "bio_impact": (localized(profile.bio_impact_cn, profile.bio_impact_en, is_zh) if profile else "") or defaults["bio_impact"],
    }

    research_areas = [
        {
            "number": f"{idx:02d}",
            "title": localized(area.title_cn, area.title_en, is_zh),
            "summary": localized(area.summary_cn, area.summary_en, is_zh),
        }
        for idx, area in enumerate(ResearchArea.objects.filter(is_visible=True)[:4], start=1)
    ]
    courses = [
        {
            "name": localized(course.name_cn, course.name_en, is_zh),
            "description": localized(course.description_cn, course.description_en, is_zh) or course.years,
        }
        for course in Course.objects.filter(is_visible=True)[:3]
    ]
    news_items = [
        {
            "title": localized(item.title_cn, item.title_en, is_zh),
            "body": localized(item.body_cn, item.body_en, is_zh),
            "cover_image": item.cover_image,
        }
        for item in NewsItem.objects.filter(is_visible=True)[:2]
    ]
    open_positions = [
        {
            "title": localized(position.title_cn, position.title_en, is_zh),
            "description": localized(position.description_cn, position.description_en, is_zh),
            "attachment": position.attachment,
        }
        for position in Position.objects.filter(is_visible=True, status="open")[:3]
    ]
    role_labels = {
        "faculty": "教师" if is_zh else "Faculty",
        "research_staff": "研究人员" if is_zh else "Research Staff",
        "postdoc": "博士后" if is_zh else "Postdoctoral Fellows",
        "phd": "博士研究生" if is_zh else "Ph.D. Students",
        "master": "硕士研究生" if is_zh else "Master Students",
        "alumni_phd": "博士毕业生" if is_zh else "Ph.D. Alumni",
        "alumni_master": "硕士毕业生" if is_zh else "Master Alumni",
    }
    people_qs = Person.objects.filter(is_visible=True)
    people_sections = []
    for role, _label in Person.ROLE_CHOICES:
        members = []
        for person in people_qs.filter(role=role):
            members.append(
                {
                    "name": localized(person.name_cn, person.name_en, is_zh) or person.name_en,
                    "role": role_labels.get(role, _label),
                    "bio": localized(person.bio_cn, person.bio_en, is_zh) or person.current_position,
                    "photo": person.photo,
                    "email": person.email,
                    "homepage": person.homepage,
                    "graduation_year": person.graduation_year,
                    "current_position": person.current_position,
                }
            )
        if members:
            people_sections.append(
                {
                    "role": role,
                    "label": role_labels.get(role, _label),
                    "members": members,
                }
            )
    publication_type_choices = [
        ("journal", labels["journal"]),
        ("book", labels["book"]),
        ("conference", labels["conference"]),
        ("workshop", labels["workshop"]),
    ]

    home_url_name = "home_zh" if is_zh else "home"
    context = {
        "is_zh": is_zh,
        "labels": labels,
        "home_url_name": home_url_name,
        "language_url": "/" if is_zh else "/zh/",
        "language_label": "English" if is_zh else "中文",
        "profile": profile,
        "site": site,
        "research_areas": research_areas,
        "people_groups": Person.objects.filter(is_visible=True).values("role").annotate(total=Count("id")),
        "people_sections": people_sections,
        "courses": courses,
        "news_items": news_items,
        "open_positions": open_positions,
        "publication_page": publication_page,
        "publication_elided_page_range": publication_elided_page_range,
        "publication_query": publication_query,
        "selected_publication_type": publication_type,
        "publication_querystring": publication_querystring,
        "publication_type_choices": publication_type_choices,
        "publication_counts": {
            "journal": publication_counts.get("journal", 0),
            "book": publication_counts.get("book", 0),
            "conference": publication_counts.get("conference", 0),
            "workshop": publication_counts.get("workshop", 0),
        },
        "years": years,
        "selected_year": year,
        "year_from": year_from or "",
        "year_to": year_to or "",
        "per_page": per_page,
        "per_page_options": [5, 10, 20],
    }
    return render(request, "home.html", context)
