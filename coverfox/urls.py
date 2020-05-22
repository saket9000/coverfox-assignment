"""coverfox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from keys import views as keys_views 

urlpatterns = [
	path('admin/', admin.site.urls),
	path('key/generate-key/', keys_views.generate_key, name='generate_key'),
	path('key/get-available-key/', keys_views.get_available_key, name='get_available_key'),
	path('key/unblock-key/<uuid:key>/', keys_views.unblock_key, name='unblock_key'),
	path('key/delete-key/<uuid:key>/', keys_views.delete_key, name='delete_key'),
	path('key/keep-key-alive/<uuid:key>/', keys_views.keep_key_alive, name='keep_key_alive')
]
