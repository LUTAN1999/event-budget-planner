from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='home'),

    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Categories
    path('events/<int:event_pk>/category/add/', views.category_add, name='category_add'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Expenses
    path('category/<int:cat_pk>/expense/add/', views.expense_add, name='expense_add'),
    path('expense/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # Vendors
    path('events/<int:event_pk>/vendor/add/', views.vendor_add, name='vendor_add'),
    path('vendor/<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),

    # Export
    path('events/<int:pk>/export/csv/', views.export_csv, name='export_csv'),
    path('events/<int:pk>/export/pdf/', views.export_pdf, name='export_pdf'),
]