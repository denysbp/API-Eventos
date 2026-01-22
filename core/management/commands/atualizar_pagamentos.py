from django.core.management.base import BaseCommand
from core.models import Inscricoes, Pagamentos, StatusInscricao, StatusPagamento


class Command(BaseCommand):
    help = 'Atualiza status dos pagamentos baseado no status das inscrições'

    def handle(self, *args, **options):
        total_atualizados = 0
        
        # Atualizar inscrições CONFIRMADAS
        inscricoes_confirmadas = Inscricoes.objects.filter(
            status=StatusInscricao.CONFIRMADA
        )
        count_confirmadas = inscricoes_confirmadas.count()
        for inscricao in inscricoes_confirmadas:
            updated = Pagamentos.objects.filter(
                evento=inscricao.evento,
                participante=inscricao.participante
            ).update(
                status=StatusPagamento.CONCLUIDO,
                ativo=True
            )
            total_atualizados += updated
        # self.stdout.write(f'Inscrições CONFIRMADAS: {count_confirmadas}')

        # Atualizar inscrições CANCELADAS
        inscricoes_canceladas = Inscricoes.objects.filter(
            status=StatusInscricao.CANCELADA
        )
        count_canceladas = inscricoes_canceladas.count()
        for inscricao in inscricoes_canceladas:
            updated = Pagamentos.objects.filter(
                evento=inscricao.evento,
                participante=inscricao.participante
            ).update(
                status=StatusPagamento.CANCELADO,
                ativo=False
            )
            total_atualizados += updated
        # self.stdout.write(f'Inscrições CANCELADAS: {count_canceladas}')

        # Atualizar inscrições REEMBOLSADAS
        inscricoes_reembolsadas = Inscricoes.objects.filter(
            status=StatusInscricao.REEMBOLSADO
        )
        count_reembolsadas = inscricoes_reembolsadas.count()
        for inscricao in inscricoes_reembolsadas:
            updated = Pagamentos.objects.filter(
                evento=inscricao.evento,
                participante=inscricao.participante
            ).update(
                status=StatusPagamento.REEMBOLSADO,
                ativo=False
            )
            total_atualizados += updated
        # self.stdout.write(f'Inscrições REEMBOLSADAS: {count_reembolsadas}')

        # self.stdout.write(self.style.SUCCESS(f'Total de pagamentos atualizados: {total_atualizados}'))
