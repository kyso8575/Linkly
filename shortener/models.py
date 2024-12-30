import string
import qrcode
from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
from urllib.parse import urlparse
from django.core.exceptions import ValidationError

# Base62 문자 집합
BASE62 = string.ascii_letters + string.digits

# Base62 인코딩 함수
def base62_encode(num):
    if num == 0:
        return BASE62[0]
    
    result = []
    while num:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])
    
    return ''.join(reversed(result))


class ShortenedURL(models.Model):
    long_url = models.CharField(max_length=100, unique=True)
    short_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    qr_image = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        """
        객체가 저장되기 전에 URL 유효성을 검사합니다.
        """
        parsed_url = urlparse(self.long_url)

        # 스키마가 없으면 http://를 추가
        if not parsed_url.scheme:
            self.long_url = f"http://{self.long_url}"
            parsed_url = urlparse(self.long_url)
        
        # netloc(도메인)이 없으면 오류 발생
        if not parsed_url.netloc:
            
            raise ValidationError("Invalid URL format. Please provide a valid domain.")

    def save(self, *args, **kwargs):
        """
        저장 전에 URL을 검증하고 short_code 및 qr_image를 생성합니다.
        """
        is_new = self._state.adding  # 객체가 새로 생성되었는지 확인

        # URL 유효성 검사
        self.clean()
        
        super().save(*args, **kwargs)  # 첫 번째 저장 (id 생성)
        
        if is_new:
            updated = False
            
            # 객체가 새로 생성되었을 때 short_code와 qr_image 생성
            if not self.short_code:
                self.short_code = self.generate_short_code()
                updated = True
            
            if not self.qr_image:
                self.qr_image = self.generate_qr_code()
                updated = True
            
            if updated:
                # 필드 업데이트
                super().save(update_fields=['short_code', 'qr_image'])
    
    def generate_short_code(self):
        """ID를 Base62로 인코딩해 short_code 생성"""
        if not self.id:
            super().save()
        return base62_encode(self.id)
    
    def generate_qr_code(self):
        """short_url을 QR 코드로 변환해 저장"""
        # BASE_URL이 설정에 없다면 기본값 사용
        short_url = f"{settings.BASE_URL}{self.short_code}" if self.short_code else settings.BASE_URL

        qr = qrcode.make(short_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        return ContentFile(buffer.getvalue(), name=f"{self.short_code}.png")
    
    def __str__(self):
        return f"{self.short_code} → {self.long_url}"
