from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout-alt/', views.simple_logout, name='logout_alt'),  # Logout alternativo
    path('meus-animais/', views.meus_animais, name='meus_animais'),
    path('cadastrar-animal/', views.cadastrar_animal, name='cadastrar_animal'),
    path('animal/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('perdidos/', views.animais_perdidos, name='animais_perdidos'),
    path('reportar-perdido/<int:animal_id>/', views.reportar_perdido, name='reportar_perdido'),
    path('perdidos/<int:pk>/', views.animal_perdido_detail, name='animal_perdido_detail'),
    path('avistamento/<int:perdido_id>/', views.reportar_avistamento, name='reportar_avistamento'),
]
