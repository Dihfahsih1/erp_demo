from django.contrib import admin
from .models import Department, Employee, Customer, SparePart, Estimate, EstimateItem, Verification, Dispatch, DeliveryConfirmation, StoresReconciliation

from .resources import EstimateResource
from django.utils.html import format_html


# Customize the admin interface
class CustomAdminSite(admin.AdminSite):
    site_header = 'AutoZone ERP Admin'
    site_title = 'AutoZone Administration'
    index_title = 'Welcome to AutoZone ERP'

admin_site = CustomAdminSite(name='autozone_admin')

# Model Admin Classes
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'department', 'phone')
    list_filter = ('department', 'is_staff')
    search_fields = ('username', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Department', {'fields': ('department',)}),
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'email', 'address')
    search_fields = ('name', 'contact', 'email')
    list_per_page = 20


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'current_stock', 'unit_price')
    list_filter = ('current_stock',)
    search_fields = ('name', 'sku')
    ordering = ('name',)

class EstimateItemInline(admin.TabularInline):
    model = EstimateItem
    extra = 1
    fields = ('part', 'quantity', 'negotiated_price', 'line_total')
    readonly_fields = ('line_total',)
    
    def line_total(self, instance):
        return instance.line_total()
    line_total.short_description = 'Total'

@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    resource_class = EstimateResource
    list_display = ('bk_estimate_id', 'customer', 'sales_agent', 'status', 'created_at', 'total_value')
    list_filter = ('status', 'created_at')
    search_fields = ('bk_estimate_id', 'customer__name')
    inlines = [EstimateItemInline]
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        queryset.update(status='verified')
    mark_as_verified.short_description = "Mark selected as verified"
    
    def total_value(self, obj):
        return sum(item.line_total() for item in obj.items.all())
    total_value.short_description = 'Total Value'

# @admin.register(Verification)
# class VerificationAdmin(admin.ModelAdmin):
#     list_display = ('estimate', 'verified_by', 'verification_date', 'is_approved')
#     list_filter = ('verification_date', 'is_approved')
#     raw_id_fields = ('estimate',)

@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'vehicle_number', 'driver_name', 'dispatch_time', 'is_delivered')
    list_filter = ('dispatch_time', 'is_delivered')
    search_fields = ('vehicle_number', 'driver_name')

@admin.register(DeliveryConfirmation)
class DeliveryConfirmationAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'uploaded_by', 'upload_time')
    readonly_fields = ('upload_time','document_preview')

    def document_preview(self, obj):
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" height="150"></a>',
            obj.signed_document.url,
            obj.signed_document.url
        )

@admin.register(StoresReconciliation)
class StoresReconciliationAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'reconciled_by', 'reconciliation_date')
    readonly_fields = ('reconciliation_date',)

