import os
import zipfile

project_name = "zenquotes_django"
app_name = "quotes"

files_to_create = {
    f"{project_name}/manage.py": """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zenquotes.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",
    f"{project_name}/{project_name}/__init__.py": "",
    f"{project_name}/{project_name}/settings.py": f"""from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{app_name}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
    f"{project_name}/{project_name}/urls.py": f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{app_name}.urls')),
]
""",
    f"{project_name}/{project_name}/wsgi.py": f"""import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
application = get_wsgi_application()
""",
    f"{project_name}/{app_name}/__init__.py": "",
    f"{project_name}/{app_name}/models.py": """from django.db import models

class Quote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'"{self.text}" — {self.author}'
""",
    f"{project_name}/{app_name}/views.py": """import random
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
""",
    f"{project_name}/{app_name}/urls.py": """from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/', views.random_quote_api, name='random_quote_api'),
]
""",
    f"{project_name}/{app_name}/templates/quotes/home.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Zen Quotes</title>
  <style>
    body {
      font-family: 'Georgia', serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: linear-gradient(135deg, #e0f7fa, #e1bee7);
      margin: 0;
      text-align: center;
      padding: 2rem;
    }
    .quote-box {
      background: white;
      padding: 2rem;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .quote {
      font-size: 1.5rem;
      margin-bottom: 1rem;
    }
    .author {
      font-size: 1rem;
      color: #555;
    }
  </style>
</head>
<body>
  <div class="quote-box">
    <div class="quote">“{{ quote.text }}”</div>
    <div class="author">— {{ quote.author }}</div>
  </div>
</body>
</html>
""",
    f"{project_name}/{app_name}/management/commands/loadquotes.py": """import json
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
""",
    f"{project_name}/{app_name}/quotes.json": """[
  {
    "quote": "Peace comes from within. Do not seek it without.",
    "author": "Buddha",
    "tags": ["zen", "peace"]
  },
  {
    "quote": "The best way out is always through.",
    "author": "Robert Frost",
    "tags": ["motivation", "resilience"]
  }
]
""",
    f"{project_name}/requirements.txt": "Django>=4.0,<5.0\n",
    f"{project_name}/Procfile": "web: gunicorn zenquotes.wsgi\n"
}

# Create project files
for path, content in files_to_create.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# Create ZIP
zip_filename = f"{project_name}.zip"
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(project_name):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, arcname=os.path.relpath(file_path, start=project_name))

print(f"✅ Project zipped as {zip_filename}")
