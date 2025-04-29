from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from erp.forms import DispatchForm,DeliveryNoteForm, EstimateForm
from .models import Customer, DeliveryNote, Dispatch, Estimate
import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import pandas as pd
from io import BytesIO
from datetime import datetime
from .models import Estimate
from .forms import DispatchVerificationForm, EstimateForm, EstimateUploadForm
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CustomerForm, EmployeeLoginForm,EmployeeRegistrationForm
from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')  # Replace with your desired redirect
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_employee(request):
    if request.method == 'POST':
        form = EmployeeLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  # Replace with your desired redirect
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = EmployeeLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-date_filled')
    paginator = Paginator(customers, 10)  # Show 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customer_list.html', {'page_obj': page_obj})

@login_required
def register_customer(request):
    submitted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CustomerForm()
            submitted = True
    else:
        form = CustomerForm()

    return render(request, 'register_customer.html', {'form': form, 'submitted': submitted})

@login_required
def customer_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_view.html', {'customer': customer})

@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_edit.html', {'form': form, 'edit_mode': True})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')

@login_required
@require_http_methods(["PATCH"])
def mark_delivered(request, dispatch_id):
    try:
        dispatch = Dispatch.objects.get(pk=dispatch_id)
        dispatch.mark_as_delivered()
        return JsonResponse({
            'status': 'success',
            'message': 'Dispatch marked as delivered'
        })
    except Dispatch.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Dispatch not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    
@login_required
def dashboard(request):
    context = {
        'page_title': 'Dashboard',
        'active_page': 'dashboard',
    }
    return render(request, 'index.html', context)

@login_required
def dispatch_view(request):
    """
    Simplified dispatch view that handles:
    - GET: Show empty form
    - POST: Save form data to database
    - PATCH (AJAX): Mark dispatch as delivered
    """
    
    if request.method == 'GET':
        # Show empty form
        form = DispatchForm()
        return render(request, 'dispatch_form.html', {'form': form})
        
    elif request.method == 'POST':
        # Save form data
        form = DispatchForm(request.POST)
        if form.is_valid():
            dispatch = form.save()
            messages.success(request, _("Dispatch saved successfully!"))
            return redirect('mark_dispatch_delivered')  # Redirect to same page to clear form
        else:
            # Show form with errors
            return render(request, 'dispatch_form.html', {'form': form})
    
    elif request.method == 'PATCH' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # AJAX endpoint for marking as delivered
        try:
            data = json.loads(request.body)
            dispatch_id = data.get('dispatch_id')
            if not dispatch_id:
                return HttpResponseBadRequest(_("Missing dispatch ID"))
            
            dispatch = Dispatch.objects.get(pk=dispatch_id)
            dispatch.mark_as_delivered()
            return JsonResponse({
                'status': 'success',
                'message': _("Marked as delivered"),
                'is_delivered': True
            })
            
        except Dispatch.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': _("Dispatch not found")
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': _(f"Error: {str(e)}")
            }, status=400)
    
    return HttpResponseBadRequest(_("Invalid request"))

@login_required
def dispatch_list_view(request):
    """
    Display all submitted dispatches in a table format
    """
    dispatches = Dispatch.objects.all().order_by('-dispatch_time')
    
    context = {
        'dispatches': dispatches,
        'table_headers': [
            _("Estimate ID"),
            _("Proforma ID"),
            _("Transport Cost"),
            _("Vehicle"),
            _("Driver"),
            _("Contact"),
            _("Dispatch Time"),
            _("Status"),
            _("Actions")
        ]
    }
    return render(request, 'dispatch_list.html', context)




@login_required
def record_estimate(request):
    if request.method == 'POST':
        # Check which form was submitted
        if 'excel_file' in request.FILES:
            return handle_excel_upload(request)
        else:
            return handle_form_submission(request)
    
    # GET request - show both forms
    form = EstimateForm(initial={
        'status': Estimate.Status.DRAFT,
        'bk_estimate_id': generate_estimate_id(),
        'sales_agent': request.user.get_full_name() or request.user.username
    })
    upload_form = EstimateUploadForm()
    
    return render(request, 'record_estimate.html', {
        'form': form,
        'upload_form': upload_form
    })
@login_required
def handle_form_submission(request):
    form = EstimateForm(request.POST)
    if form.is_valid():
        estimate = form.save()
        messages.success(request, f'Estimate #{estimate.bk_estimate_id} recorded successfully!')
        return redirect('list_estimates')
    else:
        upload_form = EstimateUploadForm()
        return render(request, 'record_estimate.html', {
            'form': form,
            'upload_form': upload_form
        })

@login_required
def handle_excel_upload(request):
    upload_form = EstimateUploadForm(request.POST, request.FILES)
    if not upload_form.is_valid():
        form = EstimateForm()
        return render(request, 'record_estimate.html', {
            'form': form,
            'upload_form': upload_form
        })
    
    try:
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        
        required_columns = ['bk_estimate_id', 'customer', 'status']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in Excel file")
        
        success_count = 0
        for _, row in df.iterrows():
            try:
                Estimate.objects.create(
                    bk_estimate_id=row['bk_estimate_id'],
                    customer=row['customer'],
                    sales_agent=row.get('sales_agent', request.user.get_full_name() or request.user.username),
                    status=row.get('status', Estimate.Status.DRAFT),
                    created_at=row.get('created_at', datetime.now())
                )
                success_count += 1
            except Exception as e:
                messages.warning(request, f"Error processing row {_ + 2}: {str(e)}")
        
        messages.success(request, f"Successfully imported {success_count} estimates!")
        return redirect('list_estimates')
    
    except Exception as e:
        messages.error(request, f"Error processing Excel file: {str(e)}")
        form = EstimateForm()
        upload_form = EstimateUploadForm()
        return render(request, 'record_estimate.html', {
            'form': form,
            'upload_form': upload_form
        })

@login_required
def generate_estimate_id():
    """Generate a new estimate ID in EST-YYYY-NNNN format"""
    from django.utils import timezone
    year = timezone.now().strftime('%Y')
    last_estimate = Estimate.objects.order_by('-bk_estimate_id').first()
    if last_estimate:
        last_num = int(last_estimate.bk_estimate_id.split('-')[-1])
        return f"EST-{year}-{last_num + 1:04d}"
    return f"EST-{year}-0001"


@login_required
def list_estimates(request):
    # Get filter parameters
    status_filter = request.GET.get('status')
    customer_filter = request.GET.get('customer')
    
    # Base queryset
    estimates = Estimate.objects.all().order_by('-created_at')
    
    # Apply filters
    if status_filter:
        estimates = estimates.filter(status=status_filter)
    if customer_filter:
        estimates = estimates.filter(customer__icontains=customer_filter)
    
    # Restrict view based on permissions
    if not request.user.has_perm('estimates.view_all_estimates'):
        estimates = estimates.filter(sales_agent=request.user.get_full_name() or request.user.username)
    
    # Pagination
    paginator = Paginator(estimates, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_choices': Estimate.Status.choices,
        'can_change_status': request.user.has_perm('estimates.change_estimate_status'),
    }
    return render(request, 'list_estimates.html', context)


from django.http import HttpResponse
import pandas as pd
from io import BytesIO


@login_required
def download_estimate_template(request):
    # Create a sample DataFrame
    data = {
        'bk_estimate_id': ['EST-2023-0001', 'EST-2023-0002'],
        'customer': ['Customer A', 'Customer B'],
        'sales_agent': ['Agent 1', 'Agent 2'],
        'status': ['draft', 'submitted'],
        'created_at': [datetime.now(), datetime.now()]
    }
    df = pd.DataFrame(data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Estimates')
    
    # Prepare response
    output.seek(0)
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=estimate_template.xlsx'
    return response

from django.utils import timezone

@login_required
def verify_dispatch(request, dispatch_id):
    dispatch = get_object_or_404(Dispatch, pk=dispatch_id)
    
    # Get the estimate if exists
    estimate = None
    if dispatch.estimate:
        estimate = Estimate.objects.filter(bk_estimate_id=dispatch.estimate).first()
    
    if request.method == 'POST':
        form = DispatchVerificationForm(request.POST, instance=dispatch)
        if form.is_valid():
            if 'verify' in request.POST:
                dispatch = form.save(commit=False)
                dispatch.mark_as_in_transit()
                messages.success(request, 'Dispatch verified and marked as In Transit!')
            elif 'cancel' in request.POST:
                dispatch = form.save(commit=False)
                dispatch.cancel_dispatch(form.cleaned_data.get('cancellation_reason'))
                messages.warning(request, 'Dispatch cancelled with reason.')
            return redirect('dispatch-detail', dispatch_id=dispatch.id)
    else:
        form = DispatchVerificationForm(instance=dispatch)
    
    context = {
        'dispatch': dispatch,
        'estimate': estimate,
        'form': form,
        'now': timezone.now().strftime("%Y-%m-%d %H:%M"),
    }
    return render(request, 'verify_dispatch.html', context)
import easyocr
import logging
import re
from django.http import JsonResponse
from django.shortcuts import render
from io import BytesIO
from .models import DeliveryNote, DeliveryNoteItem
from .forms import DeliveryNoteForm

# Initialize EasyOCR reader ONCE at module level to avoid repeated loading
# This is crucial for performance
try:
    reader = easyocr.Reader(['en'])  # English only for faster initialization
except Exception as e:
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize EasyOCR: {str(e)}")
    reader = None

def ocr_local(image_file):
    """Improved EasyOCR implementation with proper error handling"""
    if reader is None:
        return None

    try:
        # Ensure we're at the start of the file
        if hasattr(image_file, 'seek'):
            image_file.seek(0)
        
        # Read the image file directly (EasyOCR can handle bytes)
        image_bytes = image_file.read()
        
        # Perform OCR
        results = reader.readtext(image_bytes)
        
        # Combine all extracted text with line breaks for better parsing
        extracted_text = "\n".join([text for (_, text, _) in results])
        return extracted_text
    except Exception as e:
        logger.error(f"EasyOCR processing failed: {str(e)}")
        return None

# [Keep all your existing extract_* functions unchanged]

def upload_delivery_note(request):
    if request.method == 'POST':
        form = DeliveryNoteForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({
                'status': 'error',
                'message': 'Form is not valid.',
                'errors': form.errors
            }, status=400)

        try:
            if 'image' not in request.FILES:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No image file provided.'
                }, status=400)

            image = request.FILES['image']
            
            # Verify the image is not empty
            if image.size == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Empty image file provided.'
                }, status=400)

            # Try local OCR
            text = ocr_local(image)
            
            if not text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'OCR processing failed. Please try another image.',
                    'debug': 'EasyOCR returned no text'
                }, status=400)

            # Extract all fields
            extracted_data = {
                'estimate_number': extract_estimate_number(text),
                'customer_name_address': extract_customer_name_address(text),
                'sales_person': extract_sales_person(text),
                'date_of_delivery': extract_date_of_delivery(text),
                'items': extract_items(text),
                'raw_text': text  # For debugging
            }

            # Save to database
            delivery_note = form.save(commit=False)
            for field, value in extracted_data.items():
                if field != 'items' and field != 'raw_text':
                    setattr(delivery_note, field, value)
            delivery_note.save()

            # Save items
            for description, quantity in extracted_data['items']:
                DeliveryNoteItem.objects.create(
                    delivery_note=delivery_note,
                    description=description,
                    quantity=quantity
                )

            return JsonResponse({
                'status': 'success',
                'message': 'Delivery Note processed successfully.',
                'data': {k: v for k, v in extracted_data.items() if k != 'raw_text'}
            })

        except Exception as e:
            logger.error(f"Delivery note processing error: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'An unexpected error occurred.',
                'debug': str(e)
            }, status=500)

    # GET request
    form = DeliveryNoteForm()
    return render(request, 'upload_delivery_note.html', {'form': form})


from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.urls import reverse

@require_POST
def confirm_delivery(request, pk):
    note = get_object_or_404(DeliveryNote, pk=pk)
    note.status = 'confirmed'
    note.save()
    return JsonResponse({'success': True})
    
from django.http import JsonResponse
from django.urls import reverse
import json

def create_delivery_note(request):
    if request.method == 'POST':
        form = DeliveryNoteForm(request.POST, request.FILES)
        
        if form.is_valid():
            delivery_note = form.save(commit=False)
            delivery_note.sales_person = request.user.get_full_name() or request.user.username
            delivery_note.status = 'pending'
            delivery_note.save()
            
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('delivery_note_list'),
                'message': "Delivery note submitted successfully!"
            })
        else:
            # Convert form errors to a more detailed format
            errors = {}
            for field in form.errors:
                errors[field] = {
                    'id': f'id_{field}',  # matches Django's default ID format
                    'errors': form.errors[field]
                }
            
            return JsonResponse({
                'success': False,
                'errors': errors,
                'message': "Please correct the errors below.",
                'form_errors': form.errors.as_json()
            }, status=400)
    
    # GET request handling
    form = DeliveryNoteForm()
    return render(request, 'delivery_notes/create.html', {'form': form})
    
@login_required
def delivery_note_list(request):
    notes = DeliveryNote.objects.all()
    return render(request, 'delivery_notes/list.html', {'notes': notes})