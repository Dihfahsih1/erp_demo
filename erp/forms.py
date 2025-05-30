# dispatch/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Dispatch,Delivery, Estimate, UserRole

from .models import Customer,Employee,Department,UserRole
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from dal import autocomplete

class CustomerAuto(forms.ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=autocomplete.ModelSelect2(url='customer-autocomplete')
    )

class EmployeeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.ModelChoiceField(queryset=UserRole.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = ('username', 'email', 'password1', 'password2', 
                 'first_name', 'last_name', 'phone', 'department', 'role')

class EmployeeLoginForm(AuthenticationForm):
    class Meta:
        model = Employee
        fields = ('username', 'password')

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        widgets = {
            'location': forms.TextInput(attrs={'id': 'location-input', 'placeholder': 'Auto-detect or type location'}),
            'prepared_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = "__all__"
        
class DeliveryUploadForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date_goods_received:
            self.initial['date_of_delivery'] = self.instance.date_goods_received

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'date_of_delivery' in self.cleaned_data:
            instance.date_goods_received = self.cleaned_data['date_of_delivery']
        if commit:
            instance.save()
        return instance
    
    exclude = ['created_at', 'updated_at']
class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = "__all__"
        exclude = ['created_at', 'updated_at']
        
        
class EstimateForm(forms.ModelForm):
    # customer_name = forms.ModelChoiceField(
    #     queryset=Customer.objects.all(),
    #     required=True,
    #     label="Customer",
    #     widget=forms.Select(attrs={'class': 'form-control'})
    # )
    class Meta:
        model = Estimate
        fields = '__all__'
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sales_person'].queryset = Employee.objects.filter(
            role__name='Sales Officer' 
        )
        
class BillingForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['invoice_number', 'invoice_amount']
class EstimateUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File',
        help_text='Upload an Excel file with estimates. Required columns: bk_estimate_id, customer',
        widget=forms.FileInput(attrs={
            'accept': '.xlsx, .xls',
            'class': 'form-control'
        })
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data['excel_file']
        if not file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError("Only Excel files are allowed")
        return file
    
class DispatchVerificationForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = "__all__"
     
        
class SalesAgentNoteForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['image', 'extracted_text', 'receiver_name', 'receiver_contact', 'date_goods_received']

class OfficerReviewForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_status', 'remarks']