from django.db import models

class Pessoa (models.Model):
    pes_id = models.BigAutoField(primary_key=True)
    pes_nome = models.CharField(max_length=255)
    pes_doc = models.CharField(max_length=20)
    pes_ctt = models.CharField(max_length=20)
    pes_nome_adm = models.CharField(max_length=255)
    pes_adm_id = models.IntegerField()
    pes_email = models.CharField(max_length=255)
    usu_cad_dta = models.DateField(auto_now_add=True)
    usu_alt_dta = models.DateField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'pessoa'