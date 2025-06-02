from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feedback.urls')),  # Delegates routing to app-level
]
