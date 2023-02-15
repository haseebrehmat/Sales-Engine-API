from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/job_portal/', include('job_portal.urls')),
    path('api/dashboard/', include('dashboard.urls'))
]
