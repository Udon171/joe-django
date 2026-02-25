from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.commission_create, name='commission_create'),
    path('<int:pk>/edit/', views.commission_edit, name='commission_edit'),
    path('<int:pk>/delete/', views.commission_delete, name='commission_delete'),
]
