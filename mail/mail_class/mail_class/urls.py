
from django.contrib import admin
from django.urls import path,include



urlpatterns = [
    path('',include('spam_or_not.urls')),
    path("admin/", admin.site.urls),

    
]
