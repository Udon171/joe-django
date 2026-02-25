from django.db import models
from django.contrib.auth.models import User


class CommissionRequest(models.Model):
    """
    Custom commission request from a client.
    Supports full CRUD: create via form, read/update in dashboard, admin delete.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('quoted', 'Quoted – Awaiting Deposit'),
        ('in_progress', 'In Progress'),
        ('revision', 'Revision Requested'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    TYPE_CHOICES = [
        ('icon', 'Icon'),
        ('logo', 'Logo'),
        ('poster', 'Poster'),
        ('portrait', 'Character Portrait'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='commissions'
    )
    title = models.CharField(
        max_length=200, help_text="Short name for your commission"
    )
    commission_type = models.CharField(
        max_length=100, choices=TYPE_CHOICES
    )
    size = models.CharField(
        max_length=100, help_text="e.g. 1080x1080px, A3 print, custom"
    )
    description = models.TextField()
    reference_images = models.ImageField(
        upload_to='commissions/references/%Y/%m/', blank=True, null=True
    )
    estimated_price = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    deposit_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    artist_notes = models.TextField(
        blank=True, help_text="Internal notes – visible only to admin"
    )
    final_file = models.FileField(
        upload_to='commissions/final/%Y/%m/', blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    def is_editable_by_user(self):
        """Check if the user can still edit this commission."""
        return self.status in ['pending', 'quoted', 'revision']

    def get_status_badge_class(self):
        """Return Bootstrap badge class for status display."""
        badges = {
            'pending': 'secondary',
            'quoted': 'warning',
            'in_progress': 'primary',
            'revision': 'danger',
            'completed': 'success',
            'cancelled': 'dark',
        }
        return badges.get(self.status, 'secondary')
