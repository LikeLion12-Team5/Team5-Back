from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class OnlyRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        else:
            return False