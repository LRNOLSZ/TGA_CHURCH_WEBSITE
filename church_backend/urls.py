"""
URL configuration for church_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from api.views import get_book_price, get_merchandise_price, get_all_currencies

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints for book pricing
    path('api/book/<int:book_id>/price/', get_book_price, name='book_price'),
    
    # API endpoints for merchandise pricing
    path('api/merchandise/<int:merchandise_id>/price/', get_merchandise_price, name='merchandise_price'),
    
    # Currencies list
    path('api/currencies/', get_all_currencies, name='available_currencies'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

