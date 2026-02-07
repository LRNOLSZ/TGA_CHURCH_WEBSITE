from rest_framework import serializers
from .models import (
    HomeBanner, ChurchInfo, HeadPastor, ServiceTime,
    Leader, PhotoGallery, Sermon, Event, Branch,
    GivingInfo, GivingImage, ImageLog, ContactMessage, Testimony, Book, ExchangeRate, Merchandise
)


# ====================================================================
# HOME PAGE SERIALIZERS
# ====================================================================

class HomeBannerSerializer(serializers.ModelSerializer):
    """Serializer for rotating home page banners"""
    class Meta:
        model = HomeBanner
        fields = [
            'id', 'title', 'subtitle', 'image', 'button_text', 'button_link',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ChurchInfoSerializer(serializers.ModelSerializer):
    """Serializer for church information (singleton)"""
    class Meta:
        model = ChurchInfo
        fields = [
            'id', 'church_name', 'tagline', 'welcome_message', 'full_about',
            'address', 'phone', 'email',
            'mission_statement', 'vision_statement', 'core_values',
            'service_times_text',
            'youtube_channel_url', 'facebook_url', 'instagram_url',
            'twitter_url', 'tiktok_url', 'whatsapp_url',
            'updated_at'
        ]
        read_only_fields = ['updated_at']


class HeadPastorSerializer(serializers.ModelSerializer):
    """Serializer for head pastor information"""
    class Meta:
        model = HeadPastor
        fields = [
            'id', 'name', 'title', 'full_bio', 'image',
            'email', 'phone', 'whatsapp_url', 'instagram', 'tiktok',
            'updated_at'
        ]
        read_only_fields = ['updated_at']


class ServiceTimeSerializer(serializers.ModelSerializer):
    """Serializer for service times"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = ServiceTime
        fields = [
            'id', 'day', 'time', 'service_type', 'branch', 'branch_name',
            'additional_info', 'is_active'
        ]


# ====================================================================
# ABOUT US SERIALIZERS
# ====================================================================

class LeaderSerializer(serializers.ModelSerializer):
    """Serializer for church leadership team"""
    class Meta:
        model = Leader
        fields = [
            'id', 'full_name', 'position', 'biography', 'profile_picture',
            'email', 'phone', 'is_featured_on_home', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']


class PhotoGallerySerializer(serializers.ModelSerializer):
    """Serializer for photo gallery"""
    class Meta:
        model = PhotoGallery
        fields = [
            'id', 'title', 'image', 'caption', 'category', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at']


# ====================================================================
# SERMONS SERIALIZERS
# ====================================================================

class SermonSerializer(serializers.ModelSerializer):
    """Serializer for sermons/messages"""
    class Meta:
        model = Sermon
        fields = [
            'id', 'title', 'description', 'speaker', 'date',
            'video_url', 'custom_thumbnail', 'scripture_reference',
            'series', 'duration', 'is_published', 'is_featured',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ====================================================================
# EVENTS SERIALIZERS
# ====================================================================

class EventSerializer(serializers.ModelSerializer):
    """Serializer for church events"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location',
            'branch', 'branch_name', 'image', 'category',
            'registration_link', 'contact_person',
            'is_active', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ====================================================================
# BRANCHES SERIALIZERS
# ====================================================================

class BranchSerializer(serializers.ModelSerializer):
    """Serializer for church branches"""
    service_times = ServiceTimeSerializer(many=True, read_only=True)
    events_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = [
            'id', 'name', 'location', 'phone', 'email',
            'pastor_in_charge', 'service_time', 'image',
            'google_maps_url', 'is_main_branch',
            'service_times', 'events_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_events_count(self, obj):
        return obj.events.filter(is_active=True).count()


# ====================================================================
# GIVING/DONATIONS SERIALIZERS
# ====================================================================

class GivingImageSerializer(serializers.ModelSerializer):
    """Serializer for giving page images"""
    class Meta:
        model = GivingImage
        fields = ['id', 'image', 'caption', 'order', 'created_at']
        read_only_fields = ['created_at']


class GivingInfoSerializer(serializers.ModelSerializer):
    """Serializer for giving page content"""
    images = GivingImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = GivingInfo
        fields = [
            'id', 'flutterwave_link', 'title', 'instructions',
            'why_give_message', 'images', 'updated_at'
        ]
        read_only_fields = ['updated_at']


# ====================================================================
# CONTACT/MESSAGES SERIALIZERS
# ====================================================================

class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for contact form submissions"""
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject', 'message',
            'is_read', 'submitted_at'
        ]
        read_only_fields = ['submitted_at']


class TestimonySerializer(serializers.ModelSerializer):
    """Serializer for testimonies"""
    source_message_name = serializers.CharField(source='source_message.name', read_only=True)
    
    class Meta:
        model = Testimony
        fields = [
            'id', 'name', 'testimony_text', 'location', 'image',
            'show_on_carousel', 'is_approved', 'category', 'order',
            'source_message', 'source_message_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ====================================================================
# PRODUCTS SERIALIZERS
# ====================================================================

class BookSerializer(serializers.ModelSerializer):
    """Serializer for books"""
    class Meta:
        model = Book
        fields = [
            'id', 'name', 'price', 'image', 'description',
            'whatsapp_link', 'email', 'amazon',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class MerchandiseSerializer(serializers.ModelSerializer):
    """Serializer for merchandise"""
    class Meta:
        model = Merchandise
        fields = [
            'id', 'name', 'price', 'image', 'description',
            'whatsapp_link', 'jiji_link', 'amazon_link', 'email',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExchangeRateSerializer(serializers.ModelSerializer):
    """Serializer for exchange rates"""
    class Meta:
        model = ExchangeRate
        fields = [
            'id', 'currency_code', 'currency_name', 'rate', 'last_updated'
        ]
        read_only_fields = ['last_updated']


# ====================================================================
# AUDIT/LOG SERIALIZERS
# ====================================================================

class ImageLogSerializer(serializers.ModelSerializer):
    """Serializer for image logs (read-only)"""
    class Meta:
        model = ImageLog
        fields = [
            'id', 'image', 'section_name', 'file_size', 'uploaded_at'
        ]
        read_only_fields = ['id', 'image', 'section_name', 'file_size', 'uploaded_at']
