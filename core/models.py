from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from django.core.mail import send_mail
from django.conf import settings



class StatusInscricao(models.TextChoices):
    PENDENTE = "P", "Pendente"
    CONFIRMADA = "C", "Confirmada"
    CANCELADA = "X", "Cancelada"
    REEMBOLSADO="R","Reembolsado"


class StatusPagamento(models.TextChoices):
    PENDENTE="P","Pendente"
    CONCLUIDO="C","Concluido"
    CANCELADO="X","Cancelado"
    REEMBOLSADO="R","Reembolsado"

class Statusevento(models.TextChoices):
    EVENTO_ATIVO="A","ATIVO"
    EVENTO_LOTADO="L","Lotado"
    EVENTO_CONCLUIDO="C","Concluido"
    EVENTO_CANCELADO="X","Cancelado"

class Organizador(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='organizador'
    )

    nome=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    def __str__(self):
        return self.nome
    
class Participante(models.Model):
    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='participante'
    )
        
    nome=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.nome



class Eventos(models.Model):
    organizador=models.ForeignKey(
        Organizador,
        related_name='organizador_eventos',
        on_delete=models.CASCADE
    )
    titulo=models.CharField(max_length=100)
    descricao=models.TextField(max_length=300)
    inicio=models.DateTimeField()
    fim=models.DateTimeField()
    localizacao=models.CharField(max_length=200)
    Lotacao=models.PositiveBigIntegerField()
    preco=models.IntegerField()
    status=models.CharField(
        max_length=10,
        choices=Statusevento.choices,
        default=Statusevento.EVENTO_ATIVO
    )
    inscritos=models.IntegerField(
        blank=True,
        null=True
    )
    #criar funcoes para bloquear inscricoes se lotacoes já esticer no numero estabelecido
    def validacao_datas(self):
        if self.fim <= self.inicio:
            raise ValidationError('A data/hora fim deve ser depois da data/hora do inicio.')
    
    def __str__(self):
        return self.titulo
    
class Inscricoes(models.Model):
    participante=models.ForeignKey(
        Participante,
        related_name='inscritos',
        on_delete=models.CASCADE
    )

    evento=models.ForeignKey(
        Eventos,
        related_name='inscricoes',
        on_delete=models.CASCADE
        )
    
    status=models.CharField(
        max_length=1,
        choices=StatusInscricao.choices,
        default=StatusInscricao.PENDENTE
        )
    
    data=models.DateTimeField(auto_now_add=True)
    pago=models.BooleanField(default=False)

    def lotacão_eventos(self):
        total_inscritos=Inscricoes.objects.filter(
            evento=self.evento,
            status=StatusInscricao.CONFIRMADA
        ).count()
        if self.evento.Lotacao>=total_inscritos:
            self.evento.status=Statusevento.EVENTO_LOTADO
        else:
            self.evento.inscritos=total_inscritos
            self.evento.status=Statusevento.EVENTO_ATIVO
        self.save()
    def enviar_email_pendente(self):
        email_participante=self.participante.email

        #inscrição Pendente
        if self.status==StatusInscricao.PENDENTE:
            assunto=f'Inscrição no evento {self.evento.titulo}'
            mensagem=f"""
    Olá {self.participante.nome},

    A sua inscrição no evento "{self.evento.titulo}" foi criada com sucesso.

    Detalhes:
    Evento: {self.evento.titulo}
    Data: {self.evento.fim.date()}
    Local: {self.evento.localizacao}

    Por favor, efetue o pagamento para confirmar a sua vaga.
    Será enviado um link para o pagamento assim que confirmado sua inscrição estará ativa.

    Obrigado!
    """
            if not Email.objects.filter(
                evento=self.evento,
                destinatario=self.participante,
                tipo=TipoEmail.CONFIRMACAO_INSCRICAO,
                enviado=True,
                status=StatusEmail.ENVIADO
            ).exists():
                Email.objects.create(
                    destinatario=self.participante,
                    evento=self.evento,
                    tipo=TipoEmail.CONFIRMACAO_INSCRICAO,
                    assunto=assunto,
                    mensagem=mensagem
                )

            send_mail(
                    assunto,
                    mensagem,
                    settings.EMAIL_HOST_USER,
                    [email_participante],
                    fail_silently=False
            )
            Email.objects.create(
                    destinatario=self.participante,
                    evento=self.evento,
                    tipo=TipoEmail.CONFIRMACAO_INSCRICAO,
                    assunto=assunto,
                    mensagem=mensagem          
            )
            Pagamentos.objects.create(
                    evento=self.evento,
                    participante=self.participante,
                    pago=self.evento.preco,
                    status=StatusPagamento.PENDENTE
            )

    def send_email(self):
        # Apenas enviar email inicial quando inscrição é criada (status PENDENTE)
        if self.status == StatusInscricao.PENDENTE:
            self.enviar_email_pendente()

    
    def __str__(self):
        return f'{self.participante} - {self.evento} ({self.get_status_display()})'
    
class Relatorio(models.Model):
    def save(self, *args, **kwargs):
        if Relatorio.objects.exists() and not self.pk:
            raise ValidationError("Apenas um relatório permitido")
        super().save(*args, **kwargs)

    def total_evento(self):
        total=Eventos.objects.count()
        return total
    
    def total_inscritos(self):
        return Participante.objects.count()
    
    def evento_populares(self):
        evento = Eventos.objects.annotate(
        total_inscritos=Count("inscricoes")
    ).order_by("-total_inscritos").first()
        if evento:
            return evento.titulo
    def evento_sem_inscritos(self):
        eventos = Eventos.objects.filter(inscritos=0)
        return ','.join([evento.titulo for evento in eventos])
    def Faturacao(self):
        total=Pagamentos.objects.filter(status=StatusPagamento.CONCLUIDO).aggregate(total_pago=Sum('pago'))
        return total['total_pago']or 0
    def email_pendentes(self):
        email=Email.objects.filter(status=StatusEmail.PENDENTE).count()
        return email
    def __str__(self):
        return f'Analise de dados'

class Pagamentos(models.Model):
    evento=models.ForeignKey(
        Eventos,
        related_name='pagamentos',
        on_delete=models.CASCADE
    )
    
    participante=models.ForeignKey(
        Participante,
        related_name='pagos',
        on_delete=models.CASCADE
        )
    pago=models.IntegerField()
    status=models.CharField(
        max_length=12,
        choices=StatusPagamento.choices,
        default=StatusPagamento.PENDENTE
    )
    ativo=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.participante}-{self.evento}-{self.pago}$'

class TipoEmail(models.TextChoices):
    CONFIRMACAO_INSCRICAO = "confirmacao_inscricao", "Confirmação de Inscrição"
    EVENTO_CRIADO = "evento_criado", "Evento Criado"
    LEMBRETE = "lembrete", "Lembrete de Evento"
    CANCELAMENTO = "cancelamento", "Cancelamento de Evento"
    REEMBOLSO = "reembolso", "Reembolso do Evento"


class StatusEmail(models.TextChoices):
    PENDENTE = "pendente", "Pendente"
    ENVIADO = "enviado", "Enviado"
    ERRO = "erro", "Erro ao Enviar"


class Email(models.Model):
    destinatario = models.ForeignKey(
        Participante,
        on_delete=models.CASCADE,
        related_name="emails"
    )

    evento = models.ForeignKey(
        Eventos,
        on_delete=models.CASCADE,
        related_name="emails"
    )

    tipo = models.CharField(
        max_length=30,
        choices=TipoEmail.choices
    )

    assunto = models.CharField(
        max_length=150
    )

    mensagem = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=StatusEmail.choices,
        default=StatusEmail.PENDENTE
    )

    data_criacao = models.DateTimeField(
        auto_now_add=True
    )

    enviado=models.BooleanField(default=False)

    tentativas = models.PositiveIntegerField(
        default=0
    )
    
    def save(self, *args,**kwargs,):
        return super().save(*args,**kwargs)

    def __str__(self):
        return f"{self.get_tipo_display()} → {self.destinatario.email} ({self.status})"