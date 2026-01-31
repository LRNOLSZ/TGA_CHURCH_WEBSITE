"""
Admin action logging middleware and signals
Automatically logs all admin create/update/delete actions
"""
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import AuditLog
from django.contrib.auth.models import User


def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Extract user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')


def log_admin_action(user, action, model_name, object_id, object_repr='', changes=None, request=None):
    """
    Log an admin action to AuditLog
    """
    ip_address = None
    user_agent = ''
    
    if request:
        ip_address = get_client_ip(request)
        user_agent = get_user_agent(request)
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=object_id,
        object_repr=object_repr,
        changes=changes or {},
        ip_address=ip_address,
        user_agent=user_agent
    )
