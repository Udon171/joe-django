from django.contrib import admin
from .models import Category, ArtPrint


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ArtPrint)
class ArtPrintAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'limited_edition', 'created_at')
    list_filter = ('is_available', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'is_available')
