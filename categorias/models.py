from vicosafundacoes.models import *
from django.db import models

class CategoriaPessoa(models.Model):
    
    pes_id = models.BigAutoField(primary_key=True)
    pes_nome = models.CharField(max_length=255)
    pes_email = models.CharField(max_length=255)
    pes_ativo = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'categoriapessoa'
        

class CategoriaImpacto(models.Model):
    
    cat_imp_id = models.BigAutoField(primary_key=True)
    cat_imp_nome = models.CharField(max_length=255)
    cat_imp_cor = models.CharField(max_length=255)
    cat_imp_ativo = models.BooleanField()
    
    class Meta:
        managed = False
        db_table = 'categoriaimpacto'
        
        
class CategoriaStatus(models.Model):
    
    cat_sta_id = models.BigAutoField(primary_key=True)
    cat_sta_nome = models.CharField(max_length=255)
    cat_sta_cor = models.CharField(max_length=255)
    cat_sta_ativo = models.BooleanField(default=True)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_cad_sta')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_alt_sta')

    
    class Meta:
        managed = False
        db_table = 'categoriastatus'
        
        
class CategoriaTipo(models.Model):
    cat_tip_id = models.BigAutoField(primary_key=True)
    cat_tip_nome = models.CharField(max_length=255)
    cat_tip_cor = models.CharField(max_length=255)
    cat_tip_ativo = models.BooleanField(default=True)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_cad_tip')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_alt_tip')
    
    class Meta:
        managed = False
        db_table = 'categoriatipo'
        
        
class CategoriaProduto(models.Model):
    cat_prod_id = models.BigAutoField(primary_key=True)
    cat_prod_nome = models.CharField(max_length=255)
    cat_prod_cor = models.CharField(max_length=255)
    cat_prod_ativo = models.BooleanField(default=True)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_cad_prod')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_alt_prod')
    
    
    class Meta:
        managed = False
        db_table = 'categoriaproduto'


class CategoriaAvaliacao(models.Model):
    cat_aval_id = models.BigAutoField(primary_key=True)
    cat_aval_nome = models.CharField(max_length=255)
    cat_aval_cor = models.CharField(max_length=255)
    cat_aval_ativo = models.BooleanField(default=True)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_cad_aval')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_alt_aval')
    
    
    class Meta:
        managed = False
        db_table = 'categoriaavaliacao'


class CategoriaAvaliacaoItem(models.Model):
    cat_aval_item_id = models.BigAutoField(primary_key=True)
    cat_aval_item_nome = models.CharField(max_length=255)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_cad_aval_item')
    usu_alt = models.ForeignKey(CategoriaPessoa, on_delete=models.CASCADE, related_name='usu_alt_aval_item')
    
    
    class Meta:
        managed = False
        db_table = 'categoriaavaliacaoitem'


class CategoriaObra(models.Model):
    cat_obr_id = models.BigAutoField(primary_key=True)
    cat_obr_nome = models.CharField(max_length=255)
    cat_obr_cor = models.CharField(max_length=255)
    cat_obr_ativo = models.BooleanField(default=True)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_cat_obr')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_cat_obr')
    
    
    class Meta:
        managed = False
        db_table = 'categoriaobra'


class CategoriaUnidade(models.Model):
    cat_uni_id = models.BigAutoField(primary_key=True)
    cat_uni_nome = models.CharField(max_length=255)
    cat_uni_cor = models.CharField(max_length=255)
    cat_uni_ativo = models.BooleanField(default=True)
    usu_alt_dta = models.DateField(auto_now_add=True)
    usu_cad_dta = models.DateField(auto_now=True)
    usu_cad = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_cad_cat_uni')
    usu_alt = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='usu_alt_cat_uni')


    class Meta:
        managed = False
        db_table = 'categoriaunidade'

        