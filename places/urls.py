from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('', views.landing_view, name='landing'),
]