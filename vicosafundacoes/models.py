from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    forn_id = models.BigAutoField(primary_key=True)
    forn_nome = models.CharField(max_length=256)
    forn_apelido = models.CharField(max_length=100)
    forn_cnpj = models.CharField(max_length=50)
    forn_ies = models.CharField(max_length=50)
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