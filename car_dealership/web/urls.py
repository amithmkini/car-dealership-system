from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('cars/', views.cars_page, name='cars'),
    path('car_dy/', views.cars, name='car_dy'),
    path('car_s/', views.car_search, name='search'),
    path('car/<int:cid>', views.car_details, name='details'),
    path('testdrive/<int:cid>', views.testdrive, name="testdrive"),
    path('ordercar/<int:cid>', views.order_car, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
