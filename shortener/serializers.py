from rest_framework import serializers
from .models import ShortenedURL
from django.conf import settings
from urllib.parse import urlparse, urlunparse

class ShortenedURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    qr_image = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = ['id', 'long_url', 'short_code', 'short_url', 'qr_image']
        read_onlty_fields = ['short_code', 'qr_image', 'created_at']

    def get_short_url(self, obj):
        """Short URL 생성"""
        BASE_URL = getattr(settings, 'BASE_URL', 'http://localhost:8000/')
        return f"{BASE_URL}{obj.short_code}" if obj.short_code else None

    def get_qr_image(self, obj):
        """QR 이미지 URL 반환"""
        return obj.qr_image.url if obj.qr_image else None

    def validate_long_url(self, value):
        """URL 검증 및 스키마 자동 추가"""
        parsed_url = urlparse(value)

        # 스키마가 없는 경우 자동으로 http:// 추가
        if not parsed_url.scheme:
            value = f"http://{value}"
            parsed_url = urlparse(value)

        # netloc이 없으면 잘못된 URL
        if not parsed_url.netloc:
            raise serializers.ValidationError("Invalid URL format. Please provide a valid domain.")

        return urlunparse(parsed_url)

    def create(self, validated_data):
        """ShortenedURL 객체 생성 및 저장"""
        instance, created = ShortenedURL.objects.get_or_create(**validated_data)
        if created:
            instance.save()
        return instance
