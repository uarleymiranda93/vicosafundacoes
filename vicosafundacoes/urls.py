from django.urls import path
from .views import * 

app_name = 'vicosafundacoes' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', index, name='index'),
    path('entrar/', entrar, name='entrar'),
    path('sair/', sair, name='sair'),
    
    path('',homepage, name=""),

    path('register/',register, name="register"),

    path('my-login/', my_login, name="my-login"),

    path('dashboard/',dashboard, name="dashboard"),
    
    path('user-logout/', user_logout, name="user-logout"),
    
    path('user_dados/',user_dados, name="user_dados"),
    path('pes_lista/', pes_lista, name='pes_lista'),
    path('pes_atb/', pes_atb, name='pes_atb'),
    path('pes_add/', pes_add, name='pes_add'),
    path('pes_edt/', pes_edt, name='pes_edt'),
    path('pes_del/', pes_del, name='pes_del'),
    


]