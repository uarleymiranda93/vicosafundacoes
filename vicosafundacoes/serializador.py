from rest_framework import serializers
from.models import*



class FornecedorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Fornecedor
        fields = '__all__'



class FornecedorContatoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FornecedorContato
        fields = '__all__'
        