def validate_request(request, permissions):
    try:
        user_permissions = request.user.roles.permissions.values_list("codename", flat=True)
    except Exception as e:
        return False
    if request.method in permissions.keys():
        if permissions[request.method] is not None:
            for perm in permissions[request.method]:
                if perm in user_permissions:
                    return True
    return False
