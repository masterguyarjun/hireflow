from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('user_accounts.urls')),
    path('jobs/', include('job_listings.urls')),
    path('applications/', include('job_applications.urls')),
    path('companies/', include('company_profiles.urls')),
    path('dashboard/', include('user_dashboard.urls')),
    path('', include('user_dashboard.urls')),  # Homepage
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)