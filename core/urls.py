from django.urls import path,include
from .views import VerEventosAPIViwes,VerEventosIncritosAPIView,VerMeusEventosAPIViews,VerOrganizadorInscricoesAPIView,InscreverAPIView,CriarEventosAPIViews,CriarOrganizadorAPIView,CriarParticipanteAPIView,RelatorioAPIView,PerfilAPIView,VereventoAPIView,ListarEmailsAPIView,InscricaoConfirmadaAPIView,CancelarInscricaoAPIView,ReembolsarInscricaoAPIView,PagamentosAPIView


urlpatterns = [
    path('perfil/',PerfilAPIView.as_view(),name='perfil'),#verificado
    path('criar-evento/',CriarEventosAPIViews.as_view(),name='criar_evento'),#verificado
    path('ver-eventos/',VerEventosAPIViwes.as_view(),name='ver_eventos'),#verificado
    path('ver-eventos/organizador/',VerMeusEventosAPIViews.as_view(),name='ver_meus_eventos'),#verificado
    path('ver-evento/<int:evento_id>/',VereventoAPIView.as_view(),name='ver_evento'),#verificado
    path('ver-eventos/inscritos/',VerEventosIncritosAPIView.as_view(),name='ver_eventos_inscritos'),#verificado
    path('ver-inscricoes/eventos/<int:evento_id>/',VerOrganizadorInscricoesAPIView.as_view(),name='ver_inscritos'),#verificado
    path('inscrever/evento/<int:evento_id>/',InscreverAPIView.as_view(),name='inscrever'),#verificado
    path('criar/organizador/',CriarOrganizadorAPIView.as_view(),name='criar_organizador'),#verificado
    path('criar/participante/',CriarParticipanteAPIView.as_view(),name='criar_participante'),#verificado
    path('relatorio/',RelatorioAPIView.as_view(),name='relatorio'),#verificado
    path('emails/evento/<int:evento_id>/',ListarEmailsAPIView.as_view(),name='emails'),#verificado
    path('incricao/<int:inscricao_id>/estado/confirmado/',InscricaoConfirmadaAPIView.as_view(),name='inscricao_confirmada'),
    path('incricao/<int:inscricao_id>/estado/cancelada/',CancelarInscricaoAPIView.as_view(),name='inscricao_cancelada'),
    path('incricao/<int:inscricao_id>/estado/reembolso/',ReembolsarInscricaoAPIView.as_view(),name='inscricao_reembolsada'),
    path('incricao/<int:inscricao_id>/pagamento/',PagamentosAPIView.as_view(),name='pagamento'),
    path('pagamento/<int:pagamento_id>/confirmar/',PagamentosAPIView.as_view(),name='confirmar_pagamento'),
]