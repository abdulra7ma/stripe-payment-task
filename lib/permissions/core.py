# external imports
from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        if request.user.is_superuser:
            return True

        return view.get_object.customer == request.user
