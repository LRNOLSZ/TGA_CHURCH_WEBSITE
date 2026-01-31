from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import (
    HomeBanner, HeadPastor, Leader, PhotoGallery, 
    Sermon, Event, GivingImage, ImageLog
)


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
