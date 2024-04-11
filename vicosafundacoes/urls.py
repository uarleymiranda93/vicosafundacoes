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

]