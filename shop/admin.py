from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('art_print', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'is_completed', 'created_at')
    list_filter = ('status', 'is_completed')
    search_fields = ('user__username', 'stripe_session_id')
    inlines = [OrderItemInline]
