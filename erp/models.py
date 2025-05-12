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
        DELIVERED = 'delivered', _('Delivered (Signed)')
        
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
    receiver = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'department__name': 'Stores'},  
        related_name='estimates_received',
        verbose_name='Stores Department Receiver'
    )
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
    verified_by = models.ForeignKey(
        Employee,
        null=True,   
        blank=True,
        on_delete=models.PROTECT,
        limit_choices_to={'role__name': 'Credit Officer'},
        related_name='verifying_officer_estimates'
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
        return f"Estimate #{self.bk_estimate_id} - {self.customer_name} ({self.get_status_display()})"

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
            'draft': 'secondary',
            'submitted': 'info',
            'verified': 'primary',
            'dispatched': 'success',
            'delivered': 'success',
            'on-hold': 'warning',
            'rejected': 'danger',
            'cancelled': 'warning'
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


# ----------------------------
# 3. Verification & Stores
# ----------------------------
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
    billing_date = models.DateField(null=True, blank=True)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    invoice_no = models.CharField(max_length=100, null=True, blank=True)
    invoice_amount = models.CharField(max_length=100, null=True, blank=True)
    office_gate_pass = models.CharField(max_length=100, null=True, blank=True)
    store_gate_pass = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"Dispatch for {self.customer_name} - {self.invoice_no}"
        

class DeliveryNote(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('being_processed', 'Being Processed'),
        ('received', 'Received'),
        ('rejected', 'Rejected'),
    ]
    estimate_number = models.CharField(max_length=200, null=True, blank=True)
    delivery_note_number = models.CharField(max_length=100, null=True, blank=True)
    receiver_name = models.CharField(max_length=100, null=True, blank=True)
    receiver_contact = models.CharField(max_length=20, null=True, blank=True)
    date_goods_received = models.DateField(null=True, blank=True)

    
    customer_name = models.CharField(max_length=200, null=True, blank=True)  # typo fixed
    date_of_billing = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    invoice_no = models.CharField(max_length=100, null=True, blank=True)
    transaction_value = models.CharField(max_length=100, null=True, blank=True)

    
    customer_name_address = models.TextField(null=True, blank=True)
    sales_person = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_person = models.CharField(max_length=100, null=True, blank=True)
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
            return f">{(days // 15) * 15}"  # general case
 
class DeliveryNoteItem(models.Model):
    delivery_note = models.ForeignKey(DeliveryNote, related_name='items', on_delete=models.CASCADE)
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