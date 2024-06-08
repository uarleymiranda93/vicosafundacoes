from django.db import models
from vicosafundacoes.models import *
from categorias.models import *
from fornecedor.models import *

# Create your models here.
class Obra(models.Model):
    obr_id = models.BigAutoField(primary_key=True)
    obr_prop = models.CharField(max_length=255)
    obr_loc = models.CharField(max_length=255)
    obr_dta_ini = models.DateField()
    obr_dta_fin = models.DateField()
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    cat_obr = models.ForeignKey(CategoriaObra, on_delete=models.CASCADE)
    cat_sta = models.ForeignKey(CategoriaStatus, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_obr')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_obr')
    
    
    class Meta:
        managed = False
        db_table = 'obra'
        
class Pedido(models.Model):
    ped_id = models.BigAutoField(primary_key=True)
    ped_num = models.CharField(max_length=5000)
    ult_num = models.CharField(max_length=5000)
    ped_arq_path = models.CharField(max_length=255)
    ped_dta = models.DateField()
    cat_pes = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE)
    forn = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    obr = models.ForeignKey(Obra, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_ped')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_ped')
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedido'
        
        
class PedidoProduto(models.Model):
    ped_prod_id = models.BigAutoField(primary_key=True)
    ped_prod_desc = models.CharField(max_length=255)
    ped_prod_qtd = models.DecimalField(max_digits=10, decimal_places=2)
    cat_uni = models.ForeignKey(CategoriaUnidade, on_delete=models.CASCADE)
    cat_prod = models.ForeignKey(CategoriaProduto, on_delete=models.CASCADE)
    ped = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_pod_ped')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_pod_ped')
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedidoproduto'
        
class PedidoEspecificacao(models.Model):
    ped_esp_id = models.BigAutoField(primary_key=True)
    ped_esp_obs = models.CharField(max_length=5000)
    ped_esp_psq = models.BooleanField(default=True)
    ped_esp_fispq = models.BooleanField(default=True)
    ped = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_ped_esp')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_ped_esp')
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedidoespecificacao'
        
        
        
class PedidoEntrega(models.Model):
    ped_ent_id = models.BigAutoField(primary_key=True)
    ped_ent_rua = models.CharField(max_length=5000)
    ped_ent_bairro = models.CharField(max_length=5000)
    ped_ent_cidade = models.CharField(max_length=5000)
    ped_ent_num = models.CharField(max_length=5000)
    ped_ent_com = models.CharField(max_length=5000)
    ped_ent_cep = models.CharField(max_length=5000)
    ped_ent_obs = models.CharField(max_length=5000)
    ped = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cat_pes = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_ped_ent')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_ped_ent')
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedidoentrega'
        
        
class PedidoVerificacao(models.Model):
    ped_ver_id = models.BigAutoField(primary_key=True)
    ped_ver_chk = models.BooleanField(default=True)
    ped_ver_rnc_num = models.CharField(max_length=5000)
    ped_ver_desc = models.CharField(max_length=5000)
    ped_ver_sol = models.CharField(max_length=5000)
    ped = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_ped_ver')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_ped_ver')
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pedidoverificacao'