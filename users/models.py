from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Extends the built-in User model with additional fields.
    One-to-one relationship ensures each user has exactly one profile.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    wishlist = models.ManyToManyField(
        'gallery.ArtPrint',
        related_name='wishlisted_by',
        blank=True,
        verbose_name='Wishlist',
        help_text='Art prints the user has favourited for later.'
    )
    purchased_prints = models.ManyToManyField(
        'gallery.ArtPrint',
        related_name='purchased_by',
        blank=True,
        verbose_name='Purchased Prints'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"Profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Auto-create Profile when a new User is registered."""
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
