from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quote/', views.random_quote_api, name='random_quote_api'),
]
