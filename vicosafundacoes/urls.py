from django.urls import path
from .views import * 

app_name = 'vicosafundacoes' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', forn_index, name='forn_index'),
    
]