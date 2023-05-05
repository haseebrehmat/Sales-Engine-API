from error_logger.models import Log
from django.utils import timezone

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


def saveLogs(error, level='ERROR', request=None):
    path = None
    line_number = None
    error_message = None
    traceback_log = None
    error_line = None
    method = None
    status_code = None
    user_id = None
    if request:
        if hasattr(request, 'user') and request.user.is_authenticated:
            user_id = request.user
    log = Log(
        user_id=user_id,
        level=level,
        log_message=error,
        error_message=error_message,
        error_line=error_line,
        traceback=traceback_log,
        path=path,
        line_number=line_number,
        method=method,
        status_code=status_code,
        time=timezone.now()
    )
    log.save()
