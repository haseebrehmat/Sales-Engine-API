from .views import JobsPoster
from django.urls import path
urlpatterns = [
    path('post-jobs/', JobsPoster.as_view())
]
