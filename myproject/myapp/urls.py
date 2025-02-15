from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('ticket_booking/', views.ticket_booking, name='ticket_booking'),
    path('passenger_details/<int:bus_id>/', views.passenger_details, name='passenger_details'),
    path('confirm_booking/<int:bus_id>/', views.confirm_booking, name='confirm_booking'),
    path('booking_success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('add_money/', views.add_money, name='add_money'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_bus/', views.add_bus, name='add_bus'),
]