# complaints/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track_complaint, name='track_complaint'),
    
    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('complaint/<str:tracking_id>/', views.complaint_detail, name='complaint_detail'),
    path('admin-analytics/', views.dashboard_analytics, name='dashboard_analytics'),
]