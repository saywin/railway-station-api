from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedReadOnlyIsAdminAll(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if (
            request.user
            and request.user.is_authenticated
            and request.method in SAFE_METHODS
        ):
            return True

        return False
