from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('registro/', views.registro_view, name='registro'),
    path('seleccion-intereses/', views.seleccion_intereses_view, name='seleccion_intereses'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
]