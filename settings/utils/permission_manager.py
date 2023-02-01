from rest_framework.permissions import BasePermission


class UserPermissions(BasePermission):
    message = "You don't have access to this endpoint!"
    read_user_permissions = [
        "authentication.view_user",
    ]
    write_user_permissions = read_user_permissions + [
        "authentication.change_user",
        "authentication.delete_user",
        "authentication.add_user"
    ]

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif not request.user.is_superuser:
            if request.method == "GET":
                return request.user.has_perms(self.read_user_permissions)
            elif request.method in ["POST", "PUT", "DELETE"]:
                return request.user.has_perms(self.write_user_permissions)
            return False
        else:
            return False

