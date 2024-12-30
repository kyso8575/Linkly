from django.contrib import admin
from .models import ShortenedURL

# @admin.register(ShortenedURL)
# class ShortenedURLAdmin(admin.ModelAdmin):
#     list_display = ('long_url', 'short_code', 'qr_image', 'created_at')
#     readonly_fields = ('short_code', 'qr_image')
