from django.urls import path
from .views import * 

app_name = 'chatbot' #comando responsável por  deixar a app mais inteligente 

urlpatterns = [
    path('', chatbot_index, name='chatbot_index'),
    
]