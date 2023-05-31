import re
import uuid


def get_host(request):
    host = request.get_host()
    if 'http' not in host:
        host = 'http://' + host
    return host


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def validate_password(password):
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    return re.match(password_pattern, password)


def serializer_errors(serializer):
    try:
        fields = list(serializer.errors.keys())
        data = [x + ": " + serializer.errors[x][0] for x in fields]
        data = "\n".join(data)
        return data
    except:
        return serializer.errors
