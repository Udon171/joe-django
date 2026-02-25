from django.db import models
from django.contrib.auth.models import User
from gallery.models import ArtPrint


class Order(models.Model):
    """
    Represents a completed or pending purchase of art prints.
    Created after Stripe Checkout session initiation.
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders'
    )
    stripe_session_id = models.CharField(max_length=200, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} – {self.status}"

    def get_total_display(self):
        return f"€{self.total_amount:.2f}"


class OrderItem(models.Model):
    """
    Individual line item within an order.
    Stores a snapshot of price at purchase time.
    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    art_print = models.ForeignKey(
        ArtPrint, on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        title = self.art_print.title if self.art_print else 'Unknown'
        return f"{self.quantity} × {title}"
