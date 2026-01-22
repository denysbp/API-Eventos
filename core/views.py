from .serializers import RelatorioSerializers,EmailSerializers,EventosSerializers,PagamentosSerializers,ParticipanteSerializer,IncricoesSerialiers,OrganizadorSerializers,InscricaoEventoSerializer
from .models import Relatorio,Inscricoes,Email,Pagamentos,Participante,Organizador,Eventos,Statusevento,StatusInscricao,StatusPagamento
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import IsOrganizador,IsParticipante
from django.db.models import F
from django.db import transaction
from django.core.management import call_command

#criar usuarios de tipos diferentes
class CriarParticipanteAPIView(APIView):
    def post(self,request):
        serializer=ParticipanteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class CriarOrganizadorAPIView(APIView):
    def post(self,request):
        serializer=OrganizadorSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class RelatorioAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def get(self,request):
        relatorio=Relatorio.objects.all()
        serializer=RelatorioSerializers(relatorio,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer=RelatorioSerializers(data=request.data)
        #transaction.atomic para evitar race conditions(duas requisicoes ao mesmo tempo)
        with transaction.atomic():
            if Relatorio.objects.exists():
                return Response(
                    {'erro':'Apenas é permitido um relatorio no banco de dados'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class CriarEventosAPIViews(APIView):
    permission_classes=[IsOrganizador]
    def post(self,request):
        serializer=EventosSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizador=request.user.organizador)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class VerEventosAPIViwes(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        eventos=Eventos.objects.all()
        serializer=EventosSerializers(eventos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class VereventoAPIView(APIView):
    permission_classes=[IsAuthenticated,IsParticipante]
    def get(self,request,evento_id):
        evento=get_object_or_404(Eventos,id=evento_id)
        serializer=EventosSerializers(evento)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class VerEventosIncritosAPIView(APIView):
    permission_classes=[IsAuthenticated,IsParticipante]
    def get(self,request):
        participante=request.user.participante
        inscricoes = Inscricoes.objects.filter(participante=participante).select_related('evento')
        serializer = InscricaoEventoSerializer(inscricoes, many=True)
        return Response(serializer.data)


class VerOrganizadorInscricoesAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def get(self,request,evento_id):
        evento=Eventos.objects.get(id=evento_id,organizador=request.user.organizador)
        inscricoes=Inscricoes.objects.filter(evento=evento).select_related('participante')

        dados=inscricoes.values(
            'participante',
            'status',
            'pago',
            'data'
        )
        return Response({
            'Evento': evento.titulo,
            'total_inscritos': inscricoes.count(),
            'inscritos': list(dados)
        },status=status.HTTP_200_OK)
    
class VerMeusEventosAPIViews(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def get(self,request):
        organizador=request.user.organizador
        eventos=Eventos.objects.filter(organizador=organizador)
        serializer=EventosSerializers(eventos,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        

class InscreverAPIView(APIView):
    permission_classes=[IsAuthenticated,IsParticipante]
    def post(self,request,evento_id):
        evento=get_object_or_404(Eventos,id=evento_id)
        participante=request.user.participante
        if evento.status!=Statusevento.EVENTO_ATIVO:
            return Response({
                'erro':'Você não pode se inscrever neste curso pq ele já não se encontra ativo,ou já foi concluido'
            },status=status.HTTP_400_BAD_REQUEST)
        if Inscricoes.objects.filter(evento=evento,participante=participante).exists():
            return Response(
                {'erro':'Você já está inscrito neste curso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Inscricoes.objects.filter(
            evento=evento,
            status=StatusInscricao.CONFIRMADA
        ).count() >= evento.Lotacao:
            evento.status=Statusevento.EVENTO_LOTADO
            evento.save()
            return Response({
                'erro':'Este evento está lotado, não é possivel fazer a inscrição'
            },status=status.HTTP_400_BAD_REQUEST)
        serializer=IncricoesSerialiers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(participante=participante,evento=evento)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class PerfilAPIView(APIView):
    def get(self,request):
        user=request.user
        if hasattr(user,'participante'):
            participante=user.participante
            serializer=ParticipanteSerializer(participante)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        if hasattr(user,'organizador'):
            organizador=user.organizador
            serializer=OrganizadorSerializers(organizador)
            return Response(serializer.data,status=status.HTTP_200_OK)
class ListarEmailsAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def get(self,request,evento_id):
        organizador=request.user.organizador
        evento=get_object_or_404(Eventos,id=evento_id,organizador=organizador)
        email=Email.objects.filter(
            evento=evento,
        )
        try:
            with transaction.atomic():
                serializer=EmailSerializers(email,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({
                'erro':f'ocorreu um erro {str(e)}'
            })
class InscricaoConfirmadaAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def put(self,request,inscricao_id):
        inscricao=get_object_or_404(Inscricoes,id=inscricao_id)
        evento=inscricao.evento
        organizador=request.user.organizador
        if evento.organizador != organizador:
            return Response(
                {'erro':'Você não pode confirmar inscrições de eventos que não são seus'},
                status=status.HTTP_403_FORBIDDEN
            )
        if inscricao.status == StatusInscricao.CONFIRMADA:
            return Response(
                {'erro':'Esta inscrição já está confirmada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            try:
                inscricao.status=StatusInscricao.CONFIRMADA
                inscricao.pago=True
                inscricao.save()
                return Response(
                    {'sucesso':'Inscrição confirmada com sucesso'},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response({
                    'erro': 'Não foi possivel confirmar a inscrição','detalhe':str(e)
                },status=status.HTTP_400_BAD_REQUEST)

class CancelarInscricaoAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def put(self,request,inscricao_id):
        inscricao=get_object_or_404(Inscricoes,id=inscricao_id)
        evento=inscricao.evento
        organizador=request.user.organizador
        if evento.organizador != organizador:
            return Response(
                {'erro':'Você não pode cancelar inscrições de eventos que não são seus'},
                status=status.HTTP_403_FORBIDDEN
            )
        if inscricao.status == StatusInscricao.CANCELADA:
            return Response(
                {'erro':'Esta inscrição já está cancelada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            with transaction.atomic():
                inscricao.status=StatusInscricao.CANCELADA
                inscricao.pago=False
                inscricao.save()
                return Response(
                    {'sucesso':'Inscrição cancelada com sucesso'},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response({
                'erro':'Ocorreu um erro ao cancelar a inscricão','detalhe':str(e)
            },status=status.HTTP_400_BAD_REQUEST)

class ReembolsarInscricaoAPIView(APIView):
    permission_classes=[IsAuthenticated,IsOrganizador]
    def put(self,request,inscricao_id):
        inscricao=get_object_or_404(Inscricoes,id=inscricao_id)
        evento=inscricao.evento
        organizador=request.user.organizador

        if evento.organizador !=organizador:
            return Response({
                'erro':'Você não pode reembolsar uma incrição que não é sua'
            },status=status.HTTP_403_FORBIDDEN)
        elif inscricao.status==StatusInscricao.REEMBOLSADO:
            return Response({
                'erro':'Essa inscrição já se encontra reembolsada'
            })
        try:
            with transaction.atomic():
                inscricao.status=StatusInscricao.REEMBOLSADO
                inscricao.pago=False
                inscricao.save()
                call_command('atualizar_pagamentos')
                return Response({
                    'sucesso':'Inscrição reembolsada com sucesso'
                },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'erro':'Ocorreu um erro ao processar o reembolso:','detalhe':str(e)
            },status=status.HTTP_400_BAD_REQUEST)


#api de pagamento improvisada
class PagamentosAPIView(APIView):
    permission_classes=[IsAuthenticated,IsParticipante]
    def put(self, request, pagamento_id):
        """
        Confirma o pagamento e atualiza todo o fluxo:
        1. Marca pagamento como CONCLUIDO e ativo
        2. Atualiza inscrição para CONFIRMADA e pago=True
        3. Envia emails de confirmação
        4. Executa comando de atualizar pagamentos
        """
        pagamento = get_object_or_404(Pagamentos, id=pagamento_id)
        participante = request.user.participante
        
        if pagamento.participante != participante:
            return Response(
                {'erro': 'Você não pode confirmar um pagamento que não é seu'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validar se já foi pago
        if pagamento.status == StatusPagamento.CONCLUIDO:
            return Response(
                {'erro': 'Este pagamento já foi confirmado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                # 1. Atualizar pagamento
                pagamento.status = StatusPagamento.CONCLUIDO
                pagamento.ativo = True
                pagamento.save()
                
                # 2. Atualizar inscrição
                inscricao = Inscricoes.objects.get(
                    evento=pagamento.evento,
                    participante=participante
                )
                inscricao.status = StatusInscricao.CONFIRMADA
                inscricao.pago = True
                inscricao.save()
                
                # 3. Enviar email de confirmação
                inscricao.enviar_email_confirmado()
                
                # 4. Executar comando de atualizar pagamentos
                call_command('atualizar_pagamentos')
                
                return Response(
                    {
                        'sucesso': 'Pagamento confirmado com sucesso!',
                        'pagamento': {
                            'id': pagamento.id,
                            'status': pagamento.status,
                            'ativo': pagamento.ativo,
                            'pago': pagamento.pago
                        },
                        'inscricao': {
                            'id': inscricao.id,
                            'status': inscricao.status,
                            'pago': inscricao.pago
                        }
                    },
                    status=status.HTTP_200_OK
                )
        
        except Inscricoes.DoesNotExist:
            return Response(
                {'erro': 'Inscrição não encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'erro': f'Erro ao processar pagamento: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
