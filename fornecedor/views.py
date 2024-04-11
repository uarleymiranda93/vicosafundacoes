from django.shortcuts import render
from sqlite3 import DatabaseError
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import *
from categorias.models import *
from fornecedor.serializador import *
from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import JsonResponse
from django.db import DatabaseError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

def forn_index(request):
    return render(request, 'fornecedor/forn_list.html')


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
        forn.forn_desc=request.POST['forn_desc']
        forn.cat_imp = CategoriaImpacto(cat_imp_id = request.POST['cat_imp'])
        forn.cat_tip = CategoriaTipo(cat_tip_id = request.POST['cat_tip'])
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
        forn=Fornecedor.objects.get(pk=request.POST['forn_id'])
        if request.method=="POST":
            forn.forn_id=request.POST['forn_id']
            forn.forn_nome=request.POST['forn_nome']
            forn.forn_cnpj=request.POST['forn_cnpj']
            forn.forn_ies=request.POST['forn_ies']
            forn.forn_desc=request.POST['forn_desc']
            forn.cat_imp = CategoriaImpacto(cat_imp_id = request.POST['cat_imp'])
            forn.cat_tip = CategoriaTipo(cat_tip_id = request.POST['cat_tip'])
            forn.save()
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
        dados= FornecedorContatoSerializer(FornecedorContato.objects.filter(forn=request.POST['forn_id']).order_by('forn_ctt_nome'), many=True)
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
            else:
                item.forn_ctt_ativo=False
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
        

##############################################################################################
#                               Fornecedor avaliaçao                                           #
##############################################################################################
def aval_list(request):
    try:
        dados= FornecedorAvaliacaoSerializer(FornecedorAvaliacao.objects.filter(forn=request.POST['forn_id']).order_by('forn_aval_id'), many=True)
        print(dados)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def aval_atb(request):
    try:
        item = FornecedorAvaliacaoSerializer(FornecedorAvaliacao.objects.get(pk=request.GET['forn_aval_id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 


def aval_add(request):
    try:
        forn = FornecedorAvaliacao()
        
        # Convertendo a data para datetime.datetime
        forn.forn_aval_dta = datetime.strptime(request.POST['forn_aval_dta'], '%Y-%m-%d')
        
        # Definindo as chaves estrangeiras diretamente
        forn.cat_aval_id = request.POST['cat_aval']
        forn.pes_id = request.POST['pes']
        forn.forn_id = request.POST['forn_id']
        
        forn.forn_aval_evid = request.POST['forn_aval_evid']
        
        forn.save()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Produto'
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'
        }, status=200)


def aval_edt(request):
    try:
        forn=FornecedorAvaliacao.objects.get(pk=request.POST['forn_aval_id'])
        if request.method=="POST":
            forn.cat_aval_id = request.POST['cat_aval']
            forn.forn_aval_dta = datetime.strptime(request.POST['forn_aval_dta'], '%Y-%m-%d')
            forn.pes_id = request.POST['pes']
            forn.forn_id = request.POST['forn_id']
            forn.forn_aval_evid = request.POST['forn_aval_evid']
            forn.save()
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


def aval_del(request):
    try:
        if request.method=="POST":
            item=FornecedorAvaliacao.objects.get(pk=request.POST['forn_aval_id'])
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
        
