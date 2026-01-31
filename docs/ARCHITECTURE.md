# System Architecture & Code Documentation

Complete overview of the TGA Church Management System architecture, models, components, and design patterns.

## Table of Contents

1. [System Overview](#system-overview)
2. [Database Models](#database-models)
3. [Core Components](#core-components)
4. [Signal System](#signal-system)
5. [Middleware & Context](#middleware--context)
6. [File Upload Validation](#file-upload-validation)
7. [Logging & Audit Trail](#logging--audit-trail)
8. [Admin Interface](#admin-interface)

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Django Application                       │
├─────────────────────────────────────────────────────────────┤
│  Frontend (React/Vue)                                       │
│         ↓                                                   │
│  REST API (DRF)                                             │
│         ↓                                                   │
│  Views → Serializers → Models                              │
│         ↓                                                   │
│  Signals (auto-logging, cleanup)                           │
│         ↓                                                   │
│  PostgreSQL Database                                        │
└─────────────────────────────────────────────────────────────┘

                    Admin Interface
  ─────────────────────────────────────
  │ Admin Dashboard (django-unfold)    │
  │ - Create/Update/Delete content     │
  │ - Manage users & permissions       │
  │ - View audit logs                  │
  └────────────────────────────────────┘
```

## Database Models

### Core Content Models

#### Event
```python
class Event(models.Model):
    title = CharField(max_length=200)
    description = TextField()
    event_date = DateField()
    event_time = TimeField()
    location = CharField(max_length=200)
    image = ImageField(upload_to='events/', blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
```

**Signals:**
- `post_save` → Creates ImageLog entry when image uploaded
- `pre_delete` → Removes orphaned ImageLog entries

**Admin Features:**
- Separate date picker (EventAdminForm.event_date)
- Manual time input (EventAdminForm.event_time)
- Image preview in list view

#### Sermon
```python
class Sermon(models.Model):
    title = CharField(max_length=200)
    description = TextField()
    preacher = CharField(max_length=100)
    date = DateField()
    image = ImageField(upload_to='sermons/', blank=True, null=True)
    video_url = URLField(blank=True, null=True)
```

#### HomeBanner, HeadPastor, Leader, PhotoGallery, GivingImage, Branch, Merchandise, Book

All follow similar pattern with `image` field and automatic ImageLog tracking.

### User & Profile Models

#### User (Django Built-in)
```python
# Extended via UserProfile OneToOne relationship
user.userprofile.profile_picture
user.userprofile.bio
user.userprofile.phone
```

#### UserProfile
```python
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_picture = ImageField(upload_to='profiles/', blank=True, null=True)
    bio = TextField(blank=True, null=True)
    phone = CharField(max_length=20, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile: {self.user.username}"
```

**Purpose:**
- Stores optional user profile pictures
- NOT tracked in ImageLog (privacy-first design)
- Admin can see profile picture previews in users list
- Logged-in user sees their picture in sidebar

**Signals:**
- `post_save` on User → Auto-creates UserProfile if doesn't exist

### Logging Models

#### AuditLog
```python
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('PERMISSION_DENIED', 'Permission Denied'),
    ]
    
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = CharField(max_length=100, blank=True, null=True)
    object_id = IntegerField(blank=True, null=True)
    object_str = CharField(max_length=500, blank=True, null=True)
    changes = JSONField(default=dict, blank=True)
    ip_address = GenericIPAddressField(null=True, blank=True)
    user_agent = CharField(max_length=500, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.action} - {self.model_name} - {self.created_at}"
```

**Tracks:**
- User authentication (LOGIN/LOGOUT)
- Model operations (CREATE/UPDATE/DELETE)
- IP address and user agent
- Changes in JSON format
- Timestamp of every action

#### ImageLog
```python
class ImageLog(models.Model):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    model_name = CharField(max_length=100)
    object_id = IntegerField()
    image_url = URLField()
    file_size = IntegerField()  # in bytes
    image_field = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['model_name', 'object_id']),
        ]

    def __str__(self):
        return f"{self.model_name} - {self.created_at}"
```

**Tracks:**
- Which model uploaded image
- Image file size and URL
- Who uploaded and when
- Used for auditing image usage across 10 models

**Excluded from Tracking:**
- UserProfile images (privacy design)
- Testimony images (per user request)

## Core Components

### 1. API Views (api/views.py)

Uses Django REST Framework for API endpoints:

```python
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    # Automatic routing:
    # GET /api/events/ → list()
    # POST /api/events/ → create()
    # GET /api/events/{id}/ → retrieve()
    # PUT /api/events/{id}/ → update()
    # DELETE /api/events/{id}/ → destroy()
```

**Key Features:**
- Automatic CRUD operations
- Pagination support
- Search/filtering
- Serializer validation

### 2. Serializers

Validates input and formats output:

```python
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_date', 
                  'event_time', 'location', 'image', 'created_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### 3. File Upload Validation (api/validators.py)

```python
def validate_image_file(file):
    """Validate image uploads"""
    # Check 1: File size (max 10MB)
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(f"Image too large (max {MAX_IMAGE_SIZE/1024/1024}MB)")
    
    # Check 2: File extension
    ext = file.name.split('.')[-1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(f"Invalid format. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
    
    # Check 3: MIME type verification
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    if mime_type not in ALLOWED_IMAGE_MIMES:
        raise ValidationError("File content doesn't match extension")
    
    # Check 4: Filename sanitization
    file.name = sanitize_filename(file.name)
    
    return file
```

**Security Features:**
- File size limit (10MB)
- Extension whitelist (jpg, png, gif, webp)
- MIME type verification
- Filename sanitization (removes special chars)

## Signal System

Django signals automatically trigger code when model events occur.

### Auto-Create ImageLog on Upload

```python
@receiver(post_save, sender=Event)
def log_image_upload(sender, instance, created, **kwargs):
    """Auto-create ImageLog when image uploaded"""
    if instance.image:
        ImageLog.objects.get_or_create(
            model_name=sender.__name__,
            object_id=instance.id,
            defaults={
                'image_url': instance.image.url,
                'file_size': instance.image.size,
                'image_field': 'image',
                'user': get_current_user(),  # From thread-local
            }
        )
```

**Tracked Models (10 total):**
1. HomeBanner
2. HeadPastor
3. Leader
4. PhotoGallery
5. Sermon
6. Event
7. GivingImage
8. Branch
9. Merchandise
10. Book

### Auto-Cleanup Orphaned Logs

```python
@receiver(pre_delete, sender=Event)
def cleanup_image_logs_on_delete(sender, instance, **kwargs):
    """Remove orphaned ImageLog entries when parent deleted"""
    ImageLog.objects.filter(
        model_name=sender.__name__,
        object_id=instance.id
    ).delete()
```

**Why Needed:**
- Django's GenericForeignKey doesn't cascade delete
- Prevents orphaned image log entries
- Keeps audit trail clean

### Auto-Create UserProfile

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile when User created"""
    if created:
        UserProfile.objects.create(user=instance)
```

**Benefit:**
- User always has profile object available
- No "UserProfile matching query does not exist" errors

## Middleware & Context

### AuditLoggingMiddleware

Captures request context (IP, user agent) for audit logging:

```python
class AuditLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._thread_locals = threading.local()

    def __call__(self, request):
        # Store request in thread-local storage
        self._thread_locals.request = request
        
        response = self.get_response(request)
        return response

    @classmethod
    def get_request(cls):
        """Retrieve request from thread-local (used by signals)"""
        return getattr(cls._thread_locals, 'request', None)
```

**Purpose:**
- Makes request object available to signals
- Signals extract IP address and user agent
- Enables audit logging with client info

### Signal Handlers for Audit Logging

```python
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log when user logs in"""
    AuditLog.objects.create(
        user=user,
        action='LOGIN',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )

@receiver(post_save, sender=Event)
def log_model_action(sender, instance, created, **kwargs):
    """Log when Event created or updated"""
    request = AuditLoggingMiddleware.get_request()
    
    AuditLog.objects.create(
        user=request.user if request and request.user.is_authenticated else None,
        action='CREATE' if created else 'UPDATE',
        model_name=sender.__name__,
        object_id=instance.id,
        object_str=str(instance)[:500],
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500] if request else ''
    )
```

## File Upload Validation

### Model Field Validation

```python
class Event(models.Model):
    image = ImageField(
        upload_to='events/',
        validators=[validate_image_file],
        blank=True,
        null=True
    )
```

### Two-Layer Validation

```
1. Django's built-in ImageField checks
   ↓
2. Custom validators.validate_image_file()
   ├─ Size check (10MB max)
   ├─ Extension check (whitelist)
   ├─ MIME type verification
   └─ Filename sanitization
```

## Logging & Audit Trail

### Logging Configuration (settings.py)

```python
LOGGING = {
    'handlers': {
        'django_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 15728640,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 15728640,
            'backupCount': 10,
            'level': 'WARNING'
        },
        'audit_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/audit.log',
            'maxBytes': 15728640,
            'backupCount': 10,
            'level': 'INFO'
        }
    }
}
```

### Three Log Files

| File | Purpose | Events |
|------|---------|--------|
| `django.log` | Application logs | Errors, warnings, info |
| `security.log` | Security events | Auth failures, suspicious activity |
| `audit.log` | Audit trail | All admin actions with IP/user |

### Viewing Audit Logs

**In Admin:**
1. Go to `/admin/api/auditlog/`
2. View all user actions with timestamps
3. See IP addresses and user agents
4. Filter by action type or date

**Via Script:**
```python
from api.models import AuditLog

# Recent actions
recent = AuditLog.objects.all()[:10]

# Login events
logins = AuditLog.objects.filter(action='LOGIN')

# User's actions
user_actions = AuditLog.objects.filter(user__username='admin')
```

## Admin Interface

### Customizations

#### EventAdminForm - Separated Date/Time

Problem: Django's default datetime picker limited to presets (6am, 6pm, midnight)

Solution: Custom form with separate fields:

```python
class EventAdminForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    event_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Combine date + time into datetime
        instance.event_datetime = datetime.combine(
            self.cleaned_data['event_date'],
            self.cleaned_data['event_time']
        )
        if commit:
            instance.save()
        return instance
```

#### UserAdmin Enhancement - Profile Picture Preview

Shows profile picture thumbnail in users list:

```python
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'profile_picture_preview']
    
    def profile_picture_preview(self, obj):
        if hasattr(obj, 'userprofile') and obj.userprofile.profile_picture:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; '
                'border-radius: 50%;" />',
                obj.userprofile.profile_picture.url
            )
        return "—"
    profile_picture_preview.short_description = "Profile Picture"
```

#### UserProfileInline - Edit Profile with User

Allows editing profile picture while creating/editing user:

```python
class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fields = ['profile_picture', 'bio', 'phone']
    extra = 0
```

#### AuditLogAdmin - Read-Only View

Prevents accidental audit log modification:

```python
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'model_name', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'ip_address']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 
                       'changes', 'ip_address', 'user_agent', 'created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
```

## Data Flow Diagram

```
Admin Creates Event
        ↓
EventAdminForm validates input
        ↓
Event model saved to DB
        ↓
Signals triggered (post_save)
        ↓
├─→ log_image_upload() → Creates ImageLog entry
├─→ log_model_action() → Creates AuditLog entry
└─→ Logging to audit.log file
        ↓
Admin sees success message
ImageLog now shows event's image upload
AuditLog shows who did what when from where
```

## Security Layers

```
Input → Serializer validation → Model validators → 
File validators → Signals/Cleanup → Database

Admin Actions → Middleware captures request → 
Signals log to AuditLog → Rotating file logs
```

---

**Last Updated:** January 2026
