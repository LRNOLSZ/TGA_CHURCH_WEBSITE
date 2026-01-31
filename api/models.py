from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from embed_video.fields import EmbedVideoField

# ====================================================================
# HOME PAGE MODELS
# ====================================================================

class HomeBanner(models.Model):
    """
    Rotating banners on home page for dynamic content display.
    Multiple banners can be created and rotated automatically.
    """
    title = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Main heading text overlaid on banner"
    )
    subtitle = models.CharField(
        max_length=300, 
        blank=True, 
        null=True,
        help_text="Subheading or description text"
    )
    image = models.ImageField(
        upload_to='banners/%Y/%m/',  # Organized by year/month
        help_text="Banner image (recommended: 1920x600px)"
    )
    button_text = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Call-to-action button text (e.g., 'Join Us')"
    )
    button_link = models.URLField(
        blank=True, 
        null=True,
        help_text="Where the button should link to"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,  # PERFORMANCE: Fast filtering of active banners
        help_text="Uncheck to hide this banner"
    )
    order = models.IntegerField(
        default=0,
        db_index=True,  # PERFORMANCE: Fast ordering
        help_text="Lower numbers appear first"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Home Banner"
        verbose_name_plural = "Home Banners"
        indexes = [
            models.Index(fields=['is_active', 'order']),  # PERFORMANCE: Composite index
        ]
    
    def __str__(self):
        return self.title or f"Banner {self.id}"


class ChurchInfo(models.Model):
    """
    General church information - Should only have ONE record.
    Contains all static church details displayed across the site.
    """
    church_name = models.CharField(max_length=200)
    tagline = models.CharField(
        max_length=300, 
        blank=True,
        help_text="Short catchy phrase (e.g., 'Building Faith, Changing Lives')"
    )
    welcome_message = models.TextField(
        help_text="Brief introduction for home page"
    )
    full_about = models.TextField(
        help_text="Complete church history and story for About page"
    )
    
    # Contact Information
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Mission & Vision
    mission_statement = models.TextField()
    vision_statement = models.TextField()
    core_values = models.TextField(
        blank=True,
        help_text="Core beliefs and values (optional)"
    )
    
    # Service Information
    service_times_text = models.TextField(
        help_text="General service times description"
    )
    
    # Social Media Links
    youtube_channel_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    whatsapp_url = models.URLField(blank=True, null=True)
    
    # Metadata
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Church Information"
        verbose_name_plural = "Church Information"
    
    def __str__(self):
        return self.church_name
    
    def save(self, *args, **kwargs):
        """Ensure only one ChurchInfo record exists"""
        if not self.pk and ChurchInfo.objects.exists():
            raise ValueError('Only one Church Information record is allowed')
        return super().save(*args, **kwargs)


class HeadPastor(models.Model):
    """
    Head Pastor information - Featured prominently on home page.
    Should only have ONE record for the lead pastor.
    """
    name = models.CharField(max_length=200)
    title = models.CharField(
        max_length=200,
        default="Senior Pastor",
        help_text="Official title (e.g., 'Senior Pastor & Founder')"
    )
    full_bio = models.TextField(help_text="Complete biography")
    image = models.ImageField(
        upload_to='leaders/',
        help_text="Professional photo (recommended: square format)"
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Pastor's office number (not personal number)"
    )
    whatsapp_url = models.URLField(
        blank=True,
        null=True,
        help_text="WhatsApp channel link (e.g., https://whatsapp.com/channel/...)"
    )
    instagram = models.URLField(
        blank=True,
        null=True,
        help_text="Instagram profile URL (e.g., https://instagram.com/username)"
    )
    tiktok = models.URLField(
        blank=True,
        null=True,
        help_text="TikTok profile URL (e.g., https://tiktok.com/@username)"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Head Pastor"
        verbose_name_plural = "Head Pastor"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one HeadPastor record exists"""
        if not self.pk and HeadPastor.objects.exists():
            raise ValueError('Only one Head Pastor record is allowed')
        return super().save(*args, **kwargs)


class ServiceTime(models.Model):
    """
    Detailed service schedule for all church services.
    Can be filtered by day, branch, or service type.
    """
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    day = models.CharField(
        max_length=20, 
        choices=DAY_CHOICES,
        db_index=True  # PERFORMANCE: Fast filtering by day
    )
    time = models.CharField(
        max_length=50,
        help_text="e.g., '9:00 AM' or '6:00 PM'"
    )
    service_type = models.CharField(
        max_length=200,
        help_text="e.g., 'Sunday Worship', 'Midweek Service', 'Prayer Meeting'"
    )
    branch = models.ForeignKey(
        'Branch', 
        on_delete=models.CASCADE, 
        related_name='service_times',
        null=True, 
        blank=True,
        help_text="Leave blank for services at all branches"
    )
    additional_info = models.CharField(
        max_length=300, 
        blank=True, 
        null=True,
        help_text="Extra details (e.g., 'With Holy Communion')"
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True  # PERFORMANCE
    )
    
    class Meta:
        ordering = ['day', 'time']
        verbose_name = "Service Time"
        verbose_name_plural = "Service Times"
        indexes = [
            models.Index(fields=['is_active', 'day']),  # PERFORMANCE: Composite index
        ]
    
    def __str__(self):
        branch_name = f" at {self.branch.name}" if self.branch else ""
        return f"{self.day} - {self.time} ({self.service_type}){branch_name}"


# ====================================================================
# ABOUT US PAGE MODELS
# ====================================================================

class Leader(models.Model):
    """
    Church leadership team (excluding head pastor who has dedicated model).
    Can be featured on home page or displayed only on About page.
    """
    ROLE_CHOICES = [
        ('Shepherd', 'Shepherd'),
        ('Ministry Leader', 'Ministry Leader'),
        ('Worship Leader', 'Worship Leader'),
        ('Other', 'Other'),
    ]
    
    full_name = models.CharField(max_length=200)
    position = models.CharField(
        max_length=100, 
        choices=ROLE_CHOICES,
        help_text="Leadership role/title"
    )
    biography = models.TextField()
    profile_picture = models.ImageField(
        upload_to='leaders/%Y/',
        help_text="Professional photo"
    )
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number (e.g., +1-555-0123)"
    )
    
    
    is_featured_on_home = models.BooleanField(
        default=False,
        db_index=True,  # PERFORMANCE
        verbose_name="Feature on Home Page",
        help_text="Check to display on homepage"
    )
    
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers first)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Church Leader"
        verbose_name_plural = "Church Leaders"
        ordering = ['order', 'position', 'full_name']
        indexes = [
            models.Index(fields=['is_featured_on_home', 'order']),  # PERFORMANCE
        ]
    
    def __str__(self):
        return f"{self.full_name} ({self.position})"


class PhotoGallery(models.Model):
    """
    Church photo gallery for About page and general site imagery.
    Organized by categories for easy filtering.
    """
    CATEGORY_CHOICES = [
        ('Church Building', 'Church Building'),
        ('Worship', 'Worship Service'),
        ('Events', 'Special Events'),
        ('Outreach', 'Outreach & Missions'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='gallery/%Y/%m/',  # PERFORMANCE: Organized by date
        help_text="Church photos"
    )
    caption = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional description"
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='Other',
        db_index=True  # PERFORMANCE: Fast filtering
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)  # PERFORMANCE
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Photo"
        verbose_name_plural = "Photo Gallery"
        indexes = [
            models.Index(fields=['category', '-uploaded_at']),  # PERFORMANCE: Composite index
        ]
    
    def __str__(self):
        return self.title


# ====================================================================
# SERMONS PAGE MODELS
# ====================================================================

class Sermon(models.Model):
    """
    Sermon/message archive with video embedding support.
    Automatically handles YouTube/Vimeo thumbnails and embedding.
    """
    title = models.CharField(
        max_length=300,
        db_index=True  # PERFORMANCE: For search
    )
    description = models.TextField()
    speaker = models.CharField(
        max_length=200,
        db_index=True,  # PERFORMANCE: Filter by speaker
        help_text="Name of the preacher"
    )
    date = models.DateField(db_index=True)  # PERFORMANCE: Sorting and filtering
    
    # Video embedding with automatic thumbnail generation
    video_url = EmbedVideoField(
        blank=True,
        null=True,
        verbose_name="Video Link (YouTube, Vimeo)",
        help_text="Paste YouTube or Vimeo URL - thumbnails are generated automatically"
    )
    
    # Optional manual thumbnail override
    custom_thumbnail = models.ImageField(
        upload_to='sermon_thumbnails/%Y/',
        blank=True,
        null=True,
        help_text="Optional: Upload custom thumbnail (overrides auto-generated)"
    )
    
    scripture_reference = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Bible passage reference (e.g., 'John 3:16-21')"
    )
    series = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        db_index=True,  # PERFORMANCE: Filter by series
        help_text="Sermon series name (if part of a series)"
    )
    duration = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Video length (e.g., '45 min')"
    )
    
    is_published = models.BooleanField(
        default=True,
        db_index=True,  # PERFORMANCE
        help_text="Uncheck to hide drafts or archived sermons"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,  # PERFORMANCE
        help_text="Feature on home page"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = "Sermon/Message"
        verbose_name_plural = "Sermons & Messages"
        indexes = [
            models.Index(fields=['-date', 'is_published']),  # PERFORMANCE: Main query
            models.Index(fields=['speaker', '-date']),  # PERFORMANCE: Speaker filter
            models.Index(fields=['series', '-date']),  # PERFORMANCE: Series filter
        ]
    
    def __str__(self):
        return f"{self.title} - {self.speaker} ({self.date})"
    
    def get_absolute_url(self):
        return reverse('sermon_detail', args=[str(self.id)])


# ====================================================================
# EVENTS PAGE MODELS
# ====================================================================

class Event(models.Model):
    """
    Church events calendar with categorization and branch support.
    Optimized for chronological queries and filtering.
    """
    CATEGORY_CHOICES = [
        ('General', 'General Church Event'),
        ('Conference', 'Conference/Convention'),
        ('Outreach', 'Outreach/Evangelism'),
        ('Worship Night', 'Worship Night'),
        ('Healing to the city', 'Healing to the city'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(
        max_length=300,
        db_index=True  # PERFORMANCE: Search
    )
    description = models.TextField()
    date = models.DateTimeField(
        db_index=True,  # PERFORMANCE: Critical for sorting/filtering
        help_text="Event date and start time"
    )
    location = models.CharField(
        max_length=300,
        help_text="Venue or address"
    )
    branch = models.ForeignKey(
        'Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Associated branch (if applicable)"
    )
    image = models.ImageField(
        upload_to='events/%Y/%m/',  # PERFORMANCE: Organized by date
        help_text="Event poster or banner"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='General',
        db_index=True  # PERFORMANCE: Filtering
    )
    registration_link = models.URLField(
        blank=True,
        null=True,
        help_text="External registration/ticketing link"
    )
    contact_person = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Person to contact for questions"
    )
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,  # PERFORMANCE
        help_text="Uncheck to hide past events"
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True,  # PERFORMANCE
        help_text="Feature on home page"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date']  # Chronological by default
        verbose_name = "Event"
        verbose_name_plural = "Events"
        indexes = [
            models.Index(fields=['date', 'is_active']),  # PERFORMANCE: Main query
            models.Index(fields=['category', 'date']),  # PERFORMANCE: Category filter
            models.Index(fields=['is_featured', 'date']),  # PERFORMANCE: Featured events
        ]
    
    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"
    
    def get_absolute_url(self):
        return reverse('event_detail', args=[str(self.id)])


# ====================================================================
# BRANCHES PAGE MODELS
# ====================================================================

class Branch(models.Model):
    """
    Church branch locations with contact and service information.
    Supports multiple campuses/locations.
    """
    name = models.CharField(
        max_length=200,
        db_index=True  # PERFORMANCE: Search
    )
    location = models.TextField(
        help_text="Full address for maps/GPS"
    )
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    pastor_in_charge = models.CharField(
        max_length=200,
        help_text="Name of pastor leading this branch"
    )
    
    # Service times stored as text for flexibility
    service_time = models.TextField(
        help_text="Service schedule (e.g., 'Sundays: 9AM & 11AM, Wednesdays: 6PM')"
    )
    
    image = models.ImageField(
        upload_to='branches/',
        blank=True,
        null=True,
        help_text="Photo of the branch building/location"
    )
    
    google_maps_url = models.URLField(
        blank=True,
        null=True,
        help_text="Google Maps link for directions"
    )
    
    is_main_branch = models.BooleanField(
        default=False,
        db_index=True,  # PERFORMANCE
        help_text="Check if this is the main/headquarters branch"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_main_branch', 'name']  # Main branch first
        verbose_name = "Church Branch"
        verbose_name_plural = "Church Branches"
        indexes = [
            models.Index(fields=['is_main_branch', 'name']),  # PERFORMANCE
        ]
    
    def __str__(self):
        main_indicator = " (Main)" if self.is_main_branch else ""
        return f"{self.name}{main_indicator}"


# ====================================================================
# GIVING/DONATIONS PAGE MODELS
# ====================================================================

class GivingInfo(models.Model):
    """
    Simple giving page content - payment link and images.
    Should only have ONE record.
    """
    flutterwave_link = models.URLField(
        help_text="Flutterwave payment page link"
    )
    
    title = models.CharField(
        max_length=200,
        default="Give Online",
        help_text="Page heading"
    )
    
    instructions = models.TextField(
        help_text="Instructions for donors (optional)",
        blank=True
    )
    
    why_give_message = models.TextField(
        blank=True,
        null=True,
        help_text="Optional: Biblical message about giving"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Giving Page Content"
        verbose_name_plural = "Giving Page Content"
    
    def __str__(self):
        return "Giving Page Information"
    
    def save(self, *args, **kwargs):
        """Ensure only one GivingInfo record exists"""
        if not self.pk and GivingInfo.objects.exists():
            raise ValueError('Only one Giving Info record is allowed')
        return super().save(*args, **kwargs)


class GivingImage(models.Model):
    """
    Images for the giving page (QR codes, bank details, payment instructions, etc.).
    Can have unlimited images, each with its own caption.
    """
    giving_info = models.ForeignKey(
        GivingInfo,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Link to the main giving page"
    )
    
    image = models.ImageField(
        upload_to='giving/',
        help_text="QR code, bank details, payment instruction, etc."
    )
    
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Description for this image (e.g., 'Mobile Money QR Code')"
    )
    
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Giving Page Image"
        verbose_name_plural = "Giving Page Images"
    
    def __str__(self):
        return self.caption or f"Image {self.id}"

# ====================================================================
# CONTACT PAGE MODELS
# ====================================================================

class ImageLog(models.Model):
    """
    Central image tracking - logs all images uploaded across the site.
    Read-only in admin. Automatically created when images are uploaded.
    """
    # The actual image file
    image = models.ImageField(upload_to='image_log/')
    
    # Generic relationship to track which model/section this image belongs to
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Metadata
    section_name = models.CharField(
        max_length=100,
        help_text="Which section this image is from (Banner, Pastor, Leader, etc.)"
    )
    file_size = models.BigIntegerField(
        help_text="Image file size in bytes",
        null=True,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Image Log"
        verbose_name_plural = "Image Logs"
        indexes = [
            models.Index(fields=['section_name', '-uploaded_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.section_name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class ContactMessage(models.Model):
    """
    Contact form submissions from website visitors.
    Admin can mark as read/unread for tracking.
    """
    SUBJECT_CHOICES = [
        ('General Inquiry', 'General Inquiry'),
        ('Prayer Request', 'Prayer Request'),
        ('Event Information', 'Event Information'),
        ('Service Information', 'Service Information'),
        ('Counseling Request', 'Counseling Request'),
        ('Partnership', 'Partnership/Collaboration'),
        ('Feedback', 'Feedback/Testimony'),
        ('Volunteer', 'Volunteer Opportunity'),
        ('Media Request', 'Media/Press Request'),
        ('Other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional phone number"
    )
    subject = models.CharField(
        max_length=100,
        choices=SUBJECT_CHOICES,
        db_index=True  # PERFORMANCE: Filtering
    )
    message = models.TextField()
    
    is_read = models.BooleanField(
        default=False,
        db_index=True,  # PERFORMANCE: Quick filtering of unread
        help_text="Mark as read after reviewing"
    )
    
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True  # PERFORMANCE: Sorting
    )
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        indexes = [
            models.Index(fields=['is_read', '-submitted_at']),  # PERFORMANCE: Unread messages
            models.Index(fields=['subject', '-submitted_at']),  # PERFORMANCE: Filter by type
        ]


class Testimony(models.Model):
    """
    Testimony archive and display management.
    Display selected ones on home page carousel
    Keep full archive for pastor's book/records
    """
    name = models.CharField(max_length=200)
    testimony_text = models.TextField()
    location = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(
        upload_to='testimonies/',
        blank=True,
        null=True
    )
    
    # Display Controls
    show_on_carousel = models.BooleanField(
        default=False,
        db_index=True,
        help_text="✓ Display on home page carousel"
    )
    
    # Archive/Book Preparation
    is_approved = models.BooleanField(
        default=False,
        db_index=True,
        help_text="✓ Verified and approved (for book/records)"
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Optional: Healing, Salvation, Financial, etc. (for book organization)"
    )
    
    order = models.IntegerField(default=0)
    
    source_message = models.ForeignKey(
        'ContactMessage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimony'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimony"
        verbose_name_plural = "Testimony Archive"
        indexes = [
            models.Index(fields=['show_on_carousel', 'order']),
            models.Index(fields=['is_approved', 'category']),
        ]
    
    def __str__(self):
        carousel = "🎠" if self.show_on_carousel else ""
        approved = "✓" if self.is_approved else "⏳"
        return f"{approved}{carousel} {self.name} - {self.testimony_text[:40]}..."
    
    def create_testimony(self):
        """
        Helper method to create a Testimony from a contact message.
        Can be called from admin panel.
        """
        if self.source_message and self.source_message.subject == 'Feedback/Testimony':
            return self
        return None


class Book(models.Model):
    """
    Books available for purchase by the pastor/church.
    Each book has a picture, name, price, and buy links.
    """
    name = models.CharField(
        max_length=200,
        help_text="Book title"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in dollars (e.g., 19.99)"
    )
    image = models.ImageField(
        upload_to='books/',
        help_text="Book cover image"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Book description or summary"
    )
    
    # Buy links
    whatsapp_link = models.URLField(
        blank=True,
        null=True,
        help_text="WhatsApp chat link to purchase (e.g., https://wa.me/...)"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email to contact for purchase"
    )
    amazon = models.URLField(
        blank=True,
        null=True,
        help_text="Amazon purchase link"
    )
    is_available = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck to hide this book"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Book"
        verbose_name_plural = "Books"
        indexes = [
            models.Index(fields=['is_available', '-created_at']),
        ]
    
    def __str__(self):
        return f"📕 {self.name} - ${self.price}"


class ExchangeRate(models.Model):
    """
    Cached exchange rates (updated once daily).
    Stores conversion rates from USD to other currencies.
    """
    currency_code = models.CharField(
        max_length=3,
        unique=True,
        db_index=True,
        help_text="ISO currency code (e.g., USD, GHS, CUP, GBP)"
    )
    currency_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Currency name (e.g., US Dollar, Ghana Cedi)"
    )
    rate = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        help_text="Exchange rate from USD (e.g., 0.5 means 1 USD = 0.5 of this currency)"
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['currency_code']
        verbose_name = "Exchange Rate"
        verbose_name_plural = "Exchange Rates"
        indexes = [
            models.Index(fields=['currency_code']),
            models.Index(fields=['-last_updated']),
        ]
    
    def __str__(self):
        return f"{self.currency_code} - {self.currency_name} ({self.rate})"


class Merchandise(models.Model):
    """
    Church merchandise (t-shirts, sweaters, etc.) available for purchase.
    Each item has name, image, price, description, and buy links.
    """
    name = models.CharField(
        max_length=200,
        help_text="Merchandise name (e.g., 'TGA Church Hoodie')"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price in USD"
    )
    image = models.ImageField(
        upload_to='merchandise/',
        help_text="Product image/photo"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Product description, colors, sizes, materials, etc. (optional)"
    )
    
    # Buy links
    whatsapp_link = models.URLField(
        blank=True,
        null=True,
        help_text="WhatsApp chat link to purchase (e.g., https://wa.me/...)"
    )
    jiji_link = models.URLField(
        blank=True,
        null=True,
        help_text="Jiji marketplace link to purchase"
    )
    amazon_link = models.URLField(
        blank=True,
        null=True,
        help_text="Amazon purchase link"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Email to contact for purchase"
    )
    
    is_available = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck to hide this item"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Merchandise"
        verbose_name_plural = "Merchandise"
        indexes = [
            models.Index(fields=['is_available', '-created_at']),
        ]
    
    def __str__(self):
        return f"👕 {self.name} - ${self.price}"


# ====================================================================
# AUDIT & SECURITY MODELS
# ====================================================================

class AuditLog(models.Model):
    """
    Tracks all admin changes for security and compliance.
    Records who made what changes, when, and from where.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Created'),
        ('UPDATE', 'Updated'),
        ('DELETE', 'Deleted'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('PERMISSION_DENIED', 'Permission Denied'),
        ('FILE_UPLOAD', 'File Upload'),
    ]
    
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_repr = models.TextField(blank=True)
    changes = models.JSONField(
        default=dict,
        blank=True,
        help_text="JSON of what was changed (old_value, new_value)"
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['model_name', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"


# ====================================================================
# USER PROFILE MODEL
# ====================================================================

class UserProfile(models.Model):
    """
    Extended user profile with picture and additional info.
    Shows profile picture in admin sidebar.
    """
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        help_text="Profile picture shown in admin sidebar"
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text="User bio or short description"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"