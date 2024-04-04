from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def chatbot_index(request):
    return render(request, 'chatbot/index.html')

