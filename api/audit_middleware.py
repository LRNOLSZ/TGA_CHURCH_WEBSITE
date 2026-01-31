"""
Middleware to log admin login/logout and capture request context for audit logs
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_login_failed, user_logged_out, user_logged_in
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import AuditLog
import threading


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuditLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to attach request context to the current thread
    so signals can access user IP and user agent
    """
    def process_request(self, request):
        # Store request in thread-local for signals to access
        threading.current_thread().request = request
        return None


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log user login"""
    AuditLog.objects.create(
        user=user,
        action='LOGIN',
        model_name='User',
        object_repr=f'Login: {user.username}',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """Log user logout"""
    if user:
        AuditLog.objects.create(
            user=user,
            action='LOGOUT',
            model_name='User',
            object_repr=f'Logout: {user.username}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    """Log failed login attempts"""
    AuditLog.objects.create(
        user=None,
        action='PERMISSION_DENIED',
        model_name='User',
        object_repr=f'Failed login attempt: {credentials.get("username", "unknown")}',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )


# ====================================================================
# MODEL ACTION SIGNALS - Log CREATE/UPDATE/DELETE for all models
# ====================================================================

def get_request_user():
    """Get current user from request thread-local"""
    try:
        request = threading.current_thread().request
        return request.user if request and request.user.is_authenticated else None
    except AttributeError:
        return None


def get_request_ip():
    """Get client IP from request thread-local"""
    try:
        request = threading.current_thread().request
        return get_client_ip(request) if request else None
    except AttributeError:
        return None


def get_request_user_agent():
    """Get user agent from request thread-local"""
    try:
        request = threading.current_thread().request
        return request.META.get('HTTP_USER_AGENT', '') if request else ''
    except AttributeError:
        return ''


def log_model_action(sender, instance, created, action='UPDATE', **kwargs):
    """
    Generic signal handler for logging model create/update actions
    """
    user = get_request_user()
    if not user:
        return  # Only log if there's an authenticated user
    
    action_type = 'CREATE' if created else 'UPDATE'
    
    AuditLog.objects.create(
        user=user,
        action=action_type,
        model_name=sender.__name__,
        object_id=instance.id,
        object_repr=str(instance),
        ip_address=get_request_ip(),
        user_agent=get_request_user_agent()
    )


def log_model_delete(sender, instance, **kwargs):
    """
    Generic signal handler for logging model delete actions
    """
    user = get_request_user()
    if not user:
        return  # Only log if there's an authenticated user
    
    AuditLog.objects.create(
        user=user,
        action='DELETE',
        model_name=sender.__name__,
        object_id=instance.id,
        object_repr=str(instance),
        ip_address=get_request_ip(),
        user_agent=get_request_user_agent()
    )


# ====================================================================
# REGISTER SIGNALS FOR ALL MODELS
# ====================================================================

# Import all models
from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ImageLog, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
)

# Models to track
TRACKED_MODELS = [
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
]

# Register signals for all tracked models
for model in TRACKED_MODELS:
    post_save.connect(log_model_action, sender=model, dispatch_uid=f'{model.__name__}_post_save')
    post_delete.connect(log_model_delete, sender=model, dispatch_uid=f'{model.__name__}_post_delete')
