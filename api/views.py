from django.shortcuts import render
from django.contrib import admin
from django.db.models import Q
from django.http import JsonResponse
from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ImageLog, ContactMessage, Testimony, Book, ExchangeRate
)

def admin_search(request):
    """Search across admin models"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search in various models
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
        
        # If USD, return original price
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
        
        # Get cached exchange rate
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
        from .models import Merchandise
        merchandise = Merchandise.objects.get(id=merchandise_id)
        currency = request.GET.get('currency', 'USD').upper()
        
        # If USD, return original price
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
        
        # Get cached exchange rate
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
