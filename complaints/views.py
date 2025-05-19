from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Complaint, Category, Response
from .forms import ComplaintForm, TrackingForm, ResponseForm
from django.utils import timezone
from .models import Complaint, Category, Response, Agency
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField, Q
from django.db.models.fields import DurationField

def home(request):
    
    complaint_form = ComplaintForm()
    tracking_form = TrackingForm()
    
    
    categories = Category.objects.all().order_by('name')
    
    if request.method == 'POST':
        if 'submit_complaint' in request.POST:
            complaint_form = ComplaintForm(request.POST, request.FILES)
            if complaint_form.is_valid():
                complaint = complaint_form.save()
                # Return tracking ID via JSON for the popup
                return JsonResponse({
                    'success': True,
                    'tracking_id': complaint.tracking_id,
                    'message': 'Your complaint has been submitted successfully. Please save this tracking ID.'
                })
            else:
                # Return form errors via JSON
                return JsonResponse({
                    'success': False,
                    'errors': complaint_form.errors
                })
    
    context = {
        'complaint_form': complaint_form,
        'tracking_form': tracking_form,
        'categories': categories,
    }
    return render(request, 'complaints/home.html', context)

def track_complaint(request):
    if request.method == 'POST':
        tracking_form = TrackingForm(request.POST)
        if tracking_form.is_valid():
            tracking_id = tracking_form.cleaned_data['tracking_id']
            try:
                complaint = Complaint.objects.get(tracking_id=tracking_id)
                return render(request, 'complaints/track_detail.html', {
                    'complaint': complaint,
                    'responses': complaint.responses.all().order_by('-created_at')
                })
            except Complaint.DoesNotExist:
                messages.error(request, 'Complaint not found. Please check the tracking ID.')
                return redirect('home')
    return redirect('home')

def admin_dashboard(request):
    """Dashboard for government officials"""
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        complaints = complaints.filter(category_id=category_id)
    
    # Get statistics for dashboard
    total_complaints = Complaint.objects.count()
    open_complaints = Complaint.objects.exclude(status__in=['resolved', 'closed']).count()
    resolved_complaints = Complaint.objects.filter(status__in=['resolved', 'closed']).count()
    
    # Count unique categories instead of agencies if Agency model isn't available
    agency_count = Category.objects.values('agency').distinct().count()
    
    context = {
        'complaints': complaints,
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'resolved_complaints': resolved_complaints,
        'agency_count': agency_count,
        'status_choices': Complaint.STATUS_CHOICES,
        'categories': Category.objects.all(),
        'current_date': timezone.now(),
    }
    return render(request, 'complaints/admin/dashboard.html', context)

def complaint_detail(request, tracking_id):
    complaint = get_object_or_404(Complaint, tracking_id=tracking_id)
    responses = complaint.responses.all().order_by('-created_at')
    
    if request.method == 'POST':
        # Handle status update
        if 'update_status' in request.POST:
            new_status = request.POST.get('status')
            if new_status in dict(Complaint.STATUS_CHOICES):
                complaint.status = new_status
                complaint.save()
                messages.success(request, f'Status updated to {complaint.get_status_display()}')
        
        # Handle new response submission
        elif 'submit_response' in request.POST:
            response_form = ResponseForm(request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.complaint = complaint
                response.save()
                messages.success(request, 'Response submitted successfully')
                return redirect('complaint_detail', tracking_id=tracking_id)
    
    response_form = ResponseForm()
    
    context = {
        'complaint': complaint,
        'responses': responses,
        'response_form': response_form,
        'status_choices': Complaint.STATUS_CHOICES,
    }
    return render(request, 'complaints/admin/complaint_detail.html', context)

# complaints/views.py (add a new function)

def dashboard_analytics(request):
    """Analytics dashboard for admins"""
    # Get complaint statistics
    total_complaints = Complaint.objects.count()
    open_complaints = Complaint.objects.exclude(status__in=['resolved', 'closed']).count()
    resolved_complaints = Complaint.objects.filter(status__in=['resolved', 'closed']).count()
    
    # Calculate resolution rate
    resolution_rate = 0
    if total_complaints > 0:
        resolution_rate = round((resolved_complaints / total_complaints) * 100)
    
    # Calculate average resolution time (in days) without ExpressionWrapper
    avg_resolution_time = 0
    resolved_complaints_qs = Complaint.objects.filter(status__in=['resolved', 'closed'])
    
    if resolved_complaints_qs.exists():
        total_days = 0
        count = 0
        
        for complaint in resolved_complaints_qs:
            if complaint.updated_at and complaint.created_at:
                days = (complaint.updated_at - complaint.created_at).days
                total_days += days
                count += 1
        
        if count > 0:
            avg_resolution_time = round(total_days / count)
    
    # Dummy satisfaction rate (in a real app, this would come from user feedback)
    satisfaction_rate = 85
    
    # Get category distribution
    category_stats = Category.objects.annotate(count=Count('complaints')).order_by('-count')
    
    # Get status distribution
    status_stats = []
    for status_code, status_name in Complaint.STATUS_CHOICES:
        count = Complaint.objects.filter(status=status_code).count()
        status_stats.append({
            'status': status_code,
            'name': status_name,
            'count': count
        })
    
    # Get monthly complaints data (for the current year)
    current_year = timezone.now().year
    monthly_complaints = []
    monthly_resolved = []
    
    for month in range(1, 13):
        month_count = Complaint.objects.filter(
            created_at__year=current_year,
            created_at__month=month
        ).count()
        
        resolved_count = Complaint.objects.filter(
            created_at__year=current_year,
            created_at__month=month,
            status__in=['resolved', 'closed']
        ).count()
        
        monthly_complaints.append(month_count)
        monthly_resolved.append(resolved_count)
    
    context = {
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'resolved_complaints': resolved_complaints,
        'resolution_rate': resolution_rate,
        'avg_resolution_time': avg_resolution_time,
        'satisfaction_rate': satisfaction_rate,
        'category_stats': category_stats,
        'status_stats': status_stats,
        'monthly_complaints': monthly_complaints,
        'monthly_resolved': monthly_resolved,
        'current_date': timezone.now(),
    }
    return render(request, 'complaints/admin/analytics.html', context)