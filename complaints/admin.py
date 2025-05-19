from django.contrib import admin
from .models import Agency, Category, Complaint, Response

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency')
    list_filter = ('agency',)
    search_fields = ('name', 'description')

class ResponseInline(admin.TabularInline):
    model = Response
    extra = 0

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'subject', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('tracking_id', 'subject', 'description', 'name', 'email')
    readonly_fields = ('tracking_id', 'created_at', 'updated_at')
    inlines = [ResponseInline]

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'responder_name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('complaint__tracking_id', 'content', 'responder_name')