
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from .models import *
from vicosafundacoes.serializador import *
from django.db import DatabaseError
from .forms import *
from django.shortcuts import render, redirect,get_object_or_404
from . forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout



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
        
            item = Pessoa()
            item.pes_nome = request.user
            item.pes_nome_adm = request.user
            item.pes_adm_id = request.user.id
            item.save()
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

@login_required(login_url="base:my-login")
def pes_lista(request):
    try:
        # Obtendo o ID do usuário logado
        user_id = request.user.id
        
        # Obtendo o usuário logado
        user = get_object_or_404(User, pk=user_id)
        
        # Filtrando as informações da tabela Pessoa usando o ID do usuário logado
        dados = PessoaSerializer(Pessoa.objects.filter(pes_adm_id=user.id).order_by('pes_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
@login_required(login_url="vicosafundacoes:my-login") 
def pes_atb(request):
    try:
        item = PessoaSerializer(Pessoa.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 


@login_required(login_url="vicosafundacoes:my-login")
def pes_add(request):
    try:
        # Verifica se já existe uma Pessoa com os mesmos dados
        existing_person = Pessoa.objects.filter(
            pes_adm_id = request.user.id
        ).first()
        
        if existing_person:
            return JsonResponse({
                'aviso': 'Já existe uma pessoa com esses dados'},
                status=400)

        # Se não existir, cria um novo registro
        item = Pessoa()
        item.pes_nome = request.POST['pes_nome']
        item.pes_email = request.POST['pes_email']
        item.pes_doc = request.POST['pes_doc']
        item.pes_ctt = request.POST['pes_ctt']
        item.pes_nome_adm = request.user
        item.pes_adm_id = request.user.id
        
        item.save()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a pessoa'},
            status=500)
    else:
        return JsonResponse({
            'aviso': 'Adicionado com sucesso!'},
            status=200)

        
@login_required(login_url="vicosafundacoes:my-login")
def pes_edt(request):
    try:
        item = Pessoa.objects.get(pk=request.POST['pes_id'])
        if request.method=="POST":
            item.pes_nome=request.POST['pes_nome']
            item.pes_email=request.POST['pes_email']
            item.pes_doc=request.POST['pes_doc']
            item.pes_ctt=request.POST['pes_ctt']
            item.pes_nome_adm=request.POST['pes_nome_adm']
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar a produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
        
@login_required(login_url="vicosafundacoes:my-login")
def pes_del(request):
    try:
        if request.method == "POST":
            item = Pessoa.objects.get(pk=request.POST['pes_id'])
            item.delete()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar a Produto'
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)