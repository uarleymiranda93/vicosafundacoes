from sqlite3 import DatabaseError
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import *
from categorias.models import *
from vicosafundacoes.serializador import *
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@login_required(login_url="vicosafundacoes:my-login")
def index(request):
    return render(request, 'vicosafundacoes/base.html')

@login_required(login_url="vicosafundacoes:my-login")
def entrar(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session.set_expiry(60)
            login(request, user)
            return HttpResponseRedirect(reverse('vicosafundacoes:index'))
        else:
            return render(request, 'vicosafundacoes/login.html')
        
    else:
        return render(request, 'vicosafundacoes/login.html')   
        
@login_required(login_url="vicosafundacoes:my-login")       
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse(':entrar'))        
################################################################################################################################

@login_required(login_url="vicosafundacoes:my-login")
def homepage(request):

    return render(request, 'vicosafundacoes/base.html')


def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("vicosafundacoes:my-login")


    context = {'registerform':form}

    return render(request, 'vicosafundacoes/register.html', context=context)



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("vicosafundacoes:index")
            

    context = {'loginform':form,'user': request.user}

    return render(request, 'vicosafundacoes/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("vicosafundacoes:my-login")




def dashboard(request):

    return render(request, 'vicosafundacoes/dashboard.html')

########################################## Alteração dados de usuario ################################################
@login_required(login_url="vicosafundacoes:my-login")
def user_dados(request):

    return render(request, 'vicosafundacoes/user_dados.html')


