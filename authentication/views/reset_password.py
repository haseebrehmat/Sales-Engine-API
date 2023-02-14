from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from authentication.models import ResetPassword


def render_reset_page(request, email, code):
    queryset = ResetPassword.objects.get(reset_code=code)
    expiry_time = queryset.updated_at + timedelta(hours=24)
    current_time = timezone.now()
    if current_time > expiry_time:
        return HttpResponse("<h1>Reset link expired!</h1>")
    return render(request, "reset_password.html", {"email": email, "code": code})
