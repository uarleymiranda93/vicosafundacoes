from django.urls import path
from .views import * 

app_name = 'vicosafundacoes' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', forn_index, name='forn_index'),
    path('forn_list/', forn_list, name='forn_list'),
    path('forn_atb/', forn_atb, name='forn_atb'),
    path('forn_add/', forn_add, name='forn_add'),
    path('forn_edt/', forn_edt, name='forn_edt'),
    path('forn_del/', forn_del, name='forn_del'),
]