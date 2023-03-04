def check_access(code, endpoint, method):
    if endpoint == '/api/auth/company/':
        return any([
            True if method == 'GET' and code < 5 else False,
            True if method == 'PUT' and code < 5 else False,
            True if method == 'POST' and code < 5 else False,
            True if method == 'DELETE' and code < 5 else False
        ])
