from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .models import (
    HomeBanner, HeadPastor, Leader, PhotoGallery,
    Sermon, Event, GivingImage, ImageLog, Branch, Country, Region, Merchandise, Book, UserProfile
)
from .country_coordinates import COUNTRY_COORDINATES
from .region_data import REGION_DATA


def log_image_upload(sender, instance, created, **kwargs):
    """
    Automatically create ImageLog entry when an image is uploaded.
    """
    if not created:
        return  # Only log on creation, not updates
    
    # Map model to section name
    section_mapping = {
        HomeBanner: 'Home Banner',
        HeadPastor: 'Head Pastor',
        Leader: 'Church Leader',
        PhotoGallery: 'Photo Gallery',
        Sermon: 'Sermon',
        Event: 'Event',
        GivingImage: 'Giving Page',
        Branch: 'Branch',
        Merchandise: 'Merchandise',
        Book: 'Book',
    }
    
    section_name = section_mapping.get(sender, sender.__name__)
    
    # Determine which field contains the image
    image_field = None
    if hasattr(instance, 'image'):
        image_field = instance.image
    elif hasattr(instance, 'profile_picture'):
        image_field = instance.profile_picture
    
    # Only log if there's actually an image
    if image_field and image_field.name:
        content_type = ContentType.objects.get_for_model(sender)
        
        try:
            file_size = image_field.size if hasattr(image_field, 'size') else None
            
            ImageLog.objects.create(
                image=image_field,
                content_type=content_type,
                object_id=instance.id,
                section_name=section_name,
                file_size=file_size
            )
        except Exception as e:
            # Silently fail if logging doesn't work - don't break the upload
            print(f"Error logging image: {e}")


# Register signals for all models with images
post_save.connect(log_image_upload, sender=HomeBanner)
post_save.connect(log_image_upload, sender=HeadPastor)
post_save.connect(log_image_upload, sender=Leader)
post_save.connect(log_image_upload, sender=PhotoGallery)
post_save.connect(log_image_upload, sender=Sermon)
post_save.connect(log_image_upload, sender=Event)
post_save.connect(log_image_upload, sender=GivingImage)
post_save.connect(log_image_upload, sender=Branch)
post_save.connect(log_image_upload, sender=Merchandise)
post_save.connect(log_image_upload, sender=Book)


# ====================================================================
# DELETE SIGNALS - Clean up orphaned ImageLog entries
# ====================================================================

def cleanup_image_logs_on_delete(sender, instance, **kwargs):
    """
    Delete associated ImageLog entries when a model with images is deleted.
    This prevents orphaned image logs from non-existent objects.
    """
    content_type = ContentType.objects.get_for_model(sender)
    ImageLog.objects.filter(
        content_type=content_type,
        object_id=instance.id
    ).delete()


# Register delete signals for all models with images
pre_delete.connect(cleanup_image_logs_on_delete, sender=HomeBanner)
pre_delete.connect(cleanup_image_logs_on_delete, sender=HeadPastor)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Leader)
pre_delete.connect(cleanup_image_logs_on_delete, sender=PhotoGallery)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Sermon)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Event)
pre_delete.connect(cleanup_image_logs_on_delete, sender=GivingImage)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Branch)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Merchandise)
pre_delete.connect(cleanup_image_logs_on_delete, sender=Book)


# ====================================================================
# USER PROFILE AUTO-CREATE
# ====================================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create UserProfile when a new User is created"""
    if created:
        UserProfile.objects.get_or_create(user=instance)


# ====================================================================
# COUNTRY COORDINATE AUTO-POPULATION
# ====================================================================

def populate_country_coordinates(sender, instance, **kwargs):
    """
    Auto-fill Country.latitude/longitude from the static reference dataset
    so admins never enter coordinates manually.
    """
    coords = COUNTRY_COORDINATES.get(instance.name)
    if coords:
        instance.latitude, instance.longitude = coords


pre_save.connect(populate_country_coordinates, sender=Country)


# ====================================================================
# COUNTRY REGION AUTO-POPULATION
# ====================================================================

def populate_country_regions(sender, instance, **kwargs):
    """
    Auto-create Region rows from the static reference dataset the moment
    a Country is saved, so admins never create regions manually. Runs on
    every save (not just creation) so re-saving a Country tops up any
    regions added to REGION_DATA later, with no migration needed.
    """
    for region_name in REGION_DATA.get(instance.name, []):
        Region.objects.get_or_create(country=instance, name=region_name)


post_save.connect(populate_country_regions, sender=Country)
