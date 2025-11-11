import json
from django.core.management.base import BaseCommand
from quotes.models import Quote

class Command(BaseCommand):
    help = 'Load quotes from quotes.json'

    def handle(self, *args, **kwargs):
        with open('quotes/quotes.json', 'r') as f:
            data = json.load(f)
            for item in data:
                Quote.objects.create(
                    text=item['quote'],
                    author=item['author'],
                    tags=",".join(item.get('tags', []))
                )
        self.stdout.write(self.style.SUCCESS("Quotes loaded successfully."))
