from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/job_portal/', include('job_portal.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/job_scraper/', include("scraper.urls")),
    path('api/profile/', include("pseudos.urls")),
    path('api/error_logger/', include("error_logger.urls")),
    path('api/lead_managament/', include("lead_management.urls")),
    path('api/candidate_management/', include("candidate.urls")),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

