from rest_framework import serializers
from .models import Usuario, Estoque, Venda, Atividade, DiarioBordo, RPD, LogPODDiario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'tipo_usuario', 'is_staff'] # Add other fields as needed

class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = '__all__'
        read_only_fields = ['usuario', 'data_cadastro', 'ultima_atualizacao'] # User is set by the view

class VendaSerializer(serializers.ModelSerializer):
    estoque_item_display = serializers.CharField(source='estoque_item.__str__', read_only=True)

    class Meta:
        model = Venda
        fields = '__all__'
        read_only_fields = ['usuario', 'preco_unitario', 'preco_total', 'data_venda'] # These are calculated or set by the backend

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'
        read_only_fields = ['usuario', 'data_cadastro']

class DiarioBordoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiarioBordo
        fields = '__all__'
        read_only_fields = ['usuario', 'data_registro']

class RPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = RPD
        fields = '__all__'
        read_only_fields = ['usuario', 'data_registro']

class LogPODDiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogPODDiario
        fields = '__all__'
        read_only_fields = ['usuario', 'data_registro']