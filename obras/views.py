from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from obras.serializador import *
from django.db import DatabaseError,transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.db.models import Max
from vicosafundacoes.utils import user_session

# Create your views here.
@login_required(login_url="vicosafundacoes:my-login")        
def obr_index(request):
    return render(request, 'obras/obr_lista.html')

@login_required(login_url="vicosafundacoes:my-login")
def obr_lista(request):
    try:
        dados = ObraSerializer(Obra.objects.all().order_by('obr_prop'), many=True)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    else:
        return JsonResponse({'dados': dados.data})
    
@login_required(login_url="vicosafundacoes:my-login")   
def obr_atb(request):
    try:
        item = ObraSerializer(Obra.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data)

@login_required(login_url="vicosafundacoes:my-login")
def obr_add(request):
    try:
        item = Obra()
        item.obr_prop = request.POST['obr_prop']
        item.obr_loc = request.POST['obr_loc']
        item.obr_dta_ini = datetime.strptime(request.POST['obr_dta_ini'], '%Y-%m-%d')
        item.cat_sta = CategoriaStatus.objects.get(cat_sta_id=3)
        item.cat_obr = CategoriaObra.objects.get(cat_obr_id=request.POST['cat_obr'])
        item.usu_cad = Pessoa(pes_id = user_session(request))
        item.save()
    except(Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Obra'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

        
@login_required(login_url="vicosafundacoes:my-login")
def obr_edt(request):
    try:
        item = Obra.objects.get(pk=request.POST['obr_id'])
        if request.method=="POST":
            item.obr_prop=request.POST['obr_prop']
            item.obr_loc=request.POST['obr_loc']
            item.cat_sta = CategoriaStatus(cat_sta_id = request.POST['cat_sta'])
            item.cat_obr = CategoriaObra(cat_obr_id = request.POST['cat_obr'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar a Obra'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)
        
@login_required(login_url="vicosafundacoes:my-login")   
def obr_del(request):
    try:
        if request.method == "POST":
            item = Obra.objects.get(pk=request.POST['obr_id'])
            item.delete()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar a Obra'
        }, status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'
        }, status=200)

##################################################################Pedido ######################################################################################################


@login_required(login_url="vicosafundacoes:my-login")
def ped_lista(request):
    try:
        dados= PedidoSerializer(Pedido.objects.filter(obr=request.POST['obr_id']).order_by('ped_num'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})
    
@login_required(login_url="vicosafundacoes:my-login")   
def ped_atb(request):
    try:
        item = PedidoSerializer(Pedido.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data)

@login_required(login_url="vicosafundacoes:my-login")
def ped_add(request):
    try:
        with transaction.atomic():
            # Obtém o ano atual
            current_year = datetime.now().year
            
            # Obtém o último número utilizado
            ultimo_pedido = Pedido.objects.order_by('-ped_num').first()
            ultimo_numero = ultimo_pedido.ped_num if ultimo_pedido else 0
            
            if isinstance(ultimo_numero, str):
                ultimo_numero = int(ultimo_numero)
            
            # Incrementa o número
            novo_numero = (current_year * 1000) + (ultimo_numero % 1000) + 1
            
            # Cria um novo Pedido
            item = Pedido()
            item.ped_num = novo_numero
            item.ult_num = item.ped_num
            item.ped_dta = datetime.strptime(request.POST['ped_dta'], '%Y-%m-%d')
            item.obr = Obra.objects.get(obr_id=request.POST['obr_id'])
            item.cat_pes = CategoriaPessoa.objects.get(pes_id=request.POST['cat_pes'])
            item.forn = Fornecedor.objects.get(forn_id=request.POST['forn'])
            item.usu_cad = Pessoa(pes_id = user_session(request))
            
            item.save()

            # Agora que o Pedido foi salvo, podemos acessar o ped_id
            ped_id = item.ped_id

            # Caminho para salvar os arquivos do pedido
            xpath = os.path.join('media/pedido/', str(ped_id))
            # Cria o diretório se não existir
            os.makedirs(xpath, exist_ok=True)

            # Armazena os arquivos no sistema de arquivos, se estiverem presentes no request
            arquivos = request.FILES.getlist('arquivos')
            filepaths = []
            for arquivo in arquivos:
                xstorage = FileSystemStorage(location=xpath)
                filename = xstorage.save(arquivo.name, arquivo)
                filepath = os.path.join(xpath, filename)
                filepaths.append(filepath)

            # Atualiza o caminho do arquivo do Pedido com o primeiro caminho, se houver arquivos
            if filepaths:
                item.ped_arq_path ='/'+ filepaths[0]
                item.save()

        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'
        }, status=200)
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar o Pedido'
        }, status=500)
        
@login_required(login_url="vicosafundacoes:my-login")
def ped_edt(request):
    try:
        item = Pedido.objects.get(pk=request.POST['ped_id'])
        if request.method=="POST":
            item.ped_dta = datetime.strptime(request.POST['ped_dta'], '%Y-%m-%d')
            item.obr = Obra(obr_id=request.POST['obr_id'])
            item.cat_pes = CategoriaPessoa(pes_id = request.POST['cat_pes'])
            item.forn = Fornecedor.objects.get(forn_id=request.POST['forn'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
            item.save()
            
            # Agora que o Pedido foi salvo, podemos acessar o ped_id
            ped_id = item.ped_id

            # Caminho para salvar os arquivos do pedido
            xpath = os.path.join('media/pedido/', str(ped_id))
            # Cria o diretório se não existir
            os.makedirs(xpath, exist_ok=True)

            # Armazena os arquivos no sistema de arquivos, se estiverem presentes no request
            arquivos = request.FILES.getlist('arquivos')
            filepaths = []
            for arquivo in arquivos:
                xstorage = FileSystemStorage(location=xpath)
                filename = xstorage.save(arquivo.name, arquivo)
                filepath = os.path.join(xpath, filename)
                filepaths.append(filepath)

            # Atualiza o caminho do arquivo do Pedido com o primeiro caminho, se houver arquivos
            if filepaths:
                item.ped_arq_path ='/'+ filepaths[0]
                item.save()
                
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar a Pedido'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_del(request):
    try:
        if request.method == "POST":
            ped_id = request.POST['ped_id']
            item = Pedido.objects.get(pk=ped_id)
            
            arquivo_path = item.ped_arq_path
            
            if arquivo_path:
                arquivo_path = arquivo_path[1:] 
                if os.path.exists(arquivo_path):
                    os.remove(arquivo_path)
            
            # Exclui o registro do pedido
            item.delete()
            
            return JsonResponse({
                'item': None,
                'aviso': 'Excluído com sucesso!'
            }, status=200)
    except (Pedido.DoesNotExist, Exception) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao excluir o Pedido'
        }, status=500)
        
########################################################################Pedido Produto######################################################################################       
@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_lista(request):
    try:
        dados= PedidoProdutoSerializer(PedidoProduto.objects.filter(ped=request.POST['ped_id']).order_by('ped_prod_desc'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})

@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_atb(request):
    try:
        item = PedidoProdutoSerializer(PedidoProduto.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_add(request):
    try:
        ultimo_pedido = Pedido.objects.all().aggregate(Max('ped_id'))
        ultimo_ped_id = ultimo_pedido['ped_id__max']
        item = PedidoProduto()
        item.ped_prod_desc = request.POST['ped_prod_desc']
        item.ped_prod_qtd = request.POST['ped_prod_qtd']
        item.ped_prod_desc = request.POST['ped_prod_desc']
        item.cat_uni = CategoriaUnidade.objects.get(cat_uni_id=request.POST['cat_uni'])
        item.cat_prod = CategoriaProduto.objects.get(cat_prod_id=request.POST['cat_prod'])
        item.ped_id =ultimo_ped_id
        item.usu_cad = Pessoa(pes_id = user_session(request))
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Produto'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)


@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_add_2(request):
    try:
        item = PedidoProduto()
        item.ped_prod_desc = request.POST['ped_prod_desc']
        item.ped_prod_qtd = request.POST['ped_prod_qtd']
        item.ped_prod_desc = request.POST['ped_prod_desc']
        item.cat_uni = CategoriaUnidade.objects.get(cat_uni_id=request.POST['cat_uni2'])
        item.cat_prod = CategoriaProduto.objects.get(cat_prod_id=request.POST['cat_prod2'])
        item.ped = Pedido(ped_id=request.POST['ped_id'])
        item.usu_cad = Pessoa(pes_id = user_session(request))
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Especificação'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_edt(request):
    try:
        item=PedidoProduto.objects.get(pk=request.POST['ped_prod_id'])
        if request.method=="POST":
            item.ped_prod_desc = request.POST['ped_prod_desc']
            item.ped_prod_qtd = request.POST['ped_qtd']
            item.ped_prod_desc = request.POST['ped_desc']
            item.cat_uni = CategoriaUnidade.objects.get(cat_uni_id=request.POST['cat_uni'])
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
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

@login_required(login_url="vicosafundacoes:my-login")   
def ped_prod_del(request):
    try:
        if request.method=="POST":
            item=PedidoProduto.objects.get(pk=request.POST['ped_prod_id'])
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
#                              Pedido Especificação                                           #
##############################################################################################
@login_required(login_url="vicosafundacoes:my-login")   
def ped_esp_lista(request):
    try:
        dados= PedidoEspecificacaoSerializer(PedidoEspecificacao.objects.filter(ped=request.POST['ped_id']).order_by('ped_esp_obs'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})

@login_required(login_url="vicosafundacoes:my-login")   
def ped_esp_atb(request):
    try:
        item = PedidoEspecificacaoSerializer(PedidoEspecificacao.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
@login_required(login_url="vicosafundacoes:my-login")   
def ped_esp_add(request):
    try:
        item = PedidoEspecificacao()
        item.ped_esp_obs = request.POST['ped_esp_obs']
        item.ped_esp_psq = request.POST.get('ped_esp_psq') == 'on'
        item.ped_esp_fispq = request.POST.get('ped_esp_fispq') == 'on'
        item.ped = Pedido(ped_id=request.POST['ped_id'])
        item.usu_cad = Pessoa(pes_id = user_session(request))
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Especificação'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_esp_edt(request):
    try:
        item=PedidoEspecificacao.objects.get(pk=request.POST['ped_esp_id'])
        if request.method=="POST":
            item.ped_esp_obs = request.POST['ped_esp_obs']
            item.ped_esp_psq = request.POST.get('ped_esp_psq') == 'on'
            item.ped_esp_fispq = request.POST.get('ped_esp_fispq') == 'on'
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
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

@login_required(login_url="vicosafundacoes:my-login")   
def ped_esp_del(request):
    try:
        if request.method=="POST":
            item=PedidoEspecificacao.objects.get(pk=request.POST['ped_esp_id'])
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
#                              Pedido Especificação                                           #
##############################################################################################
@login_required(login_url="vicosafundacoes:my-login")   
def ped_ent_lista(request):
    try:
        dados= PedidoEntregaSerializer(PedidoEntrega.objects.filter(ped=request.POST['ped_id']).order_by('ped_ent_rua'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ent_atb(request):
    try:
        item = PedidoEntregaSerializer(PedidoEntrega.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
@login_required(login_url="vicosafundacoes:my-login")   
def ped_ent_add(request):
    try:
        item = PedidoEntrega()
        item.ped_ent_rua = request.POST['ped_ent_rua']
        item.ped_ent_bairro = request.POST['ped_ent_bairro']
        item.ped_ent_cidade = request.POST['ped_ent_cidade']
        item.ped_ent_num = request.POST['ped_ent_num']
        item.ped_ent_com = request.POST['ped_ent_com']
        item.ped_ent_cep = request.POST['ped_ent_cep']
        item.ped_ent_obs = request.POST['ped_ent_obs']
        item.ped_ent_dta = datetime.strptime(request.POST['ped_ent_dta'], '%Y-%m-%d')
        item.usu_cad = Pessoa(pes_id = user_session(request))
        item.cat_pes = CategoriaPessoa(pes_id = request.POST['cat_pes2'] )
        item.ped = Pedido(ped_id=request.POST['ped_id'])
        item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Especificação'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ent_edt(request):
    try:
        item=PedidoEntrega.objects.get(pk=request.POST['ped_ent_id'])
        if request.method=="POST":
            item.ped_ent_rua = request.POST['ped_ent_rua']
            item.ped_ent_bairro = request.POST['ped_ent_bairro']
            item.ped_ent_cidade = request.POST['ped_ent_cidade']
            item.ped_ent_num = request.POST['ped_ent_num']
            item.ped_ent_com = request.POST['ped_ent_com']
            item.ped_ent_cep = request.POST['ped_ent_cep']
            item.ped_ent_obs = request.POST['ped_ent_obs']
            item.ped_ent_dta = datetime.strptime(request.POST['ped_ent_dta'], '%Y-%m-%d')
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Entrega'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ent_del(request):
    try:
        if request.method=="POST":
            item=PedidoEntrega.objects.get(pk=request.POST['ped_ent_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar Entrega, '},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'},
            status=200) 
        
        
        
    
##############################################################################################
#                              Pedido Especificação                                           #
##############################################################################################
@login_required(login_url="vicosafundacoes:my-login")   
def ped_ver_lista(request):
    try:
        dados= PedidoVerificacaoSerializer(PedidoVerificacao.objects.filter(ped=request.POST['ped_id']).order_by('ped_ver_id'), many=True)
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error,
            'aviso': 'Problema ao consultar os dados'},
            status=500)
    else:
        return JsonResponse({'dados':dados.data})

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ver_atb(request):
    try:
        item = PedidoVerificacaoSerializer(PedidoVerificacao.objects.get(pk=request.GET['id']))
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': error, 
            'aviso': 'Problema ao consultar os dados'}, 
            status=500)
    else:
        return JsonResponse(item.data) 
    
@login_required(login_url="vicosafundacoes:my-login")   
def ped_ver_add(request):
    try:
        # Obter o último número sequencial
        ultimo_numero_sequencial = PedidoVerificacao.objects.aggregate(Max('ped_ver_rnc_num'))

        # Verificar se há um número de sequência anterior, se não, iniciar em 1
        if 'ped_ver_rnc_num__max' not in ultimo_numero_sequencial or ultimo_numero_sequencial['ped_ver_rnc_num__max'] is None:
            novo_numero_sequencial = "N°1"
        else:
            ultimo_numero = ultimo_numero_sequencial['ped_ver_rnc_num__max']
            numero_sequencial = int(ultimo_numero[2:])  # Ignorando os dois primeiros caracteres 'N°'
            novo_numero_sequencial = "N°" + str(numero_sequencial + 1)

        item = PedidoVerificacao()
        
        if request.POST.get('ped_ver_chk') == 'true':
            item.ped_ver_chk = True
            item.ped_ver_desc = request.POST['ped_ver_desc']
            item.ped_ver_sol = request.POST['ped_ver_sol']
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_cad = Pessoa(pes_id = user_session(request))
            item.save()
        else:
            item.ped_ver_chk = False
            item.ped_ver_rnc_num = novo_numero_sequencial
            item.ped_ver_desc = request.POST['ped_ver_desc']
            item.ped_ver_sol = request.POST['ped_ver_sol']
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_cad = Pessoa(pes_id = user_session(request))
            item.save()
    except (Exception, DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao adicionar a Especificação'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Adicionado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ver_edt(request):
    try:
        item=PedidoVerificacao.objects.get(pk=request.POST['ped_ver_id'])
        if request.method=="POST":
            item.ped_ver_chk = request.POST.get('ped_ver_chk') == 'true'
            item.ped_ver_desc = request.POST['ped_ver_desc']
            item.ped_ver_sol = request.POST['ped_ver_sol']
            item.ped = Pedido(ped_id=request.POST['ped_id'])
            item.usu_alt = Pessoa(pes_id = user_session(request))
            item.save()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao editar o Entrega'},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Editado com sucesso!'},
            status=200)

@login_required(login_url="vicosafundacoes:my-login")   
def ped_ver_del(request):
    try:
        if request.method=="POST":
            item=PedidoVerificacao.objects.get(pk=request.POST['ped_ver_id'])
            item.delete()
    except(Exception,DatabaseError) as error:
        print(error)
        return JsonResponse({
            'error': str(error),
            'aviso': 'Erro ao deletar Entrega, '},
            status=500)
    else:
        return JsonResponse({
            'item': None,
            'aviso': 'Excluido com sucesso!'},
            status=200) 