from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaff(BasePermission):
    """
    Permissions that will check if user has rights over the object before editing/deleting it
    It will still allow access to staff members
    [ref] https://testdriven.io/blog/custom-permission-classes-drf/
    """

    message = "User has no rights over this object."  # custom error message

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.user == obj.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
