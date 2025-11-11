import random
from django.shortcuts import render
from django.http import JsonResponse
from .models import Quote

def home(request):
    quote = random.choice(Quote.objects.all())
    return render(request, 'quotes/home.html', {'quote': quote})

def random_quote_api(request):
    quote = random.choice(Quote.objects.all())
    return JsonResponse({
        'quote': quote.text,
        'author': quote.author,
        'tags': quote.tags.split(',') if quote.tags else []
    })
