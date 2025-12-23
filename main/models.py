from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)

class MyUser(AbstractUser):
    """Custom user model with roles"""
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    # Profile fields merged from UserProfile
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),  # Index for username lookups
            models.Index(fields=['email']),      # Index for email lookups
            models.Index(fields=['role']),       # Index for role-based queries
            models.Index(fields=['is_active']),  # Index for active user queries
            models.Index(fields=['username', 'email']),  # Composite index for common queries
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def clean(self):
        """Add validation for avatar file size and type"""
        super().clean()

        if self.avatar:
            # Validate file size (max 2MB)
            max_size = 2 * 1024 * 1024  # 2MB
            if self.avatar.size > max_size:
                raise ValidationError({
                    'avatar': _('Avatar file size must be less than 2MB.')
                })

            # Validate file type
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = self.avatar.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError({
                    'avatar': _('Only JPG, JPEG, PNG, and GIF files are allowed.')
                })

    def save(self, *args, **kwargs):
        """Add error handling for avatar upload"""
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            # Log the error and provide user-friendly message
            logger.error(f"Error saving user {self.username}: {str(e)}")
            raise ValidationError({
                'avatar': _('There was an error saving your profile. Please try again.')
            })
