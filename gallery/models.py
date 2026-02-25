from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Art category for organizing prints (e.g., Gothic, Surreal, Neon-Pop).
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ArtPrint(models.Model):
    """
    Represents a finished artwork available as a limited-edition print.
    Original custom model for the artist's portfolio and shop.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='prints/%Y/%m/')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prints'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size_options = models.CharField(
        max_length=200,
        help_text="e.g. A4, A3, 50x70cm – comma separated",
        blank=True
    )
    is_available = models.BooleanField(default=True)
    limited_edition = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number remaining or leave blank if unlimited"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
