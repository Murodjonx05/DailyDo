from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Plan, Badge, Board

admin.site.register(Board)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Plan)
admin.site.register(Badge)
