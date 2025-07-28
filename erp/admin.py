import json
from django import forms
from django.contrib import admin
from .models import Department, Employee, Customer, RegionOfOperation, SparePart, Estimate, EstimateItem, Verification, Dispatch, Delivery, StoresReconciliation, UserRole

from django.utils.html import format_html
from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.templatetags.static import static
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Model Admin Classes
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = Employee

    list_display = ('username', 'email', 'department','region_of_operation')
    list_filter = ('department', 'is_staff')
    search_fields = ('username', 'email', 'phone')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Department', {'fields': ('department',)}),
        ('Region', {'fields': ('region_of_operation',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'department'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)  # Hash the password
        super().save_model(request, obj, form, change)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('owner_name','district')
    search_fields = ('owner_name','district')
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
    list_display = ('bk_estimate_id', 'status',  'amount')
    list_filter = ('status', 'created_at') 
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

@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ('estimate_number', 'store_gate_pass') 
    
    
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_note_number', 'delivery_date')  

@admin.register(StoresReconciliation)
class StoresReconciliationAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'reconciled_by', 'reconciliation_date')
    readonly_fields = ('reconciliation_date',)

@admin.register(RegionOfOperation)
class RegionOfOperationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

