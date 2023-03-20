from django.urls import path
from job_scraper.views.job_view import JobView

urlpatterns = [
  path('jobs', JobView.get, name="jobs"),
]

scheduler.start()
