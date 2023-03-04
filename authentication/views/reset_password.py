from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from authentication.models import ResetPassword
from settings.base import REACT_APP_URL


def render_reset_page(request, email, code):
    try:
        queryset = ResetPassword.objects.get(reset_code=code)
    except ResetPassword.DoesNotExist:
        return HttpResponse({'detail':"<h1 align='center'>Reset code doesn't exist</h1>"})
    expiry_time = queryset.updated_at + timedelta(hours=24)
    current_time = timezone.now()
    if current_time > expiry_time or queryset.status:
        return HttpResponse({'detail': "<h1 align='center'>Reset link expired!</h1>"})
    return redirect(f"{REACT_APP_URL}/reset-password?email={email}&code={code}")
