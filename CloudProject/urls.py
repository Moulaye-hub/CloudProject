from functools import partial
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include

app_name = 'CloudProjectApp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CloudProjectApp.urls')),
]

handler404 = 'CloudProjectApp.views.error_404'

if settings.DEBUG:
    urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, 'FORCE_SERVE_STATIC', False):
    settings.DEBUG = True
    urlpatterns += static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
    urlpatterns += static(
            settings.STATIC_URL, document_root=settings.STATIC_ROOT
          )
    settings.DEBUG = False
    
