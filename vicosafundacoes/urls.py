from django.urls import path
from .views import * 

app_name = 'vicosafundacoes' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [

    #fornecedor 
    path('', forn_index, name='forn_index'),
    path('forn_list/', forn_list, name='forn_list'),
    path('forn_atb/', forn_atb, name='forn_atb'),
    path('forn_add/', forn_add, name='forn_add'),
    path('forn_edt/', forn_edt, name='forn_edt'),
    path('forn_del/', forn_del, name='forn_del'),

    #fornecedor contanto
    path('ctt_list/', ctt_list, name='ctt_list'),
    path('ctt_atb/', ctt_atb, name='ctt_atb'),
    path('ctt_add/', ctt_add, name='ctt_add'),
    path('ctt_edt/', ctt_edt, name='ctt_edt'),
    path('ctt_del/', ctt_del, name='ctt_del'),
]