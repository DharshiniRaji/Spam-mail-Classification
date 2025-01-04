from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
app_name = 'spam_or_not'

urlpatterns = [
    
    path('login/', login_view, name='login'),
    path('', signup, name='signup'),
    path('home/', home, name='home'),
    
    
    
    
]

