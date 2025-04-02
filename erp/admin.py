import json
from django import forms
from django.contrib import admin
from .models import Department, Employee, Customer, SparePart, Estimate, EstimateItem, Verification, Dispatch, DeliveryConfirmation, StoresReconciliation

from django.utils.html import format_html
from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.templatetags.static import static
from .utils.delivery_ocr import extract_delivery_data

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

# @admin.register(DeliveryConfirmation)
# class DeliveryConfirmationAdmin(admin.ModelAdmin):
#     list_display = ('estimate', 'uploaded_by', 'upload_time')
#     readonly_fields = ('upload_time','document_preview')

#     def document_preview(self, obj):
#         return format_html(
#             '<a href="{}" target="_blank"><img src="{}" height="150"></a>',
#             obj.signed_document.url,
#             obj.signed_document.url
#         )

@admin.register(StoresReconciliation)
class StoresReconciliationAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'reconciled_by', 'reconciliation_date')
    readonly_fields = ('reconciliation_date',)



##################LOGIC#########################
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = DeliveryConfirmation
        fields = '__all__'
        widgets = {
            'uploaded_by': forms.HiddenInput(),
        }

@admin.register(DeliveryConfirmation)
class DeliveryAdmin(admin.ModelAdmin):
    form = DeliveryForm
    list_display = ('customer_name', 'estimate_number', 'delivery_date', 'image_preview')
    readonly_fields = ('extracted_data', 'created_at', 'data_preview')
    
    # Jazzmin-specific configuration
    jazzmin_form_template = 'admin/delivery_confirmation_change_form.html'
    
    def save_model(self, request, obj, form, change):
        if not change and obj.signed_image:
            # First save to get file path
            super().save_model(request, obj, form, change)
            
            # Extract data from image
            ocr_results = extract_delivery_data(obj.signed_image.path)
            obj.extracted_data = ocr_results
            
            # Auto-populate fields if found
            if 'customer_name' in ocr_results:
                obj.customer_name = ocr_results['customer_name']
            if 'estimate_number' in ocr_results:
                obj.estimate_number = ocr_results['estimate_number']
            if 'date' in ocr_results:
                obj.delivery_date = ocr_results['date']
        
        super().save_model(request, obj, form, change)
    
    def image_preview(self, obj):
        if obj.signed_image:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>',
                obj.signed_image.url
            )
        return "-"
    image_preview.short_description = "Preview"
    
    def data_preview(self, obj):
        if obj.extracted_data:
            return format_html(
                '<pre>{}</pre>',
                json.dumps(obj.extracted_data, indent=2)
            )
        return "-"
    data_preview.short_description = "Extracted Data"

