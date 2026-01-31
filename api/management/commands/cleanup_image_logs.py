"""
Management command to clean up orphaned ImageLog entries
(entries referencing deleted objects)
"""
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from api.models import ImageLog, Event, HomeBanner, HeadPastor, Leader, PhotoGallery, Sermon, Branch, Merchandise, GivingImage


class Command(BaseCommand):
    help = 'Clean up orphaned ImageLog entries that reference deleted objects'

    def handle(self, *args, **options):
        """Delete ImageLog entries for non-existent objects"""
        models_to_check = [
            Event, HomeBanner, HeadPastor, Leader, PhotoGallery, 
            Sermon, Branch, Merchandise, GivingImage
        ]
        
        deleted_count = 0
        
        for model in models_to_check:
            content_type = ContentType.objects.get_for_model(model)
            
            # Find all ImageLog entries for this model
            image_logs = ImageLog.objects.filter(content_type=content_type)
            
            for log in image_logs:
                # Try to get the object - if it doesn't exist, delete the log
                if not model.objects.filter(id=log.object_id).exists():
                    self.stdout.write(
                        f'Deleting orphaned ImageLog: {log.section_name} (ID: {log.object_id})'
                    )
                    log.delete()
                    deleted_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} orphaned ImageLog entries')
        )
