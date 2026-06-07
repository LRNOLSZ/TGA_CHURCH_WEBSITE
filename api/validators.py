"""
Security validators for file uploads
"""
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
import os
import re

# Allowed file extensions for images
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

# Allowed file extensions for documents
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

# Magic bytes (file signatures) for allowed image types
# These are the actual bytes at the start of a real image file — cannot be faked by renaming
IMAGE_MAGIC_BYTES = [
    (b'\xff\xd8\xff', 'JPEG'),                    # JPEG/JPG
    (b'\x89PNG\r\n\x1a\n', 'PNG'),                # PNG
    (b'GIF87a', 'GIF'),                            # GIF87
    (b'GIF89a', 'GIF'),                            # GIF89
    (b'RIFF', 'WebP'),                             # WebP (check WEBP marker too)
]


def _check_magic_bytes(file: UploadedFile):
    """
    Read the first 12 bytes of the file and verify it matches a known image signature.
    This catches malware/executables disguised as image files.
    """
    file.seek(0)
    header = file.read(12)
    file.seek(0)

    for magic, label in IMAGE_MAGIC_BYTES:
        if header.startswith(magic):
            # Extra check for WebP: bytes 8-12 must be "WEBP"
            if label == 'WebP' and header[8:12] != b'WEBP':
                continue
            return  # Valid image signature found

    raise ValidationError(
        "File content does not match a valid image. "
        "Uploading files disguised as images is not allowed."
    )


def validate_image_file(file: UploadedFile):
    """
    Validate image uploads:
    - Check file size
    - Check file extension
    - Check MIME type header
    - Check actual file magic bytes (prevents malware disguised as images)
    """
    if not file:
        return

    # Check file size
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(
            f"Image file too large. Maximum size is 10MB, got {file.size / (1024*1024):.1f}MB"
        )

    # Get file extension
    _, ext = os.path.splitext(file.name)
    ext = ext.lower().lstrip('.')

    # Check extension
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Invalid image format. Allowed formats: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )

    # Check MIME type header (client-supplied — not fully trusted, but filters careless attempts)
    valid_mime_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
    if hasattr(file, 'content_type') and file.content_type not in valid_mime_types:
        raise ValidationError(f"Invalid image MIME type: {file.content_type}")

    # Check actual file content (magic bytes) — this is the real security check
    _check_magic_bytes(file)


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
    _, ext = os.path.splitext(file.name)
    ext = ext.lower().lstrip('.')

    # Check extension
    if ext not in ALLOWED_DOCUMENT_EXTENSIONS:
        raise ValidationError(
            f"Invalid document format. Allowed formats: {', '.join(ALLOWED_DOCUMENT_EXTENSIONS)}"
        )


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent directory traversal and injection attacks.
    - Strips null bytes
    - Removes path separators (both / and \\)
    - Explicitly removes .. sequences
    - Removes special characters
    - Limits length
    """
    # Strip null bytes (can confuse file systems)
    filename = filename.replace('\x00', '')

    # Take only the base name — strips any path prefix like ../../
    filename = os.path.basename(filename)

    # Explicitly remove any remaining .. sequences
    filename = filename.replace('..', '')

    # Remove special characters, keep only alphanumeric, dots, hyphens, underscores
    filename = re.sub(r'[^\w\s.-]', '', filename)

    # Collapse multiple dots (prevents tricks like file....jpg)
    filename = re.sub(r'\.{2,}', '.', filename)

    # Limit length
    name, ext = os.path.splitext(filename)
    name = name[:50]

    return name + ext
