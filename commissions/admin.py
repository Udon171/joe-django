from django.contrib import admin
from .models import CommissionRequest


@admin.register(CommissionRequest)
class CommissionRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'commission_type', 'status', 'estimated_price', 'deposit_paid', 'created_at')
    list_filter = ('status', 'commission_type', 'deposit_paid')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
