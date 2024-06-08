from rest_framework import serializers
from.models import*

class ObraSerializer(serializers.ModelSerializer):

    cat_obr_id = serializers.IntegerField(source="cat_obr.cat_obr_id", read_only="True")
    cat_obr_nome = serializers.CharField(source="cat_obr.cat_obr_nome", read_only="True")
    
    cat_sta_id = serializers.IntegerField(source="cat_obr.cat_obr_id", read_only="True")
    cat_sta_nome = serializers.CharField(source="cat_sta.cat_sta_nome", read_only="True")
    cat_sta_cor = serializers.CharField(source="cat_sta.cat_sta_cor", read_only="True")

    class Meta:
        model = Obra
        fields = '__all__'  
        
        
class PedidoSerializer(serializers.ModelSerializer):
    forn_id = serializers.IntegerField(source="forn.forn_id", read_only=True)
    forn_nome = serializers.CharField(source="forn.forn_nome", read_only=True)
    forn_cnpj = serializers.CharField(source="forn.forn_cnpj", read_only=True)
    forn_ies = serializers.CharField(source="forn.forn_ies", read_only=True)
    pes_id = serializers.IntegerField(source="cat_pes.pes_id", read_only=True)
    pes_nome = serializers.CharField(source="cat_pes.pes_nome", read_only=True)
    pedido_produtos = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = '__all__'

    def get_pedido_produtos(self, obj):
        # Filtragem reversa para obter os produtos relacionados a este pedido
        pedido_produtos = PedidoProduto.objects.filter(ped=obj)
        # Serializar os produtos usando o PedidoProdutoSerializer
        serializer = PedidoProdutoSerializer(pedido_produtos, many=True)
        return serializer.data

class PedidoEspecificacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = PedidoEspecificacao
        fields = '__all__'  
        
class PedidoEntregaSerializer(serializers.ModelSerializer):

    ped_id = serializers.IntegerField(source="ped.ped_id", read_only="True")
    ped_num = serializers.CharField(source="ped.ped_num", read_only="True")
    obr_prop = serializers.CharField(source="ped.obr.obr_prop", read_only="True")

    cat_pes_id = serializers.IntegerField(source="cat_pes.pes_id", read_only="True")
    cat_pes_nome = serializers.CharField(source="cat_pes.pes_nome", read_only="True")
    
    usu_cad_id = serializers.IntegerField(source="usu_cad.usu_cad_id", read_only="True")
    usu_cad_nome = serializers.CharField(source="usu_cad.pes_nome", read_only="True")
    
    class Meta:
        model = PedidoEntrega
        fields = '__all__'  
        
class PedidoVerificacaoSerializer(serializers.ModelSerializer):

    
    usu_cad_id = serializers.IntegerField(source="usu_cad.usu_cad_id", read_only="True")
    usu_cad_nome = serializers.CharField(source="usu_cad.pes_nome", read_only="True")
    
    class Meta:
        model = PedidoVerificacao
        fields = '__all__'  

class PedidoProdutoSerializer(serializers.ModelSerializer):

    
    usu_cad_id = serializers.IntegerField(source="usu_cad.usu_cad_id", read_only="True")
    usu_cad_nome = serializers.CharField(source="usu_cad.pes_nome", read_only="True")
    
    cat_uni_id = serializers.IntegerField(source="cat_uni.cat_uni_id", read_only="True")
    cat_uni_nome = serializers.CharField(source="cat_uni.cat_uni_nome", read_only="True")
    cat_uni_cor = serializers.CharField(source="cat_uni.cat_uni_cor", read_only="True")

    cat_prod_id = serializers.IntegerField(source="cat_prod.cat_prod_id", read_only="True")
    cat_prod_nome = serializers.CharField(source="cat_prod.cat_prod_nome", read_only="True")
    
    
    class Meta:
        model = PedidoProduto
        fields = '__all__'  