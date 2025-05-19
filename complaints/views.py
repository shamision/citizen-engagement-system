from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Complaint, Category, Response
from .forms import ComplaintForm, TrackingForm, ResponseForm

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

# Admin views for government officials
def admin_dashboard(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        complaints = complaints.filter(status=status)
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        complaints = complaints.filter(category_id=category_id)
    
    context = {
        'complaints': complaints,
        'status_choices': Complaint.STATUS_CHOICES,
        'categories': Category.objects.all(),
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
    """Simple analytics dashboard for admins"""
    # Get complaint statistics
    total_complaints = Complaint.objects.count()
    open_complaints = Complaint.objects.exclude(status__in=['resolved', 'closed']).count()
    resolved_complaints = Complaint.objects.filter(status__in=['resolved', 'closed']).count()
    
    # Get category distribution
    category_stats = []
    categories = Category.objects.all()
    for category in categories:
        category_count = Complaint.objects.filter(category=category).count()
        if category_count > 0:
            category_stats.append({
                'name': category.name,
                'count': category_count,
                'percentage': (category_count / total_complaints) * 100 if total_complaints > 0 else 0
            })
    
    # Get status distribution
    status_stats = []
    status_choices = dict(Complaint.STATUS_CHOICES)
    for status_value, status_display in status_choices.items():
        status_count = Complaint.objects.filter(status=status_value).count()
        if status_count > 0:
            status_stats.append({
                'name': status_display,
                'count': status_count,
                'percentage': (status_count / total_complaints) * 100 if total_complaints > 0 else 0
            })
    
    # Calculate response time metrics (in days)
    import datetime
    response_times = []
    resolved_complaints_objects = Complaint.objects.filter(status__in=['resolved', 'closed'])
    for complaint in resolved_complaints_objects:
        created_date = complaint.created_at.date()
        updated_date = complaint.updated_at.date()
        days_to_resolve = (updated_date - created_date).days
        response_times.append(days_to_resolve)
    
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0
    
    context = {
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'resolved_complaints': resolved_complaints,
        'category_stats': category_stats,
        'status_stats': status_stats,
        'avg_response_time': avg_response_time,
    }
    return render(request, 'complaints/admin/analytics.html', context)