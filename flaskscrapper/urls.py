from .views import FlaskScrapper, FlaskResponse
from django.urls import path
urlpatterns = [
    path('flask-scrapper/', FlaskScrapper.as_view()),
    path('flask-response/', FlaskResponse.as_view())
]
