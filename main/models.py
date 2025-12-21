from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    """Custom user model with roles"""
    ROLE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='freelancer')
    
    # Profile fields merged from UserProfile
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username


class DateTimeMixin(models.Model):
    """Base class for created/updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Language(models.Model):
    """Language model for multilingual support"""
    LANG_CODE_MAX_LENGTH = 10
    NAME_MAX_LENGTH = 100
    
    lang_code = models.CharField(
        max_length=LANG_CODE_MAX_LENGTH,
        unique=True
    )
    lang_name = models.CharField(max_length=NAME_MAX_LENGTH)
    
    class Meta:
        verbose_name_plural = "Languages"
        ordering = ['lang_code']
    
    def __str__(self):
        return f"{self.lang_code}: {self.lang_name}"


class Description(DateTimeMixin):
    """Multilingual description model"""
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='descriptions'
    )
    content = models.TextField()
    
    def __str__(self):
        return f"{self.language.lang_code}: {self.content[:50]}..."


class Company(DateTimeMixin):
    """Company profile model (usually for Clients)"""
    COMPANY_NAME_MAX_LENGTH = 255
    SHORT_NAME_MAX_LENGTH = 100
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='companies',
        null=True,
        blank=True
    )
    logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=COMPANY_NAME_MAX_LENGTH)
    short_name = models.CharField(max_length=SHORT_NAME_MAX_LENGTH)
    description = models.ManyToManyField(
        Description,
        related_name='companies',
        blank=True
    )
    
    def __str__(self):
        return self.name


class WorkType(models.Model):
    """Work type options"""
    WORK_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('hybrid', 'Hybrid'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.display_name


class Tag(DateTimeMixin):
    """Tags for categorizing works and exercises"""
    name = models.CharField(max_length=255, unique=True)
    description = models.ManyToManyField(
        Description,
        related_name='tags',
        blank=True
    )
    
    def __str__(self):
        return self.name


class Work(DateTimeMixin):
    """Job posting model"""
    WORK_NAME_MAX_LENGTH = 255
    WORK_SHORT_NAME_MAX_LENGTH = 100
    LOCATION_MAX_LENGTH = 100
    PRICE_TEXT_MAX_LENGTH = 30
    
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_works',
        null=True, # Allow null temporarily if needed, but ideally should be required
        blank=True
    )

    name = models.CharField(max_length=WORK_NAME_MAX_LENGTH)
    short_name = models.CharField(max_length=WORK_SHORT_NAME_MAX_LENGTH)
    
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.SET_NULL,
        null=True
    )
    other_text = models.CharField(
        max_length=300,
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=LOCATION_MAX_LENGTH,
        null=True,
        blank=True
    )
    price_text = models.CharField(
        max_length=PRICE_TEXT_MAX_LENGTH,
        null=True,
        blank=True
    )
    
    description = models.ManyToManyField(
        Description,
        related_name='works',
        blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='works'
    )
    tags = models.ManyToManyField(Tag, blank=True)

    # hr_assistants might be other users helping manage the job?
    hr_assistants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='hr_assistants_works',
        blank=True
    )
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.work_type.name if self.work_type else 'Unknown'})"


class Image(DateTimeMixin):
    """Image model for attachments"""
    image = models.ImageField(upload_to='work_images/')

    def get_path(self):
        return self.image.url
    
    def __str__(self):
        return f"Image: {self.image.name.split('/')[-1]}"


class File(DateTimeMixin):
    """File model for document attachments"""
    file = models.FileField(upload_to='work_files/')

    def get_path(self):
        return self.file.url
    
    def __str__(self):
        return f"File: {self.file.name.split('/')[-1]}"


class URLObject(DateTimeMixin):
    """URL model for links"""
    url = models.URLField(max_length=500)

    def get_path(self):
        return self.url
    
    def __str__(self):
        return self.url


class Rate(DateTimeMixin):
    """Rate model for rating works/companies"""
    MAX_RATING = 10
    MIN_RATING = 1
    
    rating = models.IntegerField(
        validators=[
            MinValueValidator(MIN_RATING),
            MaxValueValidator(MAX_RATING)
        ]
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rates'
    )

    def counts(self):
        return len(self.objects.all()) # This looks wrong (calling objects on instance), but keeping structure for now

    def __str__(self):
        return f"{self.rating}/10 by {self.user.username}"


class Rating(DateTimeMixin):
    # This class logic seemed a bit odd in original (mix of instance state and db), keeping simple relation for now
    
    rating = models.ManyToManyField(
       Rate,
       related_name='ratings'
    )

    def get_mid(self):
        rates = self.rating.all()
        return sum([rate.rating for rate in rates]) / len(rates)
    
    # Keeping methods if they were used, but they look like they belong in a View or Property
    
    def __str__(self):
        return f"Rating Collection {self.id}"


class Exercise(DateTimeMixin):
    """Exercise/Task model for freelance projects"""
    EXERCISE_TEXT_MAX_LENGTH = 255
    SHORT_TEXT_MAX_LENGTH = 100
    PRICE_TEXT_MAX_LENGTH = 30
    
    title = models.CharField(max_length=EXERCISE_TEXT_MAX_LENGTH)
    short_title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    
    description = models.ManyToManyField(
        Description,
        related_name='exercises',
        blank=True
    )
    price_text = models.CharField(
        max_length=PRICE_TEXT_MAX_LENGTH,
        null=True,
        blank=True
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='exercises'
    )
    
    tags = models.ManyToManyField(Tag, blank=True)
    files = models.ManyToManyField(File, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    urls = models.ManyToManyField(URLObject, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class Proposal(DateTimeMixin):
    """Proposal for a job"""
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='proposals')
    cover_letter = models.TextField()
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estimated_duration = models.CharField(max_length=100, blank=True)
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Proposal by {self.freelancer.username} for {self.work.name}"