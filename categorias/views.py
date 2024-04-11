from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from categorias.serializador import *
from django.db import DatabaseError
from django.shortcuts import render
from .forms import *


def cat_pes_index(request):
    return render(request, 'categoria pessoa/pes_index.html')

def cat_pes_lista(request):
    try:
        dados= CategoriaPessoaSerializer(CategoriaPessoa.objects.all().order_by('pes_nome'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})

def cat_pes_atb(request):
    try:
        item = CategoriaPessoaSerializer(CategoriaPessoa.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    

def cat_pes_add(request):
    try:
        item=CategoriaPessoa()
        item.pes_nome=request.POST['pes_nome']
        item.pes_email=request.POST['pes_email']
        item.pes_ativo = request.POST.get('pes_ativo') == 'on'
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a pessoa'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)


def cat_pes_edt(request):
    try:
        item=CategoriaPessoa.objects.get(pk=request.POST['pes_id'])
        if request.method=="POST":
            item.pes_id=request.POST['pes_id']
            item.pes_nome=request.POST['pes_nome']
            item.pes_nome=request.POST['pes_nome']
            item.pes_ativo = request.POST.get('pes_ativo') == 'on'
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar a pessoa'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
        
def cat_pes_del(request):
    try:
        if request.method=="POST":
            item=CategoriaPessoa.objects.get(pk=request.POST['pes_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar a Pessoa'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)
        


###############################################categoria Impacto######################################################################################################################
def cat_imp_index(request):
    return render(request, 'categoria impacto/index.html')

def cat_imp_lista(request):
    try:
        dados = CategoriaImpactoSerializer(CategoriaImpacto.objects.all().order_by('cat_imp_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
    
def cat_imp_atb(request):
    try:
        item = CategoriaImpactoSerializer(CategoriaImpacto.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 

def cat_imp_add(request):
    if request.method == 'POST':
        form = CategoriaImpactoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'item': None,
                'aviso': 'Adicionado com sucesso!'
            }, status=200)
    else:
        form = CategoriaImpactoForm()
    return render(request, 'template.html', {'form': form})

def cat_imp_edt(request):
    try:
        item = CategoriaImpacto.objects.get(pk=request.POST['cat_imp_id'])
        if request.method=="POST":
            item.cat_imp_id=request.POST['cat_imp_id']
            item.cat_imp_nome=request.POST['cat_imp_nome']
            item.cat_imp_ativo = request.POST.get('cat_imp_ativo') == 'on'
            item.cat_imp_cor=request.POST['cat_imp_cor']
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Impacto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
    
def cat_imp_del(request):
    try:
        if request.method == "POST":
            item = CategoriaImpacto.objects.get(pk=request.POST['cat_imp_id'])
            item.delete()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Impacto '
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)
        
        
        
################################################################## Categoria Status ################################################################################################

def cat_sta_index(request):
    return render(request, 'categoria status/cat_sta_index.html')

def cat_sta_lista(request):
    try:
        dados = CategoriaStatusSerializer(CategoriaStatus.objects.all().order_by('cat_sta_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
    
def cat_sta_atb(request):
    try:
        item = CategoriaStatusSerializer(CategoriaStatus.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 

def cat_sta_add(request):
    try:
        item=CategoriaStatus()
        item.cat_sta_nome=request.POST['cat_sta_nome']
        item.cat_sta_cor=request.POST['cat_sta_cor']
        item.cat_sta_ativo = request.POST.get('cat_sta_ativo') == 'on'
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Status'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

def cat_sta_edt(request):
    try:
        item = CategoriaStatus.objects.get(pk=request.POST['cat_sta_id'])
        if request.method=="POST":
            item.cat_sta_id=request.POST['cat_sta_id']
            item.cat_sta_nome=request.POST['cat_sta_nome']
            item.cat_sta_ativo = request.POST.get('cat_sta_ativo') == 'on'
            item.cat_sta_cor=request.POST['cat_sta_cor']
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Status'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
    
def cat_sta_del(request):
    try:
        if request.method == "POST":
            item = CategoriaStatus.objects.get(pk=request.POST['cat_sta_id'])
            item.delete()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Status'
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)

################################################################## Categoria Tipo #######################################################################       

def cat_tip_index(request):
    return render(request, 'categoria tipo/cat_tip_index.html')

def cat_tip_lista(request):
    try:
        dados = CategoriaTipoSerializer(CategoriaTipo.objects.all().order_by('cat_tip_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
    
def cat_tip_atb(request):
    try:
        item = CategoriaTipoSerializer(CategoriaTipo.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 

def cat_tip_add(request):
    try:
        item = CategoriaTipo()
        item.cat_tip_nome=request.POST['cat_tip_nome']
        item.cat_tip_cor=request.POST['cat_tip_cor']
        item.cat_tip_ativo = request.POST.get('cat_tip_ativo') == 'on'
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Tipo'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

def cat_tip_edt(request):
    try:
        item = CategoriaTipo.objects.get(pk=request.POST['cat_tip_id'])
        if request.method=="POST":
            item.cat_tip_id=request.POST['cat_tip_id']
            item.cat_tip_nome=request.POST['cat_tip_nome']
            item.cat_tip_ativo = request.POST.get('cat_ttip_ativo') == 'on'
            item.cat_tip_cor=request.POST['cat_tip_cor']
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Tipo'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
    
def cat_tip_del(request):
    try:
        if request.method == "POST":
            item = CategoriaTipo.objects.get(pk=request.POST['cat_tip_id'])
            item.delete()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar o Tipo'
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)
        
##################################################################### categoria Porduto ########################################################################### ########## 
        
def cat_prod_index(request):
    return render(request, 'categoria produto/cat_prod_index.html')

def cat_prod_lista(request):
    try:
        dados = CategoriaProdutoSerializer(CategoriaProduto.objects.all().order_by('cat_prod_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
    
def cat_prod_atb(request):
    try:
        item = CategoriaProdutoSerializer(CategoriaProduto.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 

def cat_prod_add(request):
    try:
        item=CategoriaProduto()
        item.cat_prod_nome=request.POST['cat_prod_nome']
        item.cat_prod_cor=request.POST['cat_prod_cor']
        item.cat_prod_ativo = request.POST.get('cat_prod_ativo') == 'on'
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

def cat_prod_edt(request):
    try:
        item = CategoriaProduto.objects.get(pk=request.POST['cat_prod_id'])
        if request.method=="POST":
            item.cat_prod_id=request.POST['cat_prod_id']
            item.cat_prod_nome=request.POST['cat_prod_nome']
            item.cat_prod_ativo = request.POST.get('cat_prod_ativo') == 'on'
            item.cat_prod_cor=request.POST['cat_prod_cor']
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
    
def cat_prod_del(request):
    try:
        if request.method == "POST":
            item = CategoriaProduto.objects.get(pk=request.POST['cat_prod_id'])
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


####################################################################### pesq controls #############################################################################
def pesq_impacto(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaImpactoSerializer(CategoriaImpacto.objects.filter(nome__icontains=request.GET['term']).order_by('cat_imp_nome'), many=True)
        else:
            dados = CategoriaImpactoSerializer(CategoriaImpacto.objects.all().order_by('cat_imp_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)
    
    
def pesq_status(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaStatusSerializer(CategoriaStatus.objects.filter(nome__icontains=request.GET['term']).order_by('cat_sta_nome'), many=True)
        else:
            dados = CategoriaStatusSerializer(CategoriaStatus.objects.all().order_by('cat_sta_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)
    
def pesq_tipo(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaTipoSerializer(CategoriaTipo.objects.filter(nome__icontains=request.GET['term']).order_by('cat_tip_nome'), many=True)
        else:
            dados = CategoriaTipoSerializer(CategoriaTipo.objects.all().order_by('cat_tip_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)
    

def pesq_produto(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaProdutoSerializer(CategoriaProduto.objects.filter(nome__icontains=request.GET['term']).order_by('cat_prod_nome'), many=True)
        else:
            dados = CategoriaProdutoSerializer(CategoriaProduto.objects.all().order_by('cat_prod_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({''
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)
    

def pesq_cat_aval(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaAvaliacaoSerializer(CategoriaAvaliacao.objects.filter(nome__icontains=request.GET['term']).order_by('cat_aval_nome'), many=True)
        else:
            dados = CategoriaAvaliacaoSerializer(CategoriaAvaliacao.objects.all().order_by('cat_aval_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)


def pesq_pessoa(request):
    try:
        if 'term' in request.GET:
            dados = CategoriaPessoaSerializer(CategoriaPessoa.objects.filter(nome__icontains=request.GET['term']).order_by('pes_nome'), many=True)
        else:
            dados = CategoriaPessoaSerializer(CategoriaPessoa.objects.all().order_by('pes_nome'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(dados.data, safe=False)
    