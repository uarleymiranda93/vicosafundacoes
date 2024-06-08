from django.shortcuts import render
from pathlib import Path
import os
import datetime
import xlsxwriter
from django.db import connection
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
from django.db.models import F, Max, Case, When, Value, CharField
from .models import Fornecedor, FornecedorAvaliacao


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
        cat_aval_item = CategoriaAvaliacaoItem.objects.all()
        forn = Fornecedor()
        forn.forn_nome = request.POST['forn_nome']
        forn.forn_cnpj = request.POST['forn_cnpj']
        forn.forn_ies = request.POST['forn_ies']
        forn.forn_desc=request.POST['forn_desc']
        if 'nf' in request.POST:
            forn.forn_nf = request.POST.get('nf') == '1'
        forn.cat_imp = CategoriaImpacto(cat_imp_id = request.POST['cat_imp'])
        forn.cat_tip = CategoriaTipo(cat_tip_id = request.POST['cat_tip'])
        forn.save()

        forn_aval = FornecedorAvaliacao()
        forn_aval.forn = Fornecedor(forn_id=forn.forn_id)
        forn_aval.save()

        forn_monit = FornecedorMonitoramento()
        forn_monit.forn = Fornecedor(forn_id=forn.forn_id)
        forn_monit.save()

        for i in cat_aval_item:
            aval_item = FornecedorAvaliacaoItem()
            aval_item.cat_aval_item = CategoriaAvaliacaoItem(cat_aval_item_id=i.cat_aval_item_id)
            aval_item.forn_aval = FornecedorAvaliacao(forn_aval_id=forn_aval.forn_aval_id)
            aval_item.save()
        
       

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
            if 'nf' in request.POST:
                forn.forn_nf = request.POST.get('nf') == '1'
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
def aval_index(request):
    return render(request, 'fornecedor/forn_aval_list.html')

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


# def aval_add(request):
#     try:
#         forn = FornecedorAvaliacao()
        
#         # Convertendo a data para datetime.datetime
#         forn.forn_aval_dta = datetime.strptime(request.POST['forn_aval_dta'], '%Y-%m-%d')
        
#         # Definindo as chaves estrangeiras diretamente
#         forn.cat_aval_id = request.POST['cat_aval']
#         forn.pes_id = request.POST['pes']
#         forn.forn_id = request.POST['forn_id']
        
#         forn.forn_aval_evid = request.POST['forn_aval_evid']
        
#         forn.save()
#     except (Exception, DatabaseError) as error:
#         print(error)
#         return JsonResponse({
#             'error': str(error),
#             'aviso': 'Erro ao adicionar o Produto'
#         }, status=500)
#     else:
#         return JsonResponse({
#             'item': None,
#             'aviso': 'Adicionado com sucesso!'
#         }, status=200)


def aval_edt(request):
    try:
        forn=FornecedorAvaliacao.objects.get(pk=request.POST['forn_aval_id'])
        if request.method=="POST":
            forn.cat_aval_id = request.POST['cat_aval']
            forn.forn_aval_dta = datetime.strptime(request.POST['forn_aval_dta'], '%Y-%m-%d')
            forn.pes_id = request.POST['pes']
            forn.forn_id = Fornecedor(forn_id=forn.forn.forn_id)
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


# def aval_del(request):
#     try:
#         if request.method=="POST":
#             item=FornecedorAvaliacao.objects.get(pk=request.POST['forn_aval_id'])
#             item.delete()
#     except(Exception,DatabaseError) as error:
#         print(error)
#         return JsonResponse({
#             'error': str(error),
#             'aviso': 'Erro ao deletar o Produto, '},
#             status=500)
#     else:
#         return JsonResponse({
#             'item': None,
#             'aviso': 'Excluido com sucesso!'},
#             status=200) 
        

def aval_list(request):
    try:
        dados= FornecedorAvaliacaoSerializer(FornecedorAvaliacao.objects.all().order_by('forn_aval_id'), many=True)
        print(dados)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})
    

def aval_item_list(request):
    try:
        dados= FornecedorAvaliacaoItemSerializer(FornecedorAvaliacaoItem.objects.filter(forn_aval=request.POST['forn_aval_id']).order_by('forn_aval_id'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def item_edt_div(request):
    try:
        aval_item_ids = request.POST.getlist('aval_item_id')
        # Remove strings vazias da lista de IDs
        aval_item_ids = [id for id in aval_item_ids if id.isdigit()]
        print('ids chegando',aval_item_ids)

        if request.method == "POST":
            for aval_item_id in aval_item_ids:
                # Faça o que você precisa fazer para cada ID
                forn_item = FornecedorAvaliacaoItem.objects.get(pk=aval_item_id)
                if 'aval_item_grau' in request.POST:
                    forn_item.aval_item_grau = request.POST['aval_item_grau']
                if  'aval_item_nota' in request.POST:
                    forn_item.aval_item_nota = request.POST['aval_item_nota']
                forn_item.save()
                print('após salvar',forn_item)
            # Aqui você pode retornar uma resposta JSON de sucesso se necessário
            return JsonResponse({
                'aviso': 'Editado com sucesso!',
            }, status=200)

    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Produto'
        }, status=500)
    

def monit_index(request):
    return render(request, 'fornecedor/forn_monit_list.html')


def monit_list(request):
    try:
        dados= FornecedorMonitoramentoSerializer(FornecedorMonitoramento.objects.all().order_by('forn_monit_id'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})


def monit_atb(request):
    try:
        item = FornecedorMonitoramentoSerializer(FornecedorMonitoramento.objects.get(pk=request.GET['forn_monit_id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 


def monit_edt(request):
    try:
        monit=FornecedorMonitoramento.objects.get(pk=request.POST['forn_monit_id'])
        if request.method=="POST":
            if 'qualidade' in request.POST:
                monit.forn_monit_qld = request.POST.get('qualidade') == '1'
            if 'pontualidade' in request.POST:
                monit.forn_monit_pont = request.POST.get('pontualidade') == '3'
            if 'preco' in request.POST:
                monit.forn_monit_val = request.POST.get('preco') == '5'
            if 'suport' in request.POST:
                monit.forn_monit_sup = request.POST.get('suport') == '7'
            monit.forn_id = Fornecedor(forn_id=monit.forn.forn_id)
            monit.save()
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


def relatorio_aprov(request):
    # forn_ids = request.POST.getlist('forn_ids[]') 
    print('aquiiii')
    # forn_id = request.POST.get('forn_id')  # Recebe o forn_id enviado via AJAX
    print(request)
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #         SELECT 
    #             f.forn_nome,
    #             f.forn_desc,
    #             f.forn_nf,
    #             c.cat_tip_nome,
    #             c2.cat_imp_nome,
    #             f2.forn_ctt_nome,
    #             f2.forn_ctt_tel,
    #             f.forn_cnpj,
    #             f.forn_ies,
    #             MAX(CASE WHEN row_num = 1 THEN fa.forn_aval_dta ELSE NULL END) AS forn_aval_dta_inicial,
    #             MAX(CASE WHEN row_num = 1 THEN fa.forn_aval_evid ELSE '' END) AS forn_aval_evid_inicial,
    #             MAX(CASE WHEN row_num = 1 THEN cp.pes_nome ELSE '' END) AS pes_nome_inicial,
    #             MAX(CASE WHEN row_num = 2 THEN fa.forn_aval_dta ELSE NULL END) AS forn_aval_dta_reavaliacao,
    #             MAX(CASE WHEN row_num = 2 THEN fa.forn_aval_evid ELSE '' END) AS forn_aval_evid_reavaliacao,
    #             MAX(CASE WHEN row_num = 2 THEN cp.pes_nome ELSE '' END) AS pes_nome_reavaliacao,
    #             fm.forn_monit_qld,
    #             fm.forn_monit_pont,
    #             fm.forn_monit_val,
    #             fm.forn_monit_sup
    #         FROM 
    #             fornecedor f
    #         LEFT JOIN 
    #             (
    #                 SELECT 
    #                     *,
    #                     ROW_NUMBER() OVER(PARTITION BY forn_id ORDER BY forn_aval_dta) AS row_num
    #                 FROM 
    #                     fornecedoravaliacao
    #             ) fa ON f.forn_id = fa.forn_id
    #         LEFT JOIN 
    #             categoriatipo c ON f.cat_tip_id = c.cat_tip_id
    #         LEFT JOIN 
    #             categoriaimpacto c2 ON f.cat_imp_id = c2.cat_imp_id
    #         LEFT JOIN 
    #             fornecedorcontato f2 ON f.forn_id = f2.forn_id
    #         LEFT JOIN 
    #             fornecedormonitoramento fm ON f.forn_id = fm.forn_id
    #         LEFT JOIN 
    #             public.categoriapessoa cp ON cp.pes_id = fa.pes_id
    #         WHERE 
    #             f.forn_id = %s
    #         GROUP BY 
    #             f.forn_nome,
    #             f.forn_desc,
    #             f.forn_nf,
    #             c.cat_tip_nome,
    #             c2.cat_imp_nome,
    #             f2.forn_ctt_nome,
    #             f2.forn_ctt_tel,
    #             f.forn_cnpj,
    #             f.forn_ies,
    #             fm.forn_monit_qld,
    #             fm.forn_monit_pont,
    #             fm.forn_monit_val,
    #             fm.forn_monit_sup
    #     """,[forn_id])
    #     resultados = cursor.fetchall()
    #  # Caminho para salvar o arquivo Excel
    # diretorio_downloads = Path.home() / 'Downloads'

    # num_arquivo = 1
    # while os.path.exists(f'excel_{num_arquivo}.xlsx'):
    #     num_arquivo += 1

    # # Construir o nome do arquivo com o número sequencial
    # nome_arquivo = f'excel_{num_arquivo}.xlsx'
    # caminho_arquivo = diretorio_downloads / nome_arquivo

    # # Criar o arquivo Excel
    # workbook = xlsxwriter.Workbook(caminho_arquivo)
    # worksheet = workbook.add_worksheet()

    # # Definir a largura das colunas
    # larguras = [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]  # Largura de cada coluna
    # for col, largura in enumerate(larguras):
    #     worksheet.set_column(col, col, largura)

    # aprovacao_formato = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'justify', 'bg_color': '#C0C0C0'})
    # worksheet.merge_range('A1:S1', 'Aprovação Fornecedor', aprovacao_formato)

    # worksheet.set_row(0, 40) 
    # # Adicionar duas linhas vazias abaixo do texto "Aprovação Fornecedor"
    # worksheet.set_row(1, 30)  # Definir a altura da linha como 30 para criar duas linhas vazias

    # # Escrever o cabeçalho na linha seguinte
    # cabecalho_formato = workbook.add_format({'bold': True, 'font_size': 14, 'bg_color': '#C0C0C0'})
    # headers = [
    #     'Fornecedor', 'Descrição', 'Emissão NF', 'Tipo', 'Impacto',
    #     'Contato', 'Telefone', 'CNPJ', 'Inscrição Municipal/Estadual',
    #     'Data Aprovação', 'Evidência', 'Responsável',
    #     'Data Reavaliação', 'Evidência Reavaliação', 'Responsável Reavaliação',
    #     'Qualidade dos produtos', 'Pontualidade na entrega', 'preço', 'Suporte Pós Venda'
    # ]
    # for col, header in enumerate(headers):
    #     worksheet.write(2, col, header, cabecalho_formato)

    # # Escrever os dados nas células
    # for row, resultado in enumerate(resultados, start=3):  # Começando na linha 4 (índice 3)
    #     for col, valor in enumerate(resultado):
    #         worksheet.write(row, col, valor)

    # # Fechar o arquivo Excel
    # workbook.close()

    # # Retornar uma resposta para o usuário com o link para download do arquivo Excel
    # with open(caminho_arquivo, 'rb') as file:
    #     response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
    #     response['Content-Disposition'] = 'attachment; filename="excel.xlsx"'

    # return response