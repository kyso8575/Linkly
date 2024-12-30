from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from .models import ShortenedURL
from rest_framework import status
from .serializers import ShortenedURLSerializer

BASE_URL = "http://localhost:8000/"

@api_view(['POST'])
def create_short_url_and_qr(request):
    serializer = ShortenedURLSerializer(data=request.data)
    
    if serializer.is_valid():
        instance = serializer.save()
        response_data = ShortenedURLSerializer(instance).data
        return Response(response_data, status=status.HTTP_201_CREATED if instance else status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def redirect_to_long_url(request, short_code):
    """
    short_code를 기반으로 long_url로 리다이렉트
    """
    url_entry = get_object_or_404(ShortenedURL, short_code=short_code)
    return redirect(url_entry.long_url)
