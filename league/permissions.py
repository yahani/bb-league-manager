from rest_framework.permissions import BasePermission

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_coach

class IsCoachOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_coach or request.user.is_staff