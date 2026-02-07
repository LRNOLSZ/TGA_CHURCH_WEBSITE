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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from api.views import (
    HomeBannerViewSet, ChurchInfoViewSet, HeadPastorViewSet, ServiceTimeViewSet,
    LeaderViewSet, PhotoGalleryViewSet, SermonViewSet, EventViewSet,
    BranchViewSet, GivingImageViewSet, GivingInfoViewSet,
    ContactMessageViewSet, TestimonyViewSet, BookViewSet,
    MerchandiseViewSet, ExchangeRateViewSet, ImageLogViewSet,
    get_book_price, get_merchandise_price, get_all_currencies
)

# Initialize DRF router
router = DefaultRouter()
router.register(r'banners', HomeBannerViewSet, basename='banner')
router.register(r'church-info', ChurchInfoViewSet, basename='church-info')
router.register(r'head-pastor', HeadPastorViewSet, basename='head-pastor')
router.register(r'service-times', ServiceTimeViewSet, basename='service-time')
router.register(r'leaders', LeaderViewSet, basename='leader')
router.register(r'gallery', PhotoGalleryViewSet, basename='photo')
router.register(r'sermons', SermonViewSet, basename='sermon')
router.register(r'events', EventViewSet, basename='event')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'giving-images', GivingImageViewSet, basename='giving-image')
router.register(r'giving-info', GivingInfoViewSet, basename='giving-info')
router.register(r'contact-messages', ContactMessageViewSet, basename='contact-message')
router.register(r'testimonies', TestimonyViewSet, basename='testimony')
router.register(r'books', BookViewSet, basename='book')
router.register(r'merchandise', MerchandiseViewSet, basename='merchandise')
router.register(r'exchange-rates', ExchangeRateViewSet, basename='exchange-rate')
router.register(r'image-logs', ImageLogViewSet, basename='image-log')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # REST API endpoints
    path('api/', include(router.urls)),
    
    # Legacy pricing endpoints
    path('api/book/<int:book_id>/price/', get_book_price, name='book_price'),
    path('api/merchandise/<int:merchandise_id>/price/', get_merchandise_price, name='merchandise_price'),
    path('api/currencies/', get_all_currencies, name='available_currencies'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


