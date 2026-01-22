from django.contrib import admin
from .models import Inscricoes,Participante,Email,Eventos,Pagamentos,Organizador,Relatorio

@admin.register(Organizador)
class OrganizadorAdmin(admin.ModelAdmin):
    list_display=[
        'nome',
        'email'
    ]

@admin.register(Participante)
class PartipanteAdmin(admin.ModelAdmin):
    list_display=[
        'nome',
        'email'
    ]

@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display=[
        'titulo',
        'organizador',
        'status'
    ]
@admin.register(Pagamentos)
class PAgamentosAdmin(admin.ModelAdmin):
    list_display=[
        'participante',
        'evento',
        'pago',
        'status',
        'ativo'
    ]

@admin.register(Inscricoes)
class InscricoesAdmin(admin.ModelAdmin):
    list_display=[
        'participante',
        'evento',
        'data',
        'status',
    ]
@admin.register(Email)
class emailAdmim(admin.ModelAdmin):
    list_display=[
        'destinatario',
        'evento',
        'tipo',
    ]

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = (
        'total_evento',
        'total_inscritos',
        'evento_populares',
        'evento_sem_inscritos',
        'faturacao',
        'email_pendentes',
    )

    def total_eventos(self, obj):
        return obj.total_eventos()

    def total_inscritos(self, obj):
        return obj.total_inscritos()

    def evento_populares(self, obj):
        return obj.evento_populares()

    def evento_sem_inscritos(self, obj):
        return obj.evento_sem_inscritos()

    def faturacao(self, obj):
        return obj.Faturacao()

    def email_pendentes(self, obj):
        return obj.email_pendentes()