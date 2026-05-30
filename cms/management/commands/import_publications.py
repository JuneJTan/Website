import json
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from cms.models import Publication


TYPE_MAP = {
    "Journal": "journal",
    "Book": "book",
    "Conference": "conference",
    "Workshop": "workshop",
}


class Command(BaseCommand):
    help = "Import extracted publication JSON from the legacy website archive."

    def add_arguments(self, parser):
        parser.add_argument(
            "json_path",
            nargs="?",
            default="legacy_reference/extracted_publications/publications.json",
            help="Path to extracted publications JSON.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing publications before importing.",
        )

    def handle(self, *args, **options):
        path = Path(options["json_path"])
        if not path.exists():
            raise CommandError(f"JSON file not found: {path}")

        clear_existing = options["clear"]
        if clear_existing:
            Publication.objects.all().delete()

        payload = json.loads(path.read_text(encoding="utf-8"))
        created = 0
        skipped = 0

        for source_type, items in payload.items():
            publication_type = TYPE_MAP.get(source_type)
            if not publication_type:
                self.stderr.write(f"Skipping unknown type: {source_type}")
                continue

            for index, item in enumerate(items):
                raw = item.get("text", "").strip()
                if not raw:
                    skipped += 1
                    continue

                year = self.extract_year(raw)
                title = self.extract_title(raw)
                if clear_existing:
                    Publication.objects.create(
                        raw_citation=raw,
                        publication_type=publication_type,
                        title=title,
                        year=year,
                        display_order=index,
                        is_visible=True,
                    )
                    created += 1
                    continue

                _, was_created = Publication.objects.get_or_create(
                    raw_citation=raw,
                    publication_type=publication_type,
                    defaults={
                        "title": title,
                        "year": year,
                        "display_order": index,
                        "is_visible": True,
                    },
                )
                created += int(was_created)
                skipped += int(not was_created)

        self.stdout.write(self.style.SUCCESS(f"Imported {created} publications, skipped {skipped}."))

    @staticmethod
    def extract_year(text):
        matches = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
        if not matches:
            return None
        return int(matches[-1])

    @staticmethod
    def extract_title(text):
        match = re.search(r'"([^"]{8,})"', text)
        if match:
            return match.group(1).strip()
        match = re.search(r"“([^”]{8,})”", text)
        if match:
            return match.group(1).strip()
        return text[:220]
