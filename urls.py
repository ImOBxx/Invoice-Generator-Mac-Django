from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('invoicing/', views.invoicing_overview, name='invoicing_overview'),
    path('invoicing/create/', views.create_invoice, name='create_invoice'),
    path('list/', views.invoice_list, name='invoice_list'),
    path('invoicing/details/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoicing/list/', views.invoices_list, name='invoices_list'),  # Ensure this line exists
    path('invoicing/save/<int:invoice_id>/', views.save_invoice, name='save_invoice'),  # Only if needed
    path('invoicing/discard/<int:invoice_id>/', views.discard_invoice, name='discard_invoice'),  # Only if needed
    path('invoicing/print/<int:invoice_id>/', views.print_invoice, name='print_invoice'),
    path('invoicing/delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('logout/', views.custom_logout, name='logout'),
]
