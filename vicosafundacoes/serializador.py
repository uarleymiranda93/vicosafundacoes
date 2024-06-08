from rest_framework import serializers
from.models import*
from django.utils import timezone
import datetime


class DateTimeToDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        # Verifica se o valor é uma instância de datetime
        if isinstance(value, datetime.datetime):
            # Retorna apenas a data, ignorando a hora
            return value.date()
        # Se não for uma instância de datetime, apenas retorna o valor
        return value

class PessoaSerializer(serializers.ModelSerializer):
    
    usu_cad_dta = DateTimeToDateField()
    usu_alt_dta = DateTimeToDateField()
    
    class Meta:
        model = Pessoa
        fields = '__all__'  
        