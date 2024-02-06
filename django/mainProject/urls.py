from django.contrib import admin
from django.urls import path, include

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('mainApp.urls')),
]