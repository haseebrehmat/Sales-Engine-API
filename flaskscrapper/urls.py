from .views.job_post_view import JobsPoster
from .views.job_start_view import JobsStart
from django.urls import path

urlpatterns = [
    path('post-jobs/', JobsPoster.as_view(), name='post_job'),
    path('start-job/<job_source>/', JobsStart.as_view(), name='start_job')
]
