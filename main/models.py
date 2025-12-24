from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class MyUser(AbstractUser):
    """Custom User model with profile and role-based access."""
    ROLE_CHOICES = (
        ('user', _('User')),
        ('admin', _('Admin')),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    boards = models.ManyToManyField('Board', related_name='members', blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self):
        super().clean()
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError({'avatar': _('Avatar file size must be less than 2MB.')})

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error saving user {self.username}: {e}")
            raise ValidationError(_('Error saving profile.'))


class Badge(models.Model):
    """Achievement badges for plans and boards."""
    badge = models.ImageField(upload_to='badges/')
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024)

    def __str__(self):
        return self.name


class Board(models.Model):
    """Workspace to group related plans."""
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_boards'
    )

    def __str__(self):
        return self.name


class Plan(models.Model):
    """Hierarchical task model with configurable limits."""
    MAX_SUB_PLANS = 5
    MAX_DEPTH = 5

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='plans', null=True, blank=True)

    name = models.CharField(max_length=128)
    description = models.TextField(max_length=1024, blank=True)
    priority = models.PositiveIntegerField(default=1)
    badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(default=False)

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    last_check_update = models.DateTimeField(auto_now=True)
    last_check_complete = models.DateTimeField(null=True, blank=True, editable=False)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_plans')

    def get_depth(self):
        """Iteratively determines the depth of the plan to avoid RecursionError."""
        depth = 1
        curr = self.parent
        visited = set()

        while curr:
            if curr.pk in visited or depth > self.MAX_DEPTH:
                break
            visited.add(curr.pk)
            depth += 1
            curr = curr.parent
        return depth

    def clean(self):
        """Enforces date ranges, hierarchy depth, and child limits."""
        # 1. Date Validation
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': _("End date cannot be earlier than start date.")})

        # 2. Hierarchy Logic
        if self.parent:
            # Prevent self-parenting
            if self.pk and self.pk == self.parent_id:
                raise ValidationError({'parent': _("A plan cannot be its own parent.")})

            # Check Depth
            if self.parent.get_depth() >= self.MAX_DEPTH:
                raise ValidationError({'parent': _(f"Hierarchy cannot exceed {self.MAX_DEPTH} levels.")})

            # Check Capacity (Exclude self if already exists)
            if self.parent.sub_plans.exclude(pk=self.pk).count() >= self.MAX_SUB_PLANS:
                raise ValidationError({'parent': _(f"Parent has reached the limit of {self.MAX_SUB_PLANS} sub-plans.")})

    def save(self, *args, **kwargs):
        # Auto-calculate duration
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + timedelta(days=1)

        # Track completion time
        if self.is_complete and not self.last_check_complete:
            self.last_check_complete = timezone.now()
        elif not self.is_complete:
            self.last_check_complete = None

        super().save(*args, **kwargs)

    def __str__(self):
        icon = "✔️" if self.is_complete else "❌"
        return f"{icon} {self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['priority']),
            models.Index(fields=['is_complete']),
            models.Index(fields=['start_date']),
        ]
        ordering = ['-priority', 'start_date']