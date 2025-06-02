# Vendor
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Auto creating groups"

    def handle(self, *args, **options):
        # Оператор заявок
        Group.objects.get_or_create(name='operator')
        self.stdout.write(self.style.SUCCESS("Groups created successfully "))


