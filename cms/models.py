from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteProfile(TimeStampedModel):
    name_en = models.CharField(max_length=120, default="em+ Lab")
    name_cn = models.CharField(max_length=120, blank=True)
    subtitle_en = models.CharField(max_length=240, blank=True)
    subtitle_cn = models.CharField(max_length=240, blank=True)
    hero_title = models.CharField(max_length=160, default="em+ Lab")
    hero_title_cn = models.CharField(max_length=160, blank=True)
    hero_text = models.TextField(blank=True)
    hero_text_cn = models.TextField(blank=True)
    professor_name_en = models.CharField(max_length=160, default="Qingsha S. Cheng")
    professor_name_cn = models.CharField(max_length=160, blank=True)
    professor_title_en = models.CharField(max_length=160, default="Associate Professor, SUSTech")
    professor_title_cn = models.CharField(max_length=160, blank=True)
    biography_en = models.TextField(blank=True)
    biography_cn = models.TextField(blank=True)
    research_focus_en = models.TextField(blank=True)
    research_focus_cn = models.TextField(blank=True)
    bio_academic_path_en = models.TextField(blank=True)
    bio_academic_path_cn = models.TextField(blank=True)
    bio_sustech_appointment_en = models.TextField(blank=True)
    bio_sustech_appointment_cn = models.TextField(blank=True)
    bio_professional_service_en = models.TextField(blank=True)
    bio_professional_service_cn = models.TextField(blank=True)
    bio_conference_activity_en = models.TextField(blank=True)
    bio_conference_activity_cn = models.TextField(blank=True)
    bio_impact_en = models.TextField(blank=True)
    bio_impact_cn = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    orcid_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    address_en = models.CharField(max_length=240, blank=True)
    address_cn = models.CharField(max_length=240, blank=True)
    sustech_logo = models.FileField(upload_to="site/logos/", blank=True)
    department_logo = models.FileField(upload_to="site/logos/", blank=True)
    lab_logo = models.FileField(upload_to="site/logos/", blank=True)
    hero_image = models.FileField(upload_to="site/hero/", blank=True)
    professor_photo = models.FileField(upload_to="site/profile/", blank=True)
    professor_name_image = models.FileField(upload_to="site/profile/", blank=True)
    orcid_icon = models.FileField(upload_to="site/icons/", blank=True)

    class Meta:
        verbose_name = "站点资料"
        verbose_name_plural = "站点资料"

    def __str__(self):
        return self.name_en


class ResearchArea(TimeStampedModel):
    title_en = models.CharField(max_length=160)
    title_cn = models.CharField(max_length=160, blank=True)
    summary_en = models.TextField(blank=True)
    summary_cn = models.TextField(blank=True)
    image = models.FileField(upload_to="research/", blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "title_en"]
        verbose_name = "研究方向"
        verbose_name_plural = "研究方向"

    def __str__(self):
        return self.title_en


class Person(TimeStampedModel):
    ROLE_CHOICES = [
        ("faculty", "Faculty"),
        ("research_staff", "Research staff"),
        ("postdoc", "Postdoctoral fellow"),
        ("phd", "Ph.D. student"),
        ("master", "Master student"),
        ("alumni_phd", "Ph.D. alumnus"),
        ("alumni_master", "Master alumnus"),
    ]

    name_en = models.CharField(max_length=120)
    name_cn = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    bio_en = models.TextField(blank=True)
    bio_cn = models.TextField(blank=True)
    photo = models.FileField(upload_to="people/", blank=True)
    email = models.EmailField(blank=True)
    homepage = models.URLField(blank=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True)
    current_position = models.CharField(max_length=240, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name_en"]
        verbose_name = "团队成员"
        verbose_name_plural = "团队成员"

    def __str__(self):
        return self.name_en


class Publication(TimeStampedModel):
    TYPE_CHOICES = [
        ("journal", "Journal paper"),
        ("book", "Book or book chapter"),
        ("conference", "Conference proceeding"),
        ("workshop", "Workshop or invited seminar"),
    ]

    title = models.TextField()
    authors = models.TextField(blank=True)
    publication_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    venue = models.CharField(max_length=260, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    volume = models.CharField(max_length=80, blank=True)
    issue = models.CharField(max_length=80, blank=True)
    pages = models.CharField(max_length=80, blank=True)
    doi = models.CharField(max_length=160, blank=True)
    external_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to="publications/pdfs/", blank=True)
    raw_citation = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-year", "display_order", "title"]
        verbose_name = "论文成果"
        verbose_name_plural = "论文成果"

    def __str__(self):
        return self.title[:100]

    @property
    def type_label_cn(self):
        return {
            "journal": "期刊论文",
            "book": "书籍与章节",
            "conference": "会议论文",
            "workshop": "特邀报告与研讨会",
        }.get(self.publication_type, self.get_publication_type_display())

    @property
    def citation_text(self):
        if self.raw_citation:
            return self.raw_citation

        parts = []
        if self.authors:
            parts.append(self.authors.rstrip("."))
        if self.title:
            parts.append(f'"{self.title.rstrip(".")},"')
        if self.venue:
            parts.append(self.venue.rstrip("."))

        citation = " ".join(parts).strip()
        if citation and citation[-1] not in ".!?":
            citation += "."
        return citation or self.title


class Course(TimeStampedModel):
    name_en = models.CharField(max_length=180)
    name_cn = models.CharField(max_length=180, blank=True)
    years = models.CharField(max_length=80, blank=True)
    description_en = models.TextField(blank=True)
    description_cn = models.TextField(blank=True)
    course_url = models.CharField(max_length=240, blank=True)
    attachment = models.FileField(upload_to="courses/", blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name_en"]
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return self.name_en


class NewsItem(TimeStampedModel):
    title_en = models.CharField(max_length=220)
    title_cn = models.CharField(max_length=220, blank=True)
    body_en = models.TextField(blank=True)
    body_cn = models.TextField(blank=True)
    cover_image = models.FileField(upload_to="news/", blank=True)
    publish_date = models.DateField(blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-is_pinned", "-publish_date", "-created_at"]
        verbose_name = "新闻动态"
        verbose_name_plural = "新闻动态"

    def __str__(self):
        return self.title_en


class Position(TimeStampedModel):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("archived", "Archived"),
    ]

    title_en = models.CharField(max_length=220)
    title_cn = models.CharField(max_length=220, blank=True)
    category = models.CharField(max_length=80, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    description_en = models.TextField(blank=True)
    description_cn = models.TextField(blank=True)
    attachment = models.FileField(upload_to="positions/", blank=True)
    publish_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["status", "-publish_date", "title_en"]
        verbose_name = "招生招聘"
        verbose_name_plural = "招生招聘"

    def __str__(self):
        return self.title_en
