from django.core.management import BaseCommand

from ... import runner


class Command(BaseCommand):
    def add_arguments(self, parser):
        choices = ['getmanual', 'getauto']
        parser.add_argument('command', choices=choices)

    def handle(self, *args, **kwargs):
        if kwargs['command'] == 'getmanual':
            runner.prompt_manual_data()
        elif kwargs['command'] == 'getauto':
            runner.run_auto_fetchers()
