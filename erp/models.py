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

# ----------------------------
# 1. Core Entities
# ----------------------------
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

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

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
        DRAFT = 'draft', _('Draft (Sales)')
        SUBMITTED = 'submitted', _('Submitted to CRM')
        VERIFIED = 'verified', _('Verified')
        DISPATCHED = 'dispatched', _('Dispatched')
        DELIVERED = 'delivered', _('Delivered (Signed)')
    
    bk_estimate_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("BK Estimate ID"),
        help_text=_("Reference ID from Bookkeeping System")
    )
    customer = models.CharField(
        max_length=20, null=True
    )
    sales_agent = models.CharField(
        max_length=20, null=True
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Estimate")
        verbose_name_plural = _("Estimates")
        permissions = [
            ("change_estimate_status", "Can modify estimate status"),
            ("view_all_estimates", "Can view all estimates"),
        ]

    def __str__(self):
        return f"Estimate #{self.bk_estimate_id} - {self.customer} ({self.get_status_display()})"

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
            'dispatched': 'warning',
            'delivered': 'success',
            'rejected': 'danger',
            'cancelled': 'dark'
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
    # Status choices
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_TRANSIT = 'in_transit', _('In Transit')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    estimate = models.CharField(
        max_length=20,
        verbose_name=_("Estimate"),
        null=True,
        blank=True
    )
    bk_proforma_id = models.CharField(
        max_length=20,
        verbose_name=_("BK Proforma ID"),
        help_text=_("Reference ID from Bookkeeping System")
    )
    transport_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Transport Cost"),
        validators=[MinValueValidator(0)]
    )
    vehicle_number = models.CharField(
        max_length=20, 
        verbose_name=_("Vehicle Number")
    )
    driver_name = models.CharField(
        max_length=100, 
        verbose_name=_("Driver Name")
    )
    driver_contact = models.CharField(
        max_length=20, 
        verbose_name=_("Driver Contact")
    )
    dispatch_time = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Dispatch Time")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Dispatch Status")
    )
    delivery_confirmation_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Delivery Confirmation Time")
    )
    cancellation_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Cancellation Reason")
    )

    class Meta:
        verbose_name = _("Dispatch")
        verbose_name_plural = _("Dispatches")
        ordering = ['-dispatch_time']

    def __str__(self):
        return f"Dispatch #{self.id} for Estimate {self.estimate}"

    def mark_as_delivered(self):
        """Mark dispatch as delivered and set timestamp"""
        self.status = self.Status.DELIVERED
        self.delivery_confirmation_time = timezone.now()
        self.save()
        return True

    def mark_as_in_transit(self):
        """Mark dispatch as in transit"""
        self.status = self.Status.IN_TRANSIT
        self.save()
        return True

    def cancel_dispatch(self, reason=None):
        """Cancel dispatch with optional reason"""
        self.status = self.Status.CANCELLED
        self.cancellation_reason = reason
        self.save()
        return True

    @property
    def is_delivered(self):
        """Backward-compatible property for boolean delivery status"""
        return self.status == self.Status.DELIVERED

    @property
    def status_badge_class(self):
        """Get appropriate CSS class for status badge"""
        classes = {
            self.Status.PENDING: 'bg-secondary',
            self.Status.IN_TRANSIT: 'bg-info',
            self.Status.DELIVERED: 'bg-success',
            self.Status.CANCELLED: 'bg-danger',
        }
        return classes.get(self.status, 'bg-secondary')

class DeliveryNote(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    delivery_no = models.CharField(max_length=100, null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)  # Changed to DateField
    receiver_name = models.CharField(max_length=100, null=True, blank=True)
    receiver_contact = models.CharField(max_length=20, null=True, blank=True)
    warehouse = models.CharField(max_length=100, null=True, blank=True, default="Main Location")

    estimate_number = models.CharField(max_length=100, null=True, blank=True)
    delivery_note_number = models.CharField(max_length=100, null=True, blank=True)
    customer_name_address = models.TextField(null=True, blank=True)
    sales_person = models.CharField(max_length=100, null=True, blank=True)  # Should be required
    date_of_delivery = models.DateField(null=True, blank=True)  # Changed to DateField

    remarks = models.TextField(null=True, blank=True)
    date_goods_received = models.DateField(null=True, blank=True)  # Changed to DateField

    image = models.ImageField(upload_to='delivery_notes/', null=True, blank=True)
    extracted_text = models.TextField(null=True, blank=True)

    created_at = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Delivery {self.delivery_no} - {self.receiver_name}"

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