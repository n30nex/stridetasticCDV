from ninja_extra.permissions import BasePermission


class IsPrivilegedUser(BasePermission):
    message = "You do not have permission to perform this action."

    def has_permission(self, request, controller) -> bool:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_authenticated", False):
            return False
        return bool(getattr(user, "is_staff", False) or getattr(user, "is_superuser", False))
