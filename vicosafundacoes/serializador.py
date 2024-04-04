from rest_framework import serializers
from.models import*



class FornecedorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Fornecedor
        fields = '__all__'
        