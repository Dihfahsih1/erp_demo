from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from auditlog.models import AuditlogHistoryField
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from datetime import date
# ----------------------------
# 1. Core Entities
# ----------------------------

class SalesOfficerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role__name='Sales Officer')
    
class Department(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Department Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")

    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Role Name"))
    description = models.TextField(blank=True, verbose_name=_("Role Description"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    def __str__(self):
        return self.name

class RegionOfOperation(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Region Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name
class Employee(AbstractUser):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_("Department"),
        related_name='employees',
        blank=True, null=True
    )

    role = models.ForeignKey(
        UserRole,
        on_delete=models.PROTECT,
        verbose_name=_("Role"),
        related_name='employee_role', null=True
    )

    phone = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        blank=True
    )


    #is_verified = models.BooleanField(default=False, verbose_name='Verified by Admin'),

    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verified by Admin',
        blank=True, null=True
    )
    
    #is_accepted = models.BooleanField(default=False, verbose_name='Verified by Admin'),
    
    # Add these to resolve the clash
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='employee_set',  
        related_query_name='employee'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='employee_set',   
        related_query_name='employee'
    )
    region_of_operation = models.ForeignKey(
        RegionOfOperation,
        on_delete=models.PROTECT,
        verbose_name=_("Region of Operation"),
        related_name='employees',
        blank=True,
        null=True,
        default=None
    )


        
    class Meta:
        permissions = [
            ('can_delete_employee', 'Can delete employee records'),
        ]

    def delete(self, *args, **kwargs):
        if self.estimate_set.exists():  # Checks if employee has estimates
            raise models.ProtectedError(
                "Cannot delete employee with existing estimates",
                self
            )
        super().delete(*args, **kwargs)
        
        
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username  # fallback if names are not filled

class Customer(models.Model):
    name_of_business = models.CharField(max_length=200, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    road_location = models.CharField(max_length=150, blank=True, null=True)
    town_division = models.CharField(max_length=100, blank=True, null=True)
    nearest_landmark = models.CharField(max_length=150, blank=True, null=True)
    tel_1 = models.CharField(max_length=15, blank=True, null=True)
    tel_2 = models.CharField(max_length=15, blank=True, null=True)

    owner_name = models.CharField(max_length=100,blank=True, null=True)
    owner_tel = models.CharField(max_length=15, blank=True, null=True)

    next_of_kin = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_tel = models.CharField(max_length=15, blank=True, null=True)

    approved_by = models.CharField(max_length=100,blank=True, null=True)

    prepared_by = models.CharField(max_length=100, blank=True, null=True)
    prepared_date = models.DateField(blank=True,null=True)

    remarks = models.TextField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    # Uploads
    certificate_of_incorporation = models.FileField(upload_to='documents/certificates/', blank=True, null=True)
    passport_photo = models.ImageField(upload_to='photos/passports/', blank=True, null=True)
    trading_license = models.ImageField(upload_to='photos/license/', blank=True, null=True)
    national_id = models.ImageField(upload_to='photos/national_id/', blank=True, null=True)

    date_filled = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name_of_business

class SparePart(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Part Name"))
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("SKU"),
        help_text=_("Matching BK system SKU")
    )
    current_stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Current Stock"),
        validators=[MinValueValidator(0)]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Unit Price"),
        validators=[MinValueValidator(0)]
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Spare Part")
        verbose_name_plural = _("Spare Parts")

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_absolute_url(self):
        return reverse('sparepart-detail', kwargs={'pk': self.pk})

# ----------------------------
# 2. Estimate Lifecycle
# ----------------------------
class Estimate(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        SUBMITTED = 'submitted', _('Submitted')
        VERIFIED = 'verified', _('Verified')
        ON_HOLD = 'on-hold', _('On Hold') 
        REJECTED = 'rejected', _('Rejected')
        CANCELLED = 'cancelled', _('Cancelled')
        BILLED = 'billed', _('Billed')
        DISPATCHED = 'dispatched', _('Dispatched')
        DELIVERED = 'delivered', _('Delivered (Signed)'),
        DISPATCHREADY = 'dispatchready', _('ready for delivery')
    
    
    class StockStatus(models.TextChoices):
        PENDING = 'pending', _('Pending Check')
        IN_STOCK = 'in_stock', _('In Stock')
        OUT_OF_STOCK = 'out_of_stock', _('Out of Stock')
        PARTIAL = 'partial', _('Partial Stock')
         
    created_date = models.DateField(
        null=True,  
        blank=True,
        verbose_name='Date When Estimate was Created'
    )
    
    bk_estimate_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("BK Estimate ID"),
        help_text=_("Reference ID from Bookkeeping System")
    )
     
    customer_name = models.ForeignKey(
        Customer,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Customer"),
        related_name='estimates'
    )
    sales_person = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'role__name': 'Sales Officer'},
        related_name='estimates_as_sales_person'
    )
    verified_by= models.ForeignKey(
     Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'role__name': 'Credit Officer'},
        related_name='Verifying_Customer_Credit_Worthiness')
    # received_date = models.DateField(
    #     null=True,   
    #     blank=True,
    #     verbose_name='Date Received in Stores'
    # )
    
    amount = models.DecimalField(
        max_digits=10,  
        decimal_places=2,   
        default=0.00,  
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status")
    )
    
    stock_status = models.CharField(
        max_length=20,
        null=True,   
        blank=True,
        choices=StockStatus.choices,
        default=StockStatus.PENDING,
        verbose_name=_("Stock Status")
    )
    
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))
    history = AuditlogHistoryField()
    
    billing_officer = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'role__name': 'billing Officer'},
        related_name='billing_officer_estimates'
    )
    
    hold_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Hold Reason"),
        help_text=_("Explanation for why this estimate was put on hold")
    )

    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_verified = models.DateField(blank=True, null=True)
    date_billed = models.DateField(blank=True, null=True)
    

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Estimate")
        verbose_name_plural = _("Estimates")
        

    def __str__(self):
        return self.bk_estimate_id

    def get_absolute_url(self):
        return reverse('estimate-detail', kwargs={'pk': self.pk})

    def total_value(self):
        return sum(item.line_total() for item in self.items.all())

    def mark_as_verified(self, verified_by):
        self.status = self.Status.VERIFIED
        self.save()
        Verification.objects.create(
            estimate=self,
            verified_by=verified_by
        )
        return True

    def get_status_badge_color(self):
        colors = {
            'draft': 'secondary',      # Gray
            'submitted': 'info',       # Light blue
            'verified': 'primary',     # Blue
            'dispatched': 'success',   # Green
            'delivered': 'success',    # Green
            'on-hold': 'warning',      # Yellow
            'rejected': 'danger',      # Red
            'cancelled': 'warning',    # Yellow
            'packaged': 'secondary',   # Gray
            'billed': 'info',          # Dark gray
            'dispatchready': 'warning',# Yellow
            'in-transit': 'primary',   # Blue
        }
        return colors.get(self.status, 'light')   

class EstimateItem(models.Model):
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        verbose_name=_("Estimate"),
        related_name='items'
    )
    part = models.ForeignKey(
        SparePart,
        on_delete=models.PROTECT,
        verbose_name=_("Spare Part")
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_("Quantity"),
        validators=[MinValueValidator(1)]
    )
    negotiated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Negotiated Price"),
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = _("Estimate Item")
        verbose_name_plural = _("Estimate Items")
        unique_together = ['estimate', 'part']

    def __str__(self):
        return f"{self.part.name} x {self.quantity}"

    def line_total(self):
        return self.quantity * self.negotiated_price

 
class Verification(models.Model):
    estimate = models.OneToOneField(
        Estimate,
        on_delete=models.CASCADE,
        verbose_name=_("Estimate"),
        related_name='verification'
    )
    verified_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Verification'},
        verbose_name=_("Verified By")
    )
    notes = models.TextField(blank=True, verbose_name=_("Verification Notes"))
    verification_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Verification Date"))

    class Meta:
        verbose_name = _("Verification")
        verbose_name_plural = _("Verifications")
        ordering = ['-verification_date']

    def __str__(self):
        return f"Verification for Estimate #{self.estimate.bk_estimate_id}"

class Dispatch(models.Model):
    estimate_number = models.ForeignKey(
        Estimate,
        null=True, 
        blank=True, 
        on_delete=models.PROTECT,
        related_name='Dispatches')
    
    camera_number = models.CharField(max_length=100, null=True, blank=True)
    office_gate_pass = models.CharField(max_length=100, null=True, blank=True)
    store_gate_pass = models.CharField(max_length=100, null=True, blank=True)  
    dispatch_date = models.DateField(null=True, blank=True)
    picker = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        related_name='dispatch_picking'
    )
    packer = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        related_name='dispatch_packing'
    )
  
    def __str__(self):
        return f"Dispatch for {self.estimate_number.customer_name} - {self.estimate_number.invoice_number}"
class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        BEING_PROCESSED = 'being_processed', _('Being Processed')
        RECEIVED = 'received', _('Received')
        REJECTED = 'rejected', _('Rejected')
   
    estimate_number = models.ForeignKey(
        Estimate,
        null=True, 
        blank=True, 
        on_delete=models.PROTECT,
        related_name='Deliverys')
    
    dispatch_authorized_by = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        related_name='dispatch_authorizing_officer_estimates'
    )
    
    packaging_verified_by = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        related_name='package_verifying_officer_estimates'
    )
    
    delivery_note_number = models.CharField(max_length=100, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    
    receiver_name = models.CharField(max_length=100, null=True, blank=True)
    receiver_contact = models.CharField(max_length=20, null=True, blank=True)
    date_of_receipt = models.DateField(null=True, blank=True)
    date_goods_received = models.DateField(null=True, blank=True)
    dispatch_date = models.DateField(null=True, blank=True)
    delivery_status = models.CharField(max_length=20, null=True, blank=True, choices=Status.choices, default=Status.PENDING) 
 
    sales_person = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL, 
        null=True, blank=True)
    
    delivery_person = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        related_name='delivery_officer_estimates'
    )
    
    delivery_by_customer = models.CharField(max_length=100, null=True, blank=True)

    remarks = models.TextField(null=True, blank=True)
    

    image = models.ImageField(upload_to='delivery_notes/', null=True, blank=True)
    extracted_text = models.TextField(null=True, blank=True)
    created_at = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Delivery {self.delivery_note_number} - {self.receiver_name}"

    def days_outstanding(self):
        """Returns the number of days outstanding only if status is pending."""
        if self.status == 'pending' and self.date_of_billing:
            return (date.today() - self.date_of_billing).days
        return 0

    def aging_category(self):
        """Returns aging range like 0<15, >15, >30, etc."""
        days = self.days_outstanding()
        if self.status != 'pending' or not self.date_of_billing:
            return "N/A"
        if days < 15:
            return "0<15"
        elif 15 <= days < 30:
            return ">15"
        elif 30 <= days < 45:
            return ">30"
        elif 45 <= days < 60:
            return ">45"
        else:
            return f">{(days // 15) * 15}"   
        
    def get_status_badge_color(self):
        colors = {
            'pending': 'info',
            'being_processed': 'warning',
            'received': 'success',
            'rejected': 'danger',
        } 
        
        return colors.get(self.delivery_status, 'light')
    


class DeliveryImage(models.Model):
    delivery = models.ForeignKey(
        Delivery, 
        on_delete=models.CASCADE,
        related_name='images'
    )
    delivery_image = models.ImageField(
        upload_to='delivery_notes/%Y/%m/%d/',
        verbose_name='Delivery Note Image'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        'Employee',  # Assuming you have an Employee model
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Mark as primary image"
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Delivery Image'
        verbose_name_plural = 'Delivery Images'

    def __str__(self):
        return f"Image for {self.delivery.delivery_note_number}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image exists
        if self.is_primary:
            DeliveryImage.objects.filter(
                delivery=self.delivery
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
 
class DeliveryItem(models.Model):
    delivery_note = models.ForeignKey(Delivery, related_name='items', on_delete=models.CASCADE)
    item_code = models.CharField(max_length=100, null=True, blank=True)  # Added for codes like "REV-OF-TR-BK"
    item_description = models.CharField(max_length=255)
    quantity = models.FloatField(default=1)  # Default quantity is 1

    def __str__(self):
        return f"{self.item_code} - {self.item_description}"
# ----------------------------
# 5. Reconciliation          #
# ----------------------------
class StoresReconciliation(models.Model):
    estimate = models.OneToOneField(
        Estimate,
        on_delete=models.CASCADE,
        verbose_name=_("Estimate"),
        related_name='reconciliation'
    )
    reconciled_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},
        verbose_name=_("Reconciled By")
    )
    discrepancies = models.TextField(blank=True, verbose_name=_("Discrepancy Notes"))
    reconciliation_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Reconciliation Date"))

    class Meta:
        verbose_name = _("Stores Reconciliation")
        verbose_name_plural = _("Stores Reconciliations")
        ordering = ['-reconciliation_date']

    def __str__(self):
        return f"Reconciliation for Estimate #{self.estimate.bk_estimate_id}"

# ----------------------------
# 6. Notifications     
# ----------------------------
class Notification(models.Model):
    estimate = models.ForeignKey(
        Estimate,
        on_delete=models.CASCADE,
        verbose_name=_("Estimate"),
        related_name='notifications'
    )
    message = models.CharField(max_length=200, verbose_name=_("Notification Message"))
    recipient = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
        related_name='notifications'
    )
    is_read = models.BooleanField(default=False, verbose_name=_("Read Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"Notification for {self.recipient}: {self.message[:50]}"

    def mark_as_read(self):
        self.is_read = True
        self.save()
        return True