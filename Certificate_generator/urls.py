"""
URL configuration for Certificate_generator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Certificate_generator import views
from Certificate_generator import test

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', views.homepage, name='homepage'),
    path('', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('generate_certificate/', views.generate_certificate, name='generate_certificate'),
    path('mail-status/', views.mail_status, name='mail_status'),
    path('create_event/', views.create_event, name='create_event'),
    path('events/', views.event_list, name='event_list'),
    path('participate/<int:event_id>/', views.participate_event, name='participate_event'),
    path('event_participants/<int:event_id>/', views.event_participants, name='event_participants'),  # Add this line
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('user_profile_view/', views.user_profile_view, name='user_profile_view'),
    path('api/', include('Certificate_generator.api.api_urls')),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
