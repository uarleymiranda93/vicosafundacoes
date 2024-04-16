from rest_framework import serializers
from.models import*



class FornecedorSerializer(serializers.ModelSerializer):
    cat_imp_id = serializers.IntegerField(source="cat_imp.cat_imp_id", read_only="True")
    cat_tip_id = serializers.IntegerField(source="cat_tip.cat_tip_id", read_only="True")
    cat_tip_nome = serializers.CharField(source="cat_tip.cat_tip_nome", read_only="True")
    cat_imp_nome = serializers.CharField(source="cat_imp.cat_imp_nome", read_only="True")
    cat_imp_cor = serializers.CharField(source="cat_imp.cat_imp_cor", read_only="True")
    forn_cont = serializers.SerializerMethodField()

    class Meta:
        model = Fornecedor
        fields = '__all__'

    def get_forn_cont(self, obj):
        contatos = FornecedorContato.objects.filter(forn=obj)
        contatos_data = []
        for contato in contatos:
            contatos_data.append({
                'forn_ctt_nome': contato.forn_ctt_nome,
                'forn_ctt_tel': contato.forn_ctt_tel,
            })
        return contatos_data


class FornecedorContatoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FornecedorContato
        fields = '__all__'


class FornecedorAvaliacaoSerializer(serializers.ModelSerializer):
    cat_aval_id = serializers.IntegerField(source="cat_imp.cat_imp_id", read_only="True")
    pes_id = serializers.IntegerField(source="cat_tip.cat_tip_id", read_only="True")
    cat_aval_nome = serializers.CharField(source="cat_aval.cat_aval_nome", read_only="True")
    pes_nome = serializers.CharField(source="pes.pes_nome", read_only="True")
    forn_nome = serializers.CharField(source="forn.forn_nome", read_only="True")

    
    class Meta:
        model = FornecedorAvaliacao
        fields = '__all__'


class FornecedorAvaliacaoItemSerializer(serializers.ModelSerializer):
    cat_aval_item_id = serializers.IntegerField(source="cat_aval_item.cat_aval_item_id", read_only="True")
    cat_aval_item_nome = serializers.CharField(source="cat_aval_item.cat_aval_item_nome", read_only="True")
    
    class Meta:
        model = FornecedorAvaliacaoItem
        fields = '__all__'


class FornecedorMonitoramentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FornecedorMonitoramento
        fields = '__all__'       
        