"""
Management command to bulk-import art images from a local folder.

Usage:
    python manage.py import_prints "F:\David Folders\Pictures\Molishi Collection"

Images are copied into MEDIA_ROOT/prints/ and an ArtPrint record is
created for each one.  A default Category is created if none exists.
"""

import os
import shutil
from pathlib import Path
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify

from gallery.models import ArtPrint, Category


SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}


def _clean_title(filename: str) -> str:
    """
    Turn a filename like
      Molishi_Mysticals_Molishi_at_the_ancient_temple_0.jpg
    into a human-readable title like
      Molishi At The Ancient Temple
    """
    stem = Path(filename).stem                       # drop extension
    stem = stem.replace('Molishi_Mysticals_', '')    # drop common prefix
    stem = stem.replace('_', ' ')                    # underscores → spaces

    # Strip trailing variant numbers like " 0", " 1", " 01"
    parts = stem.rsplit(' ', 1)
    if len(parts) == 2 and parts[1].isdigit():
        stem = parts[0]

    return stem.strip().title()


class Command(BaseCommand):
    help = 'Import art images from a folder into the gallery'

    def add_arguments(self, parser):
        parser.add_argument(
            'source',
            type=str,
            help='Path to folder containing images',
        )
        parser.add_argument(
            '--category',
            type=str,
            default='Molishi Mysticals',
            help='Category name for all imported prints (default: Molishi Mysticals)',
        )
        parser.add_argument(
            '--price',
            type=str,
            default='50.00',
            help='Default price for each print (default: 50.00)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be imported without making changes',
        )

    def handle(self, *args, **options):
        source_dir = Path(options['source'])
        category_name = options['category']
        price = Decimal(options['price'])
        dry_run = options['dry_run']

        if not source_dir.exists():
            self.stderr.write(self.style.ERROR(f'Source folder not found: {source_dir}'))
            return

        # Collect image files (root only, no subfolders)
        images = sorted([
            f for f in source_dir.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ])

        if not images:
            self.stderr.write(self.style.WARNING(f'No image files found in {source_dir}'))
            return

        self.stdout.write(f'Found {len(images)} images in {source_dir}')

        if dry_run:
            self.stdout.write(self.style.WARNING('\n--- DRY RUN (no changes made) ---\n'))
            for img in images:
                title = _clean_title(img.name)
                self.stdout.write(f'  {img.name}  →  "{title}"  £{price}')
            self.stdout.write(f'\nWould create {len(images)} prints in category "{category_name}"')
            return

        # Create / get category
        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'description': f'Art prints from the {category_name} collection.'},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {category_name}'))
        else:
            self.stdout.write(f'Using existing category: {category_name}')

        # Destination inside MEDIA_ROOT
        dest_dir = Path(settings.MEDIA_ROOT) / 'prints'
        dest_dir.mkdir(parents=True, exist_ok=True)

        imported = 0
        skipped = 0

        for img in images:
            title = _clean_title(img.name)
            slug = slugify(title)

            # Skip if a print with this slug already exists
            if ArtPrint.objects.filter(slug=slug).exists():
                self.stdout.write(self.style.WARNING(f'  SKIP (exists): {title}'))
                skipped += 1
                continue

            # Handle duplicate slugs from variant numbers
            # e.g. two files both clean to "Molishi At The Ancient Temple"
            base_slug = slug
            counter = 1
            while ArtPrint.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            # Copy image to media/prints/
            dest_path = dest_dir / img.name
            if not dest_path.exists():
                shutil.copy2(str(img), str(dest_path))

            # Create the ArtPrint record
            relative_path = f'prints/{img.name}'
            ArtPrint.objects.create(
                title=title,
                slug=slug,
                description=f'"{title}" — from the {category_name} collection by Joe Django.',
                image=relative_path,
                category=category,
                price=price,
                is_available=True,
            )
            self.stdout.write(self.style.SUCCESS(f'  ✓ {img.name}  →  "{title}"'))
            imported += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Imported: {imported}'))
        if skipped:
            self.stdout.write(self.style.WARNING(f'Skipped (already exist): {skipped}'))
        self.stdout.write(self.style.SUCCESS('Done!'))
