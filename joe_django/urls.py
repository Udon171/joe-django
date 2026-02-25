"""
URL configuration for joe_django project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('gallery/', include('gallery.urls')),
    path('shop/', include('shop.urls')),
    path('commissions/', include('commissions.urls')),
    path('account/', include('users.urls')),
    path('', include('home.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
