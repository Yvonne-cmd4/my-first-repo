from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'), 
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('technician_dashboard/', views.technician_dashboard, name='technician_dashboard'),
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),  # ✅ must exist
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    
    path('technician/ticket/<int:ticket_id>/', views.technician_ticket_edit, name='technician_ticket_edit'),
    path('admin/ticket/<int:ticket_id>/edit/', views.technician_ticket_edit, name='edit_ticket'),
    
    path('assign_ticket/<int:ticket_id>/', views.assign_ticket, name='assign_ticket'),
    path('reassign_ticket/<int:ticket_id>/', views.reassign_ticket, name='reassign_ticket'),
]