"""
Security validators for file uploads
"""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
import os

# Allowed file extensions for images
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

# Allowed file extensions for documents
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image_file(file: UploadedFile):
    """
    Validate image uploads:
    - Check file extension
    - Check file size
    - Check MIME type
    """
    if not file:
        return
    
    # Check file size
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            f"Image file too large. Maximum size is 5MB, got {file.size / (1024*1024):.1f}MB"
        )
    
    # Get file extension
    name, ext = os.path.splitext(file.name)
    ext = ext.lower().lstrip('.')
    
    # Check extension
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Invalid image format. Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )
    
    # Check MIME type
    valid_mime_types = {
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp'
    }
    if hasattr(file, 'content_type') and file.content_type not in valid_mime_types:
        raise ValidationError(
            f"Invalid image MIME type: {file.content_type}"
        )


def validate_document_file(file: UploadedFile):
    """
    Validate document uploads:
    - Check file extension
    - Check file size
    """
    if not file:
        return
    
    # Check file size
    if file.size > MAX_DOCUMENT_SIZE:
        raise ValidationError(
            f"Document file too large. Maximum size is 10MB, got {file.size / (1024*1024):.1f}MB"
        )
    
    # Get file extension
    name, ext = os.path.splitext(file.name)
    ext = ext.lower().lstrip('.')
    
    # Check extension
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            f"Invalid document format. Allowed formats: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
        )


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and other attacks
    """
    import re
    # Remove any path separators and special characters
    filename = os.path.basename(filename)
    # Remove special characters, keep only alphanumeric, dots, hyphens, underscores
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Limit length
    name, ext = os.path.splitext(filename)
    name = name[:50]  # Limit filename to 50 chars
    return name + ext
