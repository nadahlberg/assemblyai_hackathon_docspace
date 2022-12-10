from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('docspace.app.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

