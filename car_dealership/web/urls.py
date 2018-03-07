from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('cars/', views.cars_page, name='cars'),
    path('car_dy/', views.cars, name='car_dy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
