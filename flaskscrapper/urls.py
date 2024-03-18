from .views import FlaskResponse
from django.urls import path
urlpatterns = [
    path('flask-response/', FlaskResponse.as_view())
]
