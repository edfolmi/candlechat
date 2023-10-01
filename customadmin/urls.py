from django.urls import path
from .admin import custom_admin_site

urlpatterns = [
    path('', custom_admin_site.urls)
]