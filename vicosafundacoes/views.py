from django.shortcuts import render

# Create your views here.

def forn_index(request):
    return render(request, 'vicosafundacoes/forn_list.html')


