from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_list, name='gallery'),
    path('wishlist/add/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<slug:slug>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('<slug:slug>/', views.art_detail, name='art_detail'),
]
