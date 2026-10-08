"""
Eventify URL Configuration.

Routes all API endpoints under /api/ prefix.
The Django admin is available at /admin/.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('events.urls')),  # All event API routes
]
