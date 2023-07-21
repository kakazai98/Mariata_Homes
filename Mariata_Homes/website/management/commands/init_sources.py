
from django.core.management.base import BaseCommand
from website.models import Source

class Command(BaseCommand):
    help = 'Initializes the Source objects in the database'

    def handle(self, *args, **options):
        sources = [
            ('Police Station', '123 Main St'),
            ('Prison Release', '456 Elm St'),
            ('Immigration Release', '789 Oak St'),
            ('Other', '321 Pine St')
        ]

        for source_type, source_address in sources:
            if not Source.objects.filter(source_type=source_type).exists():
                source = Source(
                    source_type=source_type,
                    source_address=source_address
                )
                source.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created {source_type} object with address {source_address}'))
