from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import render
from django.contrib import admin
from django.http import JsonResponse

from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ImageLog, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
)
from .serializers import (
    HomeBannerSerializer, ChurchInfoSerializer, HeadPastorSerializer, ServiceTimeSerializer,
    LeaderSerializer, PhotoGallerySerializer, SermonSerializer, EventSerializer,
    BranchSerializer, GivingInfoSerializer, GivingImageSerializer,
    ContactMessageSerializer, TestimonySerializer, BookSerializer,
    MerchandiseSerializer, ExchangeRateSerializer, ImageLogSerializer
)


# ====================================================================
# PAGINATION
# ====================================================================

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ====================================================================
# HOME PAGE VIEWSETS
# ====================================================================

class HomeBannerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing home page banners.
    
    Query params:
    - is_active: Filter by active status (true/false)
    - search: Search in title and subtitle
    """
    queryset = HomeBanner.objects.all()
    serializer_class = HomeBannerSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'subtitle']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    
    def get_queryset(self):
        queryset = HomeBanner.objects.all()
        is_active = self.request.query_params.get('is_active', None)
        
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset


class ChurchInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for church information (singleton).
    Only retrieves the single ChurchInfo record.
    """
    queryset = ChurchInfo.objects.all()
    serializer_class = ChurchInfoSerializer
    
    def get_queryset(self):
        # Return only one record
        return ChurchInfo.objects.all()[:1]


class HeadPastorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for head pastor information (singleton).
    Only retrieves the single HeadPastor record.
    """
    queryset = HeadPastor.objects.all()
    serializer_class = HeadPastorSerializer
    
    def get_queryset(self):
        # Return only one record
        return HeadPastor.objects.all()[:1]


class ServiceTimeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing service times.
    
    Query params:
    - day: Filter by day of week
    - branch_id: Filter by branch
    - is_active: Filter by active status
    """
    queryset = ServiceTime.objects.all()
    serializer_class = ServiceTimeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['day', 'time']
    
    def get_queryset(self):
        queryset = ServiceTime.objects.all()
        day = self.request.query_params.get('day', None)
        branch_id = self.request.query_params.get('branch_id', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if day:
            queryset = queryset.filter(day=day)
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        return queryset


# ====================================================================
# ABOUT US VIEWSETS
# ====================================================================

class LeaderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing church leadership.
    
    Query params:
    - position: Filter by role
    - featured: Filter featured leaders only
    - search: Search by name
    """
    queryset = Leader.objects.all()
    serializer_class = LeaderSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'position']
    ordering_fields = ['order', 'position']
    ordering = ['order', 'position']
    
    def get_queryset(self):
        queryset = Leader.objects.all()
        featured = self.request.query_params.get('featured', None)
        position = self.request.query_params.get('position', None)
        
        if featured is not None:
            featured = featured.lower() == 'true'
            queryset = queryset.filter(is_featured_on_home=featured)
        if position:
            queryset = queryset.filter(position=position)
        
        return queryset


class PhotoGalleryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing photo gallery.
    
    Query params:
    - category: Filter by category
    - search: Search by title or caption
    """
    queryset = PhotoGallery.objects.all()
    serializer_class = PhotoGallerySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'caption']
    ordering_fields = ['uploaded_at', 'category']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        queryset = PhotoGallery.objects.all()
        category = self.request.query_params.get('category', None)
        
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset


# ====================================================================
# SERMONS VIEWSET
# ====================================================================

class SermonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sermons/messages.
    
    Query params:
    - speaker: Filter by speaker
    - series: Filter by series
    - published: Filter by publication status
    - featured: Filter featured sermons only
    - search: Search by title
    """
    queryset = Sermon.objects.all()
    serializer_class = SermonSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'speaker', 'series']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date', '-created_at']
    
    def get_queryset(self):
        queryset = Sermon.objects.all()
        speaker = self.request.query_params.get('speaker', None)
        series = self.request.query_params.get('series', None)
        published = self.request.query_params.get('published', None)
        featured = self.request.query_params.get('featured', None)
        
        if speaker:
            queryset = queryset.filter(speaker__icontains=speaker)
        if series:
            queryset = queryset.filter(series=series)
        if published is not None:
            published = published.lower() == 'true'
            queryset = queryset.filter(is_published=published)
        if featured is not None:
            featured = featured.lower() == 'true'
            queryset = queryset.filter(is_featured=featured)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured sermons"""
        sermons = self.get_queryset().filter(is_featured=True)[:5]
        serializer = self.get_serializer(sermons, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest sermon"""
        sermon = self.get_queryset().first()
        if sermon:
            serializer = self.get_serializer(sermon)
            return Response(serializer.data)
        return Response({'detail': 'No sermons found'}, status=status.HTTP_404_NOT_FOUND)


# ====================================================================
# EVENTS VIEWSET
# ====================================================================

class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing church events.
    
    Query params:
    - category: Filter by category
    - branch_id: Filter by branch
    - active: Filter by active status
    - featured: Filter featured events only
    - search: Search by title
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at']
    ordering = ['date']
    
    def get_queryset(self):
        queryset = Event.objects.all()
        category = self.request.query_params.get('category', None)
        branch_id = self.request.query_params.get('branch_id', None)
        active = self.request.query_params.get('active', None)
        featured = self.request.query_params.get('featured', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if active is not None:
            active = active.lower() == 'true'
            queryset = queryset.filter(is_active=active)
        if featured is not None:
            featured = featured.lower() == 'true'
            queryset = queryset.filter(is_featured=featured)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        from django.utils import timezone
        events = self.get_queryset().filter(
            date__gte=timezone.now(),
            is_active=True
        )[:10]
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured events"""
        events = self.get_queryset().filter(is_featured=True)[:5]
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


# ====================================================================
# BRANCHES VIEWSET
# ====================================================================

class BranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing church branches.
    
    Query params:
    - main: Filter main branch (true/false)
    - search: Search by name or location
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'location']
    ordering_fields = ['is_main_branch', 'name']
    ordering = ['-is_main_branch', 'name']
    
    def get_queryset(self):
        queryset = Branch.objects.all()
        main = self.request.query_params.get('main', None)
        
        if main is not None:
            main = main.lower() == 'true'
            queryset = queryset.filter(is_main_branch=main)
        
        return queryset


# ====================================================================
# GIVING/DONATIONS VIEWSETS
# ====================================================================

class GivingImageViewSet(viewsets.ModelViewSet):
    """ViewSet for giving page images"""
    queryset = GivingImage.objects.all()
    serializer_class = GivingImageSerializer
    pagination_class = StandardResultsSetPagination


class GivingInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for giving page content (singleton).
    """
    queryset = GivingInfo.objects.all()
    serializer_class = GivingInfoSerializer
    
    def get_queryset(self):
        # Return only one record
        return GivingInfo.objects.all()[:1]


# ====================================================================
# CONTACT/MESSAGES VIEWSETS
# ====================================================================

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing contact form submissions.
    
    Query params:
    - subject: Filter by subject
    - is_read: Filter by read status
    - search: Search by name or message
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        queryset = ContactMessage.objects.all()
        subject = self.request.query_params.get('subject', None)
        is_read = self.request.query_params.get('is_read', None)
        
        if subject:
            queryset = queryset.filter(subject=subject)
        if is_read is not None:
            is_read = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'Message marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread messages"""
        messages = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


class TestimonyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing testimonies.
    
    Query params:
    - carousel: Filter carousel testimonies
    - approved: Filter approved testimonies
    - category: Filter by category
    - search: Search by name or text
    """
    queryset = Testimony.objects.all()
    serializer_class = TestimonySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'testimony_text', 'category']
    ordering_fields = ['order', 'created_at']
    ordering = ['order', '-created_at']
    
    def get_queryset(self):
        queryset = Testimony.objects.all()
        carousel = self.request.query_params.get('carousel', None)
        approved = self.request.query_params.get('approved', None)
        category = self.request.query_params.get('category', None)
        
        if carousel is not None:
            carousel = carousel.lower() == 'true'
            queryset = queryset.filter(show_on_carousel=carousel)
        if approved is not None:
            approved = approved.lower() == 'true'
            queryset = queryset.filter(is_approved=approved)
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def carousel(self, request):
        """Get testimonies for carousel display"""
        testimonies = self.get_queryset().filter(show_on_carousel=True)
        serializer = self.get_serializer(testimonies, many=True)
        return Response(serializer.data)


# ====================================================================
# PRODUCTS VIEWSETS
# ====================================================================

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.
    
    Query params:
    - available: Filter available books
    - search: Search by name or description
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Book.objects.all()
        available = self.request.query_params.get('available', None)
        
        if available is not None:
            available = available.lower() == 'true'
            queryset = queryset.filter(is_available=available)
        
        return queryset


class MerchandiseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing merchandise.
    
    Query params:
    - available: Filter available items
    - search: Search by name or description
    """
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Merchandise.objects.all()
        available = self.request.query_params.get('available', None)
        
        if available is not None:
            available = available.lower() == 'true'
            queryset = queryset.filter(is_available=available)
        
        return queryset


class ExchangeRateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for exchange rates.
    
    Query params:
    - currency_code: Filter by currency code
    """
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['currency_code']
    
    def get_queryset(self):
        queryset = ExchangeRate.objects.all()
        currency_code = self.request.query_params.get('currency_code', None)
        
        if currency_code:
            queryset = queryset.filter(currency_code__icontains=currency_code)
        
        return queryset


# ====================================================================
# LOGS VIEWSETS
# ====================================================================

class ImageLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnly ViewSet for image logs.
    
    Query params:
    - section_name: Filter by section
    - search: Search by section name
    """
    queryset = ImageLog.objects.all()
    serializer_class = ImageLogSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['section_name']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def get_queryset(self):
        queryset = ImageLog.objects.all()
        section_name = self.request.query_params.get('section_name', None)
        
        if section_name:
            queryset = queryset.filter(section_name__icontains=section_name)
        
        return queryset


# ====================================================================
# LEGACY HELPER VIEWS
# ====================================================================

def admin_search(request):
    """Search across admin models"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        banners = HomeBanner.objects.filter(title__icontains=query)
        leaders = Leader.objects.filter(full_name__icontains=query)
        sermons = Sermon.objects.filter(title__icontains=query)
        events = Event.objects.filter(title__icontains=query)
        branches = Branch.objects.filter(name__icontains=query)
        messages = ContactMessage.objects.filter(
            Q(name__icontains=query) | Q(subject__icontains=query)
        )
        testimonies = Testimony.objects.filter(
            Q(name__icontains=query) | Q(testimony_text__icontains=query)
        )
        
        results = {
            'banners': banners,
            'leaders': leaders,
            'sermons': sermons,
            'events': events,
            'branches': branches,
            'messages': messages,
            'testimonies': testimonies,
        }
    
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'admin/search.html', context)


def get_book_price(request, book_id):
    """
    Get book price converted to selected currency.
    Query params: currency (e.g., ?currency=GHS)
    """
    try:
        book = Book.objects.get(id=book_id)
        currency = request.GET.get('currency', 'USD').upper()
        
        if currency == 'USD':
            return JsonResponse({
                'success': True,
                'book_id': book.id,
                'name': book.name,
                'original_price': float(book.price),
                'converted_price': float(book.price),
                'currency': 'USD',
                'currency_code': 'USD'
            })
        
        try:
            exchange_rate = ExchangeRate.objects.get(currency_code=currency)
            converted_price = float(book.price) * float(exchange_rate.rate)
            
            return JsonResponse({
                'success': True,
                'book_id': book.id,
                'name': book.name,
                'original_price': float(book.price),
                'converted_price': round(converted_price, 2),
                'currency': exchange_rate.currency_name,
                'currency_code': currency,
                'exchange_rate': float(exchange_rate.rate),
                'last_updated': exchange_rate.last_updated.isoformat()
            })
        except ExchangeRate.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Currency {currency} not found in database',
                'available_currencies': list(
                    ExchangeRate.objects.values_list('currency_code', flat=True)
                )
            }, status=404)
            
    except Book.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Book with ID {book_id} not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_merchandise_price(request, merchandise_id):
    """
    Get merchandise price converted to selected currency.
    Query params: currency (e.g., ?currency=GHS)
    """
    try:
        merchandise = Merchandise.objects.get(id=merchandise_id)
        currency = request.GET.get('currency', 'USD').upper()
        
        if currency == 'USD':
            return JsonResponse({
                'success': True,
                'merchandise_id': merchandise.id,
                'name': merchandise.name,
                'original_price': float(merchandise.price),
                'converted_price': float(merchandise.price),
                'currency': 'USD',
                'currency_code': 'USD'
            })
        
        try:
            exchange_rate = ExchangeRate.objects.get(currency_code=currency)
            converted_price = float(merchandise.price) * float(exchange_rate.rate)
            
            return JsonResponse({
                'success': True,
                'merchandise_id': merchandise.id,
                'name': merchandise.name,
                'original_price': float(merchandise.price),
                'converted_price': round(converted_price, 2),
                'currency': exchange_rate.currency_name,
                'currency_code': currency,
                'exchange_rate': float(exchange_rate.rate),
                'last_updated': exchange_rate.last_updated.isoformat()
            })
        except ExchangeRate.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Currency {currency} not found in database',
                'available_currencies': list(
                    ExchangeRate.objects.values_list('currency_code', flat=True)
                )
            }, status=404)
            
    except Merchandise.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': f'Merchandise with ID {merchandise_id} not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_all_currencies(request):
    """Get list of all available currencies for conversion"""
    currencies = ExchangeRate.objects.values('currency_code', 'currency_name').order_by('currency_code')
    return JsonResponse({
        'success': True,
        'currencies': list(currencies),
        'count': len(list(currencies))
    })
