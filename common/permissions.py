from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import timedelta


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
    
class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CanEditWithIn15minutes(BasePermission):
    def has_object_permission(self, request, view, obj):
        time_passed = timezone.now() - obj.created_at
        print("time", time_passed)
        return time_passed <= timedelta(minutes=30)
    

class IsModerator(BasePermission):
    def has_permission(self, request, view):

        if request.method == 'POST':
            return False
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return True


class CustomProductEditPermission(BasePermission):
    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if obj.owner == request.user:
            time_passed = timezone.now() - obj.created_at
            return time_passed <= timedelta(minutes=30)
        return False