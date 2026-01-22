from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Inscricoes, Pagamentos, StatusInscricao, StatusPagamento, Email, TipoEmail, StatusEmail
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime,timedelta

@receiver(post_save, sender=Inscricoes)
def enviar_email_automatico(sender, instance, created, **kwargs):
    if created:
        instance.send_email()
    else:
        # Verificar emails já enviados
        email_confirmacao_enviado = Email.objects.filter(
            evento=instance.evento,
            destinatario=instance.participante,
            tipo=TipoEmail.CONFIRMACAO_INSCRICAO,
            status=StatusEmail.ENVIADO
        ).exists()
        
        email_cancelamento_enviado = Email.objects.filter(
            evento=instance.evento,
            destinatario=instance.participante,
            tipo=TipoEmail.CANCELAMENTO,
            status=StatusEmail.ENVIADO
        ).exists()
        
        email_reembolso_enviado = Email.objects.filter(
            evento=instance.evento,
            destinatario=instance.participante,
            tipo=TipoEmail.REEMBOLSO,  
            status=StatusEmail.ENVIADO
        ).exists()
        email_lembrete_enviado = Email.objects.filter(
            evento=instance.evento,
            destinatario=instance.participante,
            tipo=TipoEmail.LEMBRETE,  
            status=StatusEmail.ENVIADO
        ).exists()
        
        # EMAIL DE CONFIRMAÇÃO
        if instance.status == StatusInscricao.CONFIRMADA and not email_confirmacao_enviado:
            assunto = f'Confirmação do evento {instance.evento.titulo}'
            mensagem = f"""
Olá {instance.participante.nome},

A sua inscrição no evento "{instance.evento.titulo}" foi confirmada com sucesso!

Detalhes:
Evento: {instance.evento.titulo}
Data: {instance.evento.inicio.date()}
Local: {instance.evento.localizacao}

Nos vemos lá!

Obrigado!
"""
            try:
                send_mail(
                    assunto,
                    mensagem,
                    settings.EMAIL_HOST_USER,
                    [instance.participante.email],
                    fail_silently=False
                )
                Email.objects.create(
                    destinatario=instance.participante,
                    evento=instance.evento,
                    tipo=TipoEmail.CONFIRMACAO_INSCRICAO,
                    assunto=assunto,
                    mensagem=mensagem,
                    status=StatusEmail.ENVIADO,
                    enviado=True
                )
            except Exception as e:
                print(f"Erro ao enviar email de confirmação: {e}")
            
            # Atualizar status do pagamento
            Pagamentos.objects.filter(
                evento=instance.evento,
                participante=instance.participante
            ).update(
                status=StatusPagamento.CONCLUIDO,
                ativo=True
            )
        
        # EMAIL DE CANCELAMENTO
        elif instance.status == StatusInscricao.CANCELADA and not email_cancelamento_enviado:
            assunto = f'Cancelamento de inscrição - {instance.evento.titulo}'
            mensagem = f"""
Olá {instance.participante.nome},

A sua inscrição no evento "{instance.evento.titulo}" foi cancelada.

Detalhes:
Evento: {instance.evento.titulo}
Data: {instance.evento.inicio.date()}
Local: {instance.evento.localizacao}

Se você pagou pela inscrição, em breve receberá o reembolso.

Obrigado!
"""
            try:
                send_mail(
                    assunto,
                    mensagem,
                    settings.EMAIL_HOST_USER,
                    [instance.participante.email],
                    fail_silently=False
                )
                Email.objects.create(
                    destinatario=instance.participante,
                    evento=instance.evento,
                    tipo=TipoEmail.CANCELAMENTO,
                    assunto=assunto,
                    mensagem=mensagem,
                    status=StatusEmail.ENVIADO,
                    enviado=True
                )
            except Exception as e:
                return Response(
                    {'erro':f'Erro ao enviar email de cancelamento: {str(e)}'
                    })
            
            Pagamentos.objects.filter(
                evento=instance.evento,
                participante=instance.participante
            ).update(
                status=StatusPagamento.CANCELADO,
                ativo=False
            )
        
        # EMAIL DE REEMBOLSO
        elif instance.status == StatusInscricao.REEMBOLSADO and not email_reembolso_enviado:
            assunto = f'Reembolso confirmado - {instance.evento.titulo}'
            mensagem = f"""
Olá {instance.participante.nome},

O seu reembolso referente ao evento "{instance.evento.titulo}" foi processado com sucesso!

Detalhes:
Evento: {instance.evento.titulo}
Data: {instance.evento.inicio.date()}
Local: {instance.evento.localizacao}

O valor será creditado em sua conta em até 5 dias úteis.

Obrigado!
"""
            try:
                send_mail(
                    assunto,
                    mensagem,
                    settings.EMAIL_HOST_USER,
                    [instance.participante.email],
                    fail_silently=False
                )
                Email.objects.create(
                    destinatario=instance.participante,
                    evento=instance.evento,
                    tipo=TipoEmail.REEMBOLSO,
                    assunto=assunto,
                    mensagem=mensagem,
                    status=StatusEmail.ENVIADO,
                    enviado=True
                )
            except Exception as e:
                return Response({
                    'erro':f'Erro ao enviar email de reembolso: {str(e)}'
                },status=status.HTTP_400_BAD_REQUEST)
            
            Pagamentos.objects.filter(
                evento=instance.evento,
                participante=instance.participante
            ).update(
                status=StatusPagamento.REEMBOLSADO,
                ativo=False
            )
        elif instance.pago==True and instance.status==StatusInscricao.CONFIRMADA and not email_lembrete_enviado:
                dia=datetime.now().date()
                dia_evento=instance.evento.inicio.date()
                if dia_evento-dia== timedelta(days=2):
                    assunto=f'Lembrete do evento {instance.evento.titulo}'
                    mensagem=f"""
        Olá {instance.participante.nome},

        Faltam 2 dias para o evento "{instance.evento.titulo}".

        Detalhes:
        Evento: {instance.evento.titulo}
        Data: {instance.evento.fim.date()}
        Local: {instance.evento.localizacao}


        Não se esqueça de comparecer!.

        Obrigado!
        """
                    try:
                        
                        send_mail(
                            assunto,
                            mensagem,
                            settings.EMAIL_HOST_USER,
                            [instance.participante.email],
                            fail_silently=False
                        )

                        Email.objects.create(
                            destinatario=instance.participante,
                            evento=instance.evento,
                            tipo=TipoEmail.LEMBRETE,
                            assunto=assunto,
                            mensagem=mensagem,
                            status=StatusEmail.ENVIADO         
                        )
                    except Exception as e:
                        return Response({
                            'erro':f'Erro ao enviar email de cancelamento: {str(e)}'
                        })