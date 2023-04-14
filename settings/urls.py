from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/job_portal/', include('job_portal.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/job_scraper/', include("job_scraper.urls")),
    path('api/profile/', include("pseudos.urls")),
    path('api/error_logger/', include("error_logger.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

