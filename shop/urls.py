from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:pk>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove/<int:pk>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('update/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/create-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('download/<int:art_id>/', views.download_print, name='download_print'),
]
