from django.core.management import BaseCommand

from ...runner import prompt_manual_data


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        prompt_manual_data()
