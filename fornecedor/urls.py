from django.urls import path
from .views import * 

app_name = 'fornecedor' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    #fornecedor 
    path('', forn_index, name='forn_index'),
    path('forn_list/', forn_list, name='forn_list'),
    path('forn_atb/', forn_atb, name='forn_atb'),
    path('forn_add/', forn_add, name='forn_add'),
    path('forn_edt/', forn_edt, name='forn_edt'),
    path('forn_del/', forn_del, name='forn_del'),

    #fornecedor contato
    path('ctt_list/', ctt_list, name='ctt_list'),
    path('ctt_atb/', ctt_atb, name='ctt_atb'),
    path('ctt_add/', ctt_add, name='ctt_add'),
    path('ctt_edt/', ctt_edt, name='ctt_edt'),
    path('ctt_del/', ctt_del, name='ctt_del'),

    #fornecedor avaliação
    path('avaliacao/', aval_index, name='aval_index'),
    path('aval_list/', aval_list, name='aval_list'),
    path('aval_atb/', aval_atb, name='aval_atb'),
    path('aval_edt/', aval_edt, name='aval_edt'),
    
    #fornecedor avaliação item 
    path('aval_item_list/', aval_item_list, name='aval_item_list'),
    path('item_edt_div/', item_edt_div, name='item_edt_div'),
    # path('aval_atb/', aval_atb, name='aval_atb'),
    # path('aval_add/', aval_add, name='aval_add'),
    # path('aval_edt/', aval_edt, name='aval_edt'),
    # path('aval_del/', aval_del, name='aval_del'),

]