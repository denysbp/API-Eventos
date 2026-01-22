from .models import Pagamentos,Participante,Email,Eventos,Organizador,Relatorio,Inscricoes
from django.contrib.auth.models import User
from rest_framework import serializers


class ParticipanteSerializer(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model = Participante
        fields = [
            'username',
            'password',
            'nome',
            'email'
        ]

    def create(self,validated_data):
        username=validated_data.pop('username')
        password=validated_data.pop('password')
        user=User.objects.create_user(
            username=username,
            password=password
        )
        participante=Participante.objects.create(
            user=user,
            **validated_data
        )
        return participante
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Já existe um usario com este username!')
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('ja existe um usuario com este email!')
        return value
class OrganizadorSerializers(serializers.ModelSerializer):
    username=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model = Organizador
        fields = [
            'username',
            'password',
            'nome',
            'email'
        ]

    def create(self, validated_data):
        username=validated_data.pop('username')
        password=validated_data.pop('password')
        user=User.objects.create_user(
            username=username,
            password=password    
        )
        organizador=Organizador.objects.create(
            user=user,
            **validated_data
        )
        return organizador
    

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Já existe um usario com este username!')
        return value
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('ja existe um usuario com este email!')
        return value

class PagamentosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pagamentos
        fields = [
            'evento',
            'participante',
            'pago',
            'status',
            'ativo'
        ]
        read_only_fields = [
            'evento',
            'participante',
            'status'
        ]

class IncricoesSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Inscricoes
        fields = [
            'participante',
            'status',
            'data',
            'evento',
            'pago'
        ]
        read_only_fields = [
            'evento',
            'participante',
            'data'
        ]

class RelatorioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = '__all__'

class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = [
            'destinatario',
            'evento',
            'tipo',
            'assunto',
            'mensagem',
            'status',
            'data_criacao',
            'data_envio',
            'tentativas'
        ]
        read_only_fields = [
            'status',
            'data_criacao',
            'data_envio',
            'tentativas'
        ]


class EventosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = [
            'id',
            'organizador',
            'titulo',
            'descricao',
            'inicio',
            'fim',
            'localizacao',
            'Lotacao',
            'preco',
            'status',
            'inscritos'
        ]
        read_only_fields = [
            'organizador',
            'status'
        ]

class InscricaoEventoSerializer(serializers.ModelSerializer):
    Titulo = serializers.CharField(source='evento.titulo')
    Inicio = serializers.DateTimeField(source='evento.inicio')
    Localizacao = serializers.CharField(source='evento.localizacao')
    Estado = serializers.CharField(source='evento.status')

    class Meta:
        model = Inscricoes
        fields = ['Titulo', 'Inicio', 'Localizacao', 'Estado']