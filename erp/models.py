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

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
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
    RECEIVER_CHOICES = [
        ('customer', 'Customer'),
        ('other', 'Other'),
    ]
    
    received_by = models.CharField(max_length=10, choices=RECEIVER_CHOICES, null=True, blank=True) 
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
    received_by_customer = models.CharField(max_length=100, null=True, blank=True)
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
    
    
    
    
#ERPNEXT  tables 
class CustomerDetails(models.Model):
    # Basic Info
    naming_series = models.CharField(max_length=100, blank=True, null=True)
    salutation = models.CharField(max_length=50, blank=True, null=True)
    customer_id = models.CharField(max_length=10000, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=50)
    customer_group = models.CharField(max_length=100, blank=True, null=True)
    territory = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    lead_name = models.CharField(max_length=100, blank=True, null=True)
    opportunity_name = models.CharField(max_length=100, blank=True, null=True)
    prospect_name = models.CharField(max_length=100, blank=True, null=True)
    account_manager = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='customer_images/', blank=True, null=True)

    # Defaults
    default_currency = models.CharField(max_length=50, blank=True, null=True)
    default_bank_account = models.CharField(max_length=100, blank=True, null=True)
    default_price_list = models.CharField(max_length=100, blank=True, null=True)

    # Internal Customer
    is_internal_customer = models.BooleanField(default=False)
    represents_company = models.CharField(max_length=100, blank=True, null=True)

    # More Info
    market_segment = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    customer_pos_id = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    customer_details = models.TextField(blank=True, null=True)

    # Primary Address & Contact Info
    customer_primary_address = models.CharField(max_length=100, blank=True, null=True)
    primary_address = models.TextField(blank=True, null=True)
    customer_primary_contact = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    route = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)

    # Taxation
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    tax_category = models.CharField(max_length=100, blank=True, null=True)
    tax_withholding_category = models.CharField(max_length=100, blank=True, null=True)

    # Accounting
    payment_terms = models.CharField(max_length=100, blank=True, null=True)

    # Loyalty
    loyalty_program = models.CharField(max_length=100, blank=True, null=True)
    loyalty_program_tier = models.CharField(max_length=100, blank=True, null=True)

    # Sales Team
    default_sales_partner = models.CharField(max_length=100, blank=True, null=True)
    default_commission_rate = models.FloatField(blank=True, null=True)

    # Settings
    so_required = models.BooleanField(default=False)
    dn_required = models.BooleanField(default=False)
    is_frozen = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)

    # Custom Attachments
    custom_national_id = models.FileField(upload_to='customer_docs/', blank=True, null=True)
    custom_trading_license = models.FileField(upload_to='customer_docs/', blank=True, null=True)
    custom_passport_photo = models.ImageField(upload_to='customer_docs/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name
    
    
class SalesPerson(models.Model):
    sales_person_name = models.CharField(max_length=255)
    parent_sales_person = models.CharField(max_length=255, blank=True, null=True)  # Link to another SalesPerson
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_group = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    employee = models.CharField(max_length=100, blank=True, null=True)  # Link to Employee
    department = models.CharField(max_length=100, blank=True, null=True)  # Link to Department

    lft = models.IntegerField(blank=True, null=True)  # Nested Set model fields
    rgt = models.IntegerField(blank=True, null=True)
    old_parent = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sales_person_name

class CustomerAddress(models.Model):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    
class CustomerSalesTeam(models.Model):
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    sales_person = models.CharField(max_length=255, blank=True, null=True)
    allocated_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    
class SalesOrder(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    naming_series = models.CharField(max_length=140)
    customer = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    tax_id = models.CharField(max_length=140, blank=True, null=True)
    order_type = models.CharField(max_length=140, blank=True, null=True)
    transaction_date = models.DateField()
    delivery_date = models.DateField(blank=True, null=True)
    po_no = models.CharField(max_length=140, blank=True, null=True)
    po_date = models.DateField(blank=True, null=True)
    company = models.CharField(max_length=255)
    
    skip_delivery_note = models.BooleanField(default=False)
    has_unit_price_items = models.BooleanField(default=False)
    amended_from = models.CharField(max_length=140, blank=True, null=True)
    cost_center = models.CharField(max_length=140, blank=True, null=True)
    project = models.CharField(max_length=140, blank=True, null=True)
    currency = models.CharField(max_length=20)
    conversion_rate = models.FloatField(default=1.0)
    selling_price_list = models.CharField(max_length=140, blank=True, null=True)
    price_list_currency = models.CharField(max_length=20, blank=True, null=True)
    plc_conversion_rate = models.FloatField(default=1.0)
    ignore_pricing_rule = models.BooleanField(default=False)
    set_warehouse = models.CharField(max_length=140, blank=True, null=True)
    reserve_stock = models.BooleanField(default=False)

    total_qty = models.FloatField(default=0.0)
    total_net_weight = models.FloatField(default=0.0)
    base_total = models.DecimalField(max_digits=12, decimal_places=2)
    base_net_total = models.DecimalField(max_digits=12, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    net_total = models.DecimalField(max_digits=12, decimal_places=2)

    tax_category = models.CharField(max_length=140, blank=True, null=True)
    taxes_and_charges = models.CharField(max_length=255, blank=True, null=True)
    shipping_rule = models.CharField(max_length=140, blank=True, null=True)
    incoterm = models.CharField(max_length=140, blank=True, null=True)
    named_place = models.CharField(max_length=140, blank=True, null=True)

    base_grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    base_rounding_adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    base_rounded_total = models.DecimalField(max_digits=12, decimal_places=2)
    base_in_words = models.TextField(blank=True, null=True)

    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    rounding_adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    rounded_total = models.DecimalField(max_digits=12, decimal_places=2)
    in_words = models.TextField(blank=True, null=True)

    advance_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    disable_rounded_total = models.BooleanField(default=False)

    status = models.CharField(max_length=140, blank=True, null=True)
    delivery_status = models.CharField(max_length=140, blank=True, null=True)
    per_delivered = models.FloatField(default=0.0)
    per_billed = models.FloatField(default=0.0)
    per_picked = models.FloatField(default=0.0)
    billing_status = models.CharField(max_length=140, blank=True, null=True)

    sales_partner = models.CharField(max_length=140, blank=True, null=True)
    amount_eligible_for_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    commission_rate = models.FloatField(default=0.0)
    total_commission = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    loyalty_points = models.IntegerField(default=0)
    loyalty_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    is_internal_customer = models.BooleanField(default=False, null=True, blank=True)
    source = models.CharField(max_length=140, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} - {self.transaction_date}"


class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    item_code = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    qty = models.FloatField()
    rate = models.DecimalField(max_digits=18, decimal_places=2)
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return f"{self.item_code} - {self.qty}"



from django.db import models

class Item(models.Model):
    # Basic Information
    naming_series = models.CharField(max_length=255, blank=True, null=True)
    item_code = models.CharField(max_length=255, unique=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    item_group = models.CharField(max_length=255, blank=True, null=True)
    stock_uom = models.CharField(max_length=255, blank=True, null=True)

    # Status
    disabled = models.BooleanField(default=False)
    allow_alternative_item = models.BooleanField(default=False)
    is_stock_item = models.BooleanField(default=False)
    has_variants = models.BooleanField(default=False)
    is_fixed_asset = models.BooleanField(default=False)
    auto_create_assets = models.BooleanField(default=False)
    is_grouped_asset = models.BooleanField(default=False)

    # Asset
    asset_category = models.CharField(max_length=255, blank=True, null=True)
    asset_naming_series = models.CharField(max_length=255, blank=True, null=True)

    # Stock
    opening_stock = models.FloatField(blank=True, null=True)
    valuation_rate = models.FloatField(blank=True, null=True)
    standard_rate = models.FloatField(blank=True, null=True)
    over_delivery_receipt_allowance = models.FloatField(blank=True, null=True)
    over_billing_allowance = models.FloatField(blank=True, null=True)

    # Image and Description
    image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Brand
    brand = models.CharField(max_length=255, blank=True, null=True)
    custom_model = models.CharField(max_length=255, blank=True, null=True)

    # Inventory Settings
    shelf_life_in_days = models.IntegerField(blank=True, null=True)
    end_of_life = models.DateField(blank=True, null=True)
    default_material_request_type = models.CharField(max_length=255, blank=True, null=True)
    valuation_method = models.CharField(max_length=255, blank=True, null=True)
    warranty_period = models.CharField(max_length=255, blank=True, null=True)
    weight_per_unit = models.FloatField(blank=True, null=True)
    weight_uom = models.CharField(max_length=255, blank=True, null=True)
    allow_negative_stock = models.BooleanField(default=False)

    # Serial and Batch
    has_batch_no = models.BooleanField(default=False)
    create_new_batch = models.BooleanField(default=False)
    batch_number_series = models.CharField(max_length=255, blank=True, null=True)
    has_expiry_date = models.BooleanField(default=False)
    retain_sample = models.BooleanField(default=False)
    sample_quantity = models.IntegerField(blank=True, null=True)
    has_serial_no = models.BooleanField(default=False)
    serial_no_series = models.CharField(max_length=255, blank=True, null=True)

    # Variants
    variant_of = models.CharField(max_length=255, blank=True, null=True)
    variant_based_on = models.CharField(max_length=255, blank=True, null=True)

    # Deferred Accounting
    enable_deferred_expense = models.BooleanField(default=False)
    no_of_months_exp = models.IntegerField(blank=True, null=True)
    enable_deferred_revenue = models.BooleanField(default=False)
    no_of_months = models.IntegerField(blank=True, null=True)

    # Purchasing
    purchase_uom = models.CharField(max_length=255, blank=True, null=True)
    min_order_qty = models.FloatField(blank=True, null=True)
    safety_stock = models.FloatField(blank=True, null=True)
    is_purchase_item = models.BooleanField(default=False)
    lead_time_days = models.IntegerField(blank=True, null=True)
    last_purchase_rate = models.FloatField(blank=True, null=True)
    is_customer_provided_item = models.BooleanField(default=False)
    customer = models.CharField(max_length=255, blank=True, null=True)
    delivered_by_supplier = models.BooleanField(default=False)

    # Foreign Trade
    country_of_origin = models.CharField(max_length=255, blank=True, null=True)
    customs_tariff_number = models.CharField(max_length=255, blank=True, null=True)

    # Sales
    sales_uom = models.CharField(max_length=255, blank=True, null=True)
    grant_commission = models.BooleanField(default=False)
    is_sales_item = models.BooleanField(default=False)
    max_discount = models.FloatField(blank=True, null=True)

    # Taxes and Quality
    inspection_required_before_purchase = models.BooleanField(default=False)
    quality_inspection_template = models.CharField(max_length=255, blank=True, null=True)
    inspection_required_before_delivery = models.BooleanField(default=False)

    # Manufacturing
    include_item_in_manufacturing = models.BooleanField(default=False)
    is_sub_contracted_item = models.BooleanField(default=False)
    default_bom = models.CharField(max_length=255, blank=True, null=True)
    customer_code = models.TextField(blank=True, null=True)
    default_item_manufacturer = models.CharField(max_length=255, blank=True, null=True)
    default_manufacturer_part_no = models.CharField(max_length=255, blank=True, null=True)
    total_projected_qty = models.FloatField(blank=True, null=True)
    
    
        # 🔧 Add these missing fields below
    default_supplier = models.CharField(max_length=255, null=True, blank=True)
    default_warehouse = models.CharField(max_length=255, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    reorder_level = models.FloatField(null=True, blank=True)
    reorder_qty = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_code




class ERPUser(models.Model):
    # Basic Identity
    enabled = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=100, unique=True)
    
    # Password for login (Django-compatible)
    password = models.CharField(max_length=128, blank=True)

    # Profile Image
    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    
    # Locale
    language = models.CharField(max_length=50, blank=True)
    time_zone = models.CharField(max_length=100, blank=True)
    
    # Account Settings
    send_welcome_email = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
    mute_sounds = models.BooleanField(default=False)
    desk_theme = models.CharField(max_length=50, blank=True)
    banner_image = models.ImageField(upload_to='banner_images/', blank=True, null=True)

    # Password Reset & Security
    new_password = models.CharField(max_length=128, blank=True)
    logout_all_sessions = models.BooleanField(default=False)
    reset_password_key = models.CharField(max_length=128, blank=True)
    last_reset_password_key_generated_on = models.DateTimeField(null=True, blank=True)
    last_password_reset_date = models.DateField(null=True, blank=True)

    # Bio
    gender = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    interest = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    mobile_no = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    # Notifications & Follow Settings
    document_follow_notify = models.BooleanField(default=True)
    document_follow_frequency = models.CharField(max_length=50, blank=True)
    follow_created_documents = models.BooleanField(default=True)
    follow_commented_documents = models.BooleanField(default=True)
    follow_liked_documents = models.BooleanField(default=True)
    follow_assigned_documents = models.BooleanField(default=True)
    follow_shared_documents = models.BooleanField(default=True)

    # Email Preferences
    email_signature = models.TextField(blank=True)
    thread_notify = models.BooleanField(default=True)
    send_me_a_copy = models.BooleanField(default=True)
    allowed_in_mentions = models.BooleanField(default=True)

    # Workspace
    default_workspace = models.CharField(max_length=100, blank=True)
    default_app = models.CharField(max_length=100, blank=True)

    # Security / Access Control
    simultaneous_sessions = models.PositiveIntegerField(default=1)
    restrict_ip = models.TextField(blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    login_after = models.PositiveIntegerField(null=True, blank=True)
    login_before = models.PositiveIntegerField(null=True, blank=True)
    user_type = models.CharField(max_length=50, blank=True)
    last_active = models.DateTimeField(null=True, blank=True)
    bypass_restrict_ip_check_if_2fa_enabled = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    # API Access
    api_key = models.CharField(max_length=128, blank=True)
    api_secret = models.CharField(max_length=128, blank=True)
    
    # System fields
    onboarding_status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.full_name or f"{self.first_name} {self.last_name}".strip() or self.username or self.email

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        ordering = ['username']

class SalesPerson(models.Model):
    sales_person_name = models.CharField(max_length=255)
    parent_sales_person = models.CharField(max_length=255, null=True, blank=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    employee = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    lft = models.IntegerField(null=True, blank=True)
    rgt = models.IntegerField(null=True, blank=True)
    old_parent = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.sales_person_name
    
class SalesPersonTarget(models.Model):
    sales_person = models.CharField(max_length=255, null=True, blank=True)
    target_period = models.CharField(max_length=100)  # e.g. "Monthly", "Quarterly", etc.
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    distribution_id = models.CharField(max_length=100, null=True, blank=True)  # Optional custom field

    def __str__(self):
        return f"{self.sales_person} - {self.target_period}: {self.target_amount}"

