from django.urls import path
from . views import *

app_name = 'categorias'

urlpatterns = [
    
    
    
    path('', cat_imp_index, name='cat_imp_index'),
    path('cat_imp_lista/', cat_imp_lista, name='cat_imp_lista'),
    path('cat_imp_atb/', cat_imp_atb, name='cat_imp_atb'),
    path('cat_imp_add/', cat_imp_add, name='cat_imp_add'),
    path('cat_imp_edt/', cat_imp_edt, name='cat_imp_edt'),
    path('cat_imp_del/', cat_imp_del, name='cat_imp_del'),
    
    path('cat_pes_index', cat_pes_index, name='cat_pes_index'),
    path('cat_pes_lista/', cat_pes_lista, name='cat_pes_lista'),
    path('cat_pes_atb/', cat_pes_atb, name='cat_pes_atb'),
    path('cat_pes_add/', cat_pes_add, name='cat_pes_add'),
    path('cat_pes_edt/', cat_pes_edt, name='cat_pes_edt'),
    path('cat_pes_del/', cat_pes_del, name='cat_pes_del'),
    
    path('cat_sta_index', cat_sta_index, name='cat_sta_index'),
    path('cat_sta_lista/', cat_sta_lista, name='cat_sta_lista'),
    path('cat_sta_atb/', cat_sta_atb, name='cat_sta_atb'),
    path('cat_sta_add/', cat_sta_add, name='cat_sta_add'),
    path('cat_sta_edt/', cat_sta_edt, name='cat_sta_edt'),
    path('cat_sta_del/', cat_sta_del, name='cat_sta_del'),

    path('cat_tip_index', cat_tip_index, name='cat_tip_index'),
    path('cat_tip_lista/', cat_tip_lista, name='cat_tip_lista'),
    path('cat_tip_atb/', cat_tip_atb, name='cat_tip_atb'),
    path('cat_tip_add/', cat_tip_add, name='cat_tip_add'),
    path('cat_tip_edt/', cat_tip_edt, name='cat_tip_edt'),
    path('cat_tip_del/', cat_tip_del, name='cat_tip_del'),

    path('cat_prod_index', cat_prod_index, name='cat_prod_index'),
    path('cat_prod_lista/', cat_prod_lista, name='cat_prod_lista'),
    path('cat_prod_atb/', cat_prod_atb, name='cat_prod_atb'),
    path('cat_prod_add/', cat_prod_add, name='cat_prod_add'),
    path('cat_prod_edt/', cat_prod_edt, name='cat_prod_edt'),
    path('cat_prod_del/', cat_prod_del, name='cat_prod_del'),


                        #Url Select2
    path('pesq_impacto/',pesq_impacto, name='pesq_impacto'),
    path('pesq_status/',pesq_status, name='pesq_status'),
    path('pesq_produto/',pesq_produto, name='pesq_produto'),
    path('pesq_tipo/',pesq_tipo, name='pesq_tipo'),

]