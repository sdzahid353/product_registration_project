from django.core.management.base import BaseCommand
import shutil
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Backs up the SQLite database'

    def handle(self, *args, **options):
        backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        os.makedirs(backup_dir, exist_ok=True)

        db_path = settings.DATABASES['default']['NAME']
        backup_path = os.path.join(backup_dir, 'db_backup.sqlite3')

        shutil.copy(db_path, backup_path)

        self.stdout.write(self.style.SUCCESS(f"Database backup created successfully at {backup_path}"))
