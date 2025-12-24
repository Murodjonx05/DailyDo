from django.contrib import admin
from django.forms import TextInput
from .models import SiteConfig
from django.db import models

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'site_name')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        # Перечисляем здесь только те поля, которые должны быть Color Picker
        color_fields = ['nav_color', 'another_color_field'] 
        
        if db_field.name in color_fields:
            kwargs['widget'] = TextInput(attrs={
                'type': 'color',
                'style': 'height: 40px; width: 100px; cursor: pointer;'
            })
        return super().formfield_for_dbfield(db_field, request, **kwargs)