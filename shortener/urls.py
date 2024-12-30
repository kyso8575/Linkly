from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.create_short_url_and_qr, name='generate'),
    path('<str:short_code>/', views.redirect_to_long_url, name='redirect_to_long_url'),
] 