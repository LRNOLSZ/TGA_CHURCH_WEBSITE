from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils import timezone
from django.db.models import Count, DateTimeField
from django.forms.widgets import DateTimeInput
from django import forms
from datetime import datetime

# Unfold specific imports
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils.html import format_html

# ====================================================================
# CUSTOM FORMS
# ====================================================================

class EventAdminForm(forms.ModelForm):
    """Custom form for Event that separates date and time"""
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Event Date',
        help_text='Select the date (calendar picker)'
    )
    event_time = forms.TimeField(
        widget=forms.TextInput(attrs={'type': 'time', 'placeholder': 'HH:MM'}),
        label='Event Time',
        help_text='Enter time manually (HH:MM format, e.g., 14:30)'
    )
    
    class Meta:
        from .models import Event
        model = Event
        fields = ('title', 'description', 'category', 'image', 'event_date', 'event_time', 'location', 'branch', 'contact_person', 'registration_link', 'is_active', 'is_featured')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing event, populate date and time fields
        if self.instance and self.instance.pk:
            self.fields['event_date'].initial = self.instance.date.date()
            self.fields['event_time'].initial = self.instance.date.time()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Combine date and time back into datetime
        if self.cleaned_data.get('event_date') and self.cleaned_data.get('event_time'):
            instance.date = datetime.combine(
                self.cleaned_data['event_date'],
                self.cleaned_data['event_time']
            )
        if commit:
            instance.save()
        return instance


# Your church models
from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ImageLog, ContactMessage, Testimony, Book, ExchangeRate, Merchandise, AuditLog, UserProfile
)

# ====================================================================
# AUTH MODELS FIX (Restores the Delete/Run Button)
# ====================================================================

class UserProfileInline(TabularInline):
    """Inline profile editor for users"""
    model = UserProfile
    extra = 0
    fields = ('profile_picture', 'bio', 'phone')


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = [UserProfileInline]
    
    def profile_picture_preview(self, obj):
        """Show profile picture in list view"""
        try:
            profile = obj.profile
            if profile.profile_picture and hasattr(profile.profile_picture, 'url'):
                return format_html(
                    '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 1px solid #ddd;" />', 
                    profile.profile_picture.url
                )
        except:
            pass
        return "—"
    profile_picture_preview.short_description = "Picture"
    
    # Add picture preview to list display
    list_display = ('profile_picture_preview', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

# ====================================================================
# UTILITY MIXINS
# ====================================================================

class AdminImagePreviewMixin:
    """Helper to show thumbnails in the admin list view using Unfold styling."""
    def image_preview(self, obj):
        img = (getattr(obj, 'image', None) or 
               getattr(obj, 'profile_picture', None) or 
               getattr(obj, 'custom_thumbnail', None) or
               getattr(obj, 'logo', None))
        
        if img and hasattr(img, 'url'):
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; border-radius: 8px; object-fit: cover; border: 1px solid #ddd;" />', 
                img.url
            )
        return "No Image"
    image_preview.short_description = "Preview"

# ====================================================================
# INLINES
# ====================================================================

class GivingImageInline(TabularInline):
    model = GivingImage
    extra = 1
    fields = ('image', 'caption', 'order')

# ====================================================================
# CHURCH ADMIN CLASSES
# ====================================================================

@admin.register(HomeBanner)
class HomeBannerAdmin(ModelAdmin, AdminImagePreviewMixin):
    list_display = ('image_preview', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
    ordering = ('order',)

@admin.register(ChurchInfo)
class ChurchInfoAdmin(ModelAdmin):
    fieldsets = (
        ('General Branding', {'fields': ('church_name', 'tagline', 'welcome_message', 'full_about')}),
        ('Contact Info', {'fields': ('address', 'phone', 'email')}),
        ('Mission & Vision', {'fields': ('mission_statement', 'vision_statement', 'core_values')}),
        ('Social Media', {'fields': ('youtube_channel_url', 'facebook_url', 'instagram_url', 'twitter_url', 'tiktok_url', 'whatsapp_url')}),
    )
    def has_add_permission(self, request):
        return not ChurchInfo.objects.exists()

@admin.register(HeadPastor)
class HeadPastorAdmin(ModelAdmin, AdminImagePreviewMixin):
    list_display = ('image_preview', 'name', 'title')
    fieldsets = (
        ('Personal Info', {'fields': ('name', 'title', 'image')}),
        ('Biography', {'fields': ('full_bio',)}),
        ('Contact', {'fields': ('email', 'phone', 'whatsapp_url', 'instagram', 'tiktok')}),
    )
    def has_add_permission(self, request):
        return not HeadPastor.objects.exists()

@admin.register(ServiceTime)
class ServiceTimeAdmin(ModelAdmin):
    list_display = ('day', 'time', 'service_type', 'branch', 'is_active')
    list_filter = ('day', 'is_active', 'branch')
    list_editable = ('is_active',)

@admin.register(Leader)
class LeaderAdmin(ModelAdmin, AdminImagePreviewMixin):
    list_display = ('image_preview', 'full_name', 'position', 'is_featured_on_home', 'order')
    list_editable = ('is_featured_on_home', 'order')
    list_filter = ('position', 'is_featured_on_home')

@admin.register(PhotoGallery)
class PhotoGalleryAdmin(ModelAdmin, AdminImagePreviewMixin):
    list_display = ('image_preview', 'title', 'category', 'uploaded_at')
    list_filter = ('category',)

@admin.register(Sermon)
class SermonAdmin(ModelAdmin):
    list_display = ('title', 'speaker', 'date', 'is_published', 'is_featured')
    list_filter = ('speaker', 'is_published', 'is_featured')
    search_fields = ('title', 'speaker', 'series', 'scripture_reference')

@admin.register(Event)
class EventAdmin(ModelAdmin, AdminImagePreviewMixin):
    form = EventAdminForm
    list_display = ('image_preview', 'title', 'date', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'description', 'category', 'image')
        }),
        ('Event Details', {
            'fields': ('event_date', 'event_time', 'location', 'branch', 'contact_person')
        }),
        ('Links & Registration', {
            'fields': ('registration_link',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
    )
    # Use simple datetime-local input for manual time entry
    formfield_overrides = {
        DateTimeField: {'widget': forms.HiddenInput()}
    }

@admin.register(Branch)
class BranchAdmin(ModelAdmin, AdminImagePreviewMixin):
    list_display = ('image_preview', 'name', 'pastor_in_charge', 'is_main_branch')
    list_filter = ('is_main_branch',)

@admin.register(GivingInfo)
class GivingInfoAdmin(ModelAdmin):
    inlines = [GivingImageInline]
    def has_add_permission(self, request):
        return not GivingInfo.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('is_read', 'name', 'subject', 'submitted_at')
    list_filter = ('is_read', 'subject')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'submitted_at')
    actions = ['mark_as_read']

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    
    def has_add_permission(self, request):
        return False

@admin.register(ImageLog)
class ImageLogAdmin(ModelAdmin):
    list_display = ('section_name', 'file_size', 'uploaded_at')
    readonly_fields = ('image', 'section_name', 'file_size', 'uploaded_at', 'content_type', 'object_id')
    
    def has_add_permission(self, request): return False
    def has_delete_permission(self, request, obj=None): return False
    def has_change_permission(self, request, obj=None): return False


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Book Information', {
            'fields': ('name', 'price', 'image', 'description')
        }),
        ('Purchase Links', {
            'fields': ('whatsapp_link', 'email', 'amazon'),
            'description': 'Links for customers to purchase the book'
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Merchandise)
class MerchandiseAdmin(ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'price', 'image', 'description')
        }),
        ('Purchase Links', {
            'fields': ('whatsapp_link', 'jiji_link', 'amazon_link', 'email'),
            'description': 'Links for customers to purchase this item'
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExchangeRate)
class ExchangeRateAdmin(ModelAdmin):
    list_display = ('currency_code', 'currency_name', 'rate', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('currency_code', 'currency_name')
    readonly_fields = ('last_updated',)
    fieldsets = (
        ('Currency Information', {
            'fields': ('currency_code', 'currency_name')
        }),
        ('Exchange Rate', {
            'fields': ('rate',),
            'description': 'Rate from 1 USD to this currency'
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent accidental deletion


# ====================================================================
# AUDIT LOG ADMIN (READ-ONLY)
# ====================================================================

@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'timestamp', 'ip_address')
    list_filter = ('action', 'model_name', 'timestamp')
    search_fields = ('user__username', 'model_name', 'ip_address')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'user_agent', 'timestamp')
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of audit logs


# ====================================================================
# USER PROFILE ADMIN
# ====================================================================

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ('user', 'profile_picture_preview', 'phone')
    search_fields = ('user__username', 'user__email')
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
        ('Info', {'fields': ('bio', 'phone')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    def profile_picture_preview(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover; border: 2px solid #ddd;" />', 
                obj.profile_picture.url
            )
        return "No Picture"
    profile_picture_preview.short_description = "Picture"


# ====================================================================
# UNFOLD DASHBOARD CUSTOMIZATION
# ====================================================================
