from django.db import models
import uuid
import datetime

class Agency(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Agencies"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="categories")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    # Generate a unique ID
    def generate_tracking_id():
        # Format: CE-Year-Random 6 digits
        year = datetime.datetime.now().year
        random_digits = uuid.uuid4().hex[:6].upper()
        return f"CE-{year}-{random_digits}"
    
    tracking_id = models.CharField(max_length=20, default=generate_tracking_id, unique=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="complaints")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tracking_id} - {self.subject}"

class Response(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    responder_name = models.CharField(max_length=100)
    responder_title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.complaint.tracking_id}"