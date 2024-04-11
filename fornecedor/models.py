from django.db import models
from categorias.models import *

# Create your models here.
class Fornecedor(models.Model):
    forn_id = models.BigAutoField(primary_key=True)
    forn_nome = models.CharField(max_length=256)
    forn_apelido = models.CharField(max_length=100)
    forn_cnpj = models.CharField(max_length=50)
    forn_ies = models.CharField(max_length=50)
    forn_desc=models.CharField(max_length=5000)
    cat_imp = models.ForeignKey(CategoriaImpacto, on_delete=models.DO_NOTHING)
    cat_tip = models.ForeignKey(CategoriaTipo, on_delete=models.DO_NOTHING)
    usu_cad_dta = models.DateTimeField(auto_now_add=True)
    usu_alt_dta = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'fornecedor'

class FornecedorContato(models.Model):
    forn_ctt_id = models.BigAutoField(primary_key=True)
    forn_ctt_nome = models.CharField(max_length=256)
    forn_ctt_tel = models.CharField(max_length=100)
    forn_ctt_email = models.CharField(max_length=50)
    forn_ctt_ativo = models.BooleanField()
    forn = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    # usu_cad
    # usu_alt
    usu_cad_dta = models.DateTimeField(auto_now_add=True)
    usu_alt_dta = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'fornecedorcontato'


class FornecedorAvaliacao(models.Model):
    forn_aval_id = models.BigAutoField(primary_key=True)
    forn_aval_dta = models.DateTimeField()
    forn_aval_evid = models.CharField(max_length=5000)
    cat_aval = models.ForeignKey(CategoriaAvaliacao, on_delete=models.DO_NOTHING)
    pes = models.ForeignKey(CategoriaPessoa, on_delete=models.DO_NOTHING, related_name='pes_forn_aval')
    forn = models.ForeignKey(Fornecedor, on_delete=models.DO_NOTHING, related_name='pes_forn')
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.DO_NOTHING, related_name='usu_cad_forn_aval')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.DO_NOTHING, related_name='usu_alt_forn_aval')
    usu_cad_dta = models.DateTimeField(auto_now_add=True)
    usu_alt_dta = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'fornecedoravaliacao'
