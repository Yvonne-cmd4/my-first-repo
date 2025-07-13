from django.contrib import admin
from .models import User, Ticket
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportMixin

# Custom admin for User
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

# Custom admin for Ticket
class TicketAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'title', 'created_by', 'assigned_to', 'status',
        'priority', 'category', 'solved_by', 'created_at'
    )
    list_filter = ('status', 'priority', 'category', 'assigned_to')
    search_fields = ('title', 'created_by__username', 'assigned_to__username')
    readonly_fields = ('created_by', 'created_at', 'solved_by')

    def save_model(self, request, obj, form, change):
        # Automatically set solved_by when ticket is closed
        if obj.status == 'Closed' and obj.assigned_to:
            obj.solved_by = obj.assigned_to.get_full_name() or obj.assigned_to.username
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Only allow technicians to be assigned in the dropdown
        if db_field.name == "assigned_to":
            kwargs["queryset"] = User.objects.filter(role='Technician')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Register models with correct admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Ticket, TicketAdmin)
