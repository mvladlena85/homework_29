from rest_framework import permissions

from ads.models import Ads


class IsSelectionOwner(permissions.BasePermission):
    message = "Вы не можете редактировать эту подборку"

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.owner:
            return True
        return False


class IsAdOwnerOrStaff(permissions.BasePermission):
    message = "Вы не можете редактировать это объявление"

    def has_permission(self, request, view):
        ad = Ads.objects.get(id=view.kwargs.get('pk'))
        if request.user == ad.author or request.user.role in ['moderator', 'admin']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in ['moderator', 'admin']:
            return True
        return False

