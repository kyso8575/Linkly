from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer



# URL 단축 및 QR 생성 뷰 (POST)
class CreateShortURLAndQRView(APIView):
    """
    POST 요청을 통해 ShortenedURL을 생성하고 QR 코드를 반환합니다.
    """
    def post(self, request):
        serializer = ShortenedURLSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
            response_data = ShortenedURLSerializer(instance).data
            return Response(response_data, status=status.HTTP_201_CREATED if instance else status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Short URL 리디렉션 뷰 (GET)
class RedirectToLongURLView(APIView):
    """
    short_code를 사용해 long_url로 리다이렉트합니다.
    """
    def get(self, request, short_code):
        url_entry = get_object_or_404(ShortenedURL, short_code=short_code)
        return redirect(url_entry.long_url)
