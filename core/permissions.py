from rest_framework.permissions import BasePermission

class IsOrganizador(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'organizador')
    
class IsParticipante(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'participante')