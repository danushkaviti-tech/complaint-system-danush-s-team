from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'subject')

    # Optional: ensure admin save triggers signals
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
