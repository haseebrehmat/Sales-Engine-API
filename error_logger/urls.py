from django.urls import path
from . import views

urlpatterns = [
    path('error_logs/', views.LogsView.as_view()),
]
