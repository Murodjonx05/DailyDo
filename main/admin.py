from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Language, Description, Company, WorkType, Tag, 
    Work, Image, File, URLObject, Rate, Rating, Exercise, Proposal
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'bio', 'avatar', 'phone_number', 'location')}),
    )

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'work_type', 'is_active', 'created_at')
    list_filter = ('work_type', 'is_active', 'created_at')
    search_fields = ('name', 'description__content')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'work', 'hourly_rate', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')

# Register other models simply
admin.site.register(Language)
admin.site.register(Description)
admin.site.register(WorkType)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(File)
admin.site.register(URLObject)
admin.site.register(Rate)
admin.site.register(Rating)
admin.site.register(Exercise)
