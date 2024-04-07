from sqlite3 import DatabaseError
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import *
from vicosafundacoes.serializador import *

# Create your views here.

def forn_index(request):
    return render(request, 'vicosafundacoes/forn_list.html')


def forn_list(request):
    try:
        dados= FornecedorSerializer(Fornecedor.objects.all().order_by('forn_nome'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def forn_atb(request):
    try:
        item = FornecedorSerializer(Fornecedor.objects.get(pk=request.GET['forn_id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
 
def forn_add(request):
    try:
        forn = Fornecedor()
        forn.forn_nome = request.POST['forn_nome']
        forn.forn_cnpj = request.POST['forn_cnpj']
        forn.forn_ies = request.POST['forn_ies']
        forn.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)


def forn_edt(request):
    try:
        item=Fornecedor.objects.get(pk=request.POST['forn_id'])
        if request.method=="POST":
            item.forn_id=request.POST['forn_id']
            item.forn_nome=request.POST['forn_nome']
            item.forn_cnpj=request.POST['forn_cnpj']
            item.forn_ies=request.POST['forn_ies']
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)


def forn_del(request):
    try:
        if request.method=="POST":
            item=Fornecedor.objects.get(pk=request.POST['forn_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Produto, '},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'},
            status=200) 

##############################################################################################
#                               Fornecedor contato                                           #
##############################################################################################
def ctt_list(request):
    try:
        dados= FornecedorContatoSerializer(FornecedorContato.objects.all().order_by('forn_ctt_nome'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def ctt_atb(request):
    try:
        item = FornecedorContatoSerializer(FornecedorContato.objects.get(pk=request.GET['forn_ctt_id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
 
def ctt_add(request):
    try:
        print(request.POST['forn_id'])
        forn = FornecedorContato()
        forn.forn_ctt_nome = request.POST['forn_ctt_nome']
        forn.forn_ctt_tel = request.POST['forn_ctt_tel']
        forn.forn_ctt_email = request.POST['forn_ctt_email']
        forn.forn = Fornecedor(forn_id=request.POST['forn_id'])
        if 'forn_ctt_ativo' in request.POST:
            forn.forn_ctt_ativo = True
        forn.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)


def ctt_edt(request):
    try:
        item=FornecedorContato.objects.get(pk=request.POST['forn_ctt_id'])
        if request.method=="POST":
            item.forn_ctt_id=request.POST['forn_ctt_id']
            item.forn_ctt_tel=request.POST['forn_ctt_tel']
            item.forn_ctt_email=request.POST['forn_ctt_email']
            if 'forn_ctt_ativo' in request.POST:
                item.forn_ctt_ativo=True
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)


def ctt_del(request):
    try:
        if request.method=="POST":
            item=FornecedorContato.objects.get(pk=request.POST['forn_ctt_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Produto, '},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'},
            status=200) 
        
