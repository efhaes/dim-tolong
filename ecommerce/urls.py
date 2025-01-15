from django.contrib import admin
from django.urls import path, include  # Tambahkan `include`
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Sertakan URL dari aplikasi store
]

# Tambahkan konfigurasi untuk file media
if settings.DEBUG:  # Hanya aktifkan saat pengembangan
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
