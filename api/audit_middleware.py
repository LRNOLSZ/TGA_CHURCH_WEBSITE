"""
Middleware to log admin login/logout and capture request context for audit logs
"""
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.signals import user_login_failed, user_logged_out, user_logged_in
from django.dispatch import receiver
from .models import AuditLog


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
        import threading
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
