from django.urls import path
from .views import * 

app_name = 'obras' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [

    
    path('', obr_index, name='obr_index'),
    path('obr_lista/', obr_lista, name='obr_lista'),
    path('obr_atb/', obr_atb, name='obr_atb'),
    path('obr_add/', obr_add, name='obr_add'),
    path('obr_edt/', obr_edt, name='obr_edt'),
    path('obr_del/', obr_del, name='obr_del'),
    

    path('ped_lista/', ped_lista, name='ped_lista'),
    path('ped_atb/', ped_atb, name='ped_atb'),
    path('ped_add/', ped_add, name='ped_add'),
    path('ped_edt/', ped_edt, name='ped_edt'),
    path('ped_del/', ped_del, name='ped_del'),
    
    path('ped_prod_lista/', ped_prod_lista, name='ped_prod_lista'),
    path('ped_prod_atb/', ped_prod_atb, name='ped_prod_atb'),
    path('ped_prod_add/', ped_prod_add, name='ped_prod_add'),
    path('ped_prod_add_2/', ped_prod_add_2, name='ped_prod_add_2'),
    path('ped_prod_edt/', ped_prod_edt, name='ped_prod_edt'),
    path('ped_prod_del/', ped_prod_del, name='ped_prod_del'),

    
    path('ped_esp_lista/', ped_esp_lista, name='ped_esp_lista'),
    path('ped_esp_atb/', ped_esp_atb, name='ped_esp_atb'),
    path('ped_esp_add/', ped_esp_add, name='ped_esp_add'),
    path('ped_esp_edt/', ped_esp_edt, name='ped_esp_edt'),
    path('ped_esp_del/', ped_esp_del, name='ped_esp_del'),
    
    path('ped_ent_lista/', ped_ent_lista, name='ped_ent_lista'),
    path('ped_ent_atb/', ped_ent_atb, name='ped_ent_atb'),
    path('ped_ent_add/', ped_ent_add, name='ped_ent_add'),
    path('ped_ent_edt/', ped_ent_edt, name='ped_ent_edt'),
    path('ped_ent_del/', ped_ent_del, name='ped_ent_del'),
    
    path('ped_ver_lista/', ped_ver_lista, name='ped_ver_lista'),
    path('ped_ver_atb/', ped_ver_atb, name='ped_ver_atb'),
    path('ped_ver_add/', ped_ver_add, name='ped_ver_add'),
    path('ped_ver_edt/', ped_ver_edt, name='ped_ver_edt'),
    path('ped_ver_del/', ped_ver_del, name='ped_ver_del'),



]