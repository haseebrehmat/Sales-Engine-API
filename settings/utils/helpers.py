def get_host(request):
    host = request.get_host()
    if 'http' not in host:
        host = 'http://' + host
    return host
