import datetime
from django.core.management import BaseCommand


class Command(BaseCommand):
    # args = '<uid uid ...>'
    help = 'Used for debugging'

    def add_arguments(self, parser):
        parser.add_argument('n', nargs='?', type=int)

    def handle(self, *args, **options):
        # translation.activate('zh-cn')

        for uid in args:
            self.stdout.write(str(uid))

        self.stdout.write('cmd handler of simple msg:) ')


